import re
from pathlib import Path

from collections import OrderedDict
from itertools import groupby
import google.protobuf.descriptor_pb2 as descriptor_pb2

"""
https://github.com/marin-m/pbtk/blob/master/utils/descpb_to_proto.py
"""


class ProtoRecover:
    def __init__(self, descriptor: descriptor_pb2.FileDescriptorProto):
        self.descriptor = descriptor

    def get_proto(self, output_dir: Path = None):
        out = 'syntax = "%s";\n\n' % (self.descriptor.syntax or "proto2")

        scopes = [""]
        if self.descriptor.package:
            out += "package %s;\n\n" % self.descriptor.package
            scopes[0] += "." + self.descriptor.package

        for index, dep in enumerate(self.descriptor.dependency):
            prefix = " public" * (index in self.descriptor.public_dependency)
            prefix += " weak" * (index in self.descriptor.weak_dependency)
            imports = 'import%s "%s";\n' % (prefix, dep)

            out += self._patch_import(imports)
            scopes.append("." + ("/" + dep.rsplit("/", 1)[0])[1:].replace("/", "."))

        out += "\n" * (out[-2] != "\n")
        out += self._parse_msg(self.descriptor, scopes, self.descriptor.syntax).strip(
            "\n"
        )
        name = self.descriptor.name.replace("..", "").strip(".\\/")
        proto = {"name": name, "content": out}
        file_path = self._write_proto_file(proto=proto, output_dir=output_dir)

        return file_path

    @staticmethod
    def _write_proto_file(proto: dict, output_dir: Path = None):
        parts = proto["name"].rsplit(".", 1)
        directory = parts[0].replace(".", "/")
        new_path = directory if len(parts) == 1 else f"{directory}.{parts[1]}"
        proto_name = output_dir / new_path
        proto_name.parent.mkdir(parents=True, exist_ok=True)
        with open(proto_name, "w") as f:
            f.write(proto["content"])
        return proto_name

    @staticmethod
    def _patch_import(content: str):
        if "google" not in content:
            content = re.sub(r"\.(?=.*\.)", r"/", content)
        return content

    def _parse_msg(
        self, desc: descriptor_pb2.DescriptorProto, scopes: list, syntax: str
    ):
        out = ""
        is_msg = isinstance(desc, descriptor_pb2.DescriptorProto)

        if is_msg:
            scopes = list(scopes)
            scopes[0] += "." + desc.name

        blocks = OrderedDict()
        for nested_msg in desc.nested_type if is_msg else desc.message_type:
            blocks[nested_msg.name] = self._parse_msg(nested_msg, scopes, syntax)

        for enum in desc.enum_type:
            out2 = ""
            for val in enum.value:
                out2 += "%s = %s;\n" % (
                    val.name,
                    self._fmt_value(val.number, val.options),
                )

            if len(set(i.number for i in enum.value)) == len(enum.value):
                enum.options.ClearField("allow_alias")

            blocks[enum.name] = self._wrap_block("enum", out2, enum)

        if is_msg and desc.options.map_entry:
            return " map<%s>" % ", ".join(
                (
                    self._min_name(i.type_name, scopes)
                    if i.type_name
                    else self._types[i.type]
                )
                for i in desc.field
            )

        if is_msg:
            for field in desc.field:
                out += self._fmt_field(field, scopes, blocks, syntax)

            for index, oneof in enumerate(desc.oneof_decl):
                out += self._wrap_block("oneof", blocks.pop("_oneof_%d" % index), oneof)

            out += self._fmt_ranges("extensions", desc.extension_range)
            out += self._fmt_ranges(
                "reserved", [*desc.reserved_range, *desc.reserved_name]
            )

        else:
            for service in desc.service:
                out2 = ""
                for method in service.method:
                    out2 += "rpc %s(%s%s) returns (%s%s);\n" % (
                        method.name,
                        "stream " * method.client_streaming,
                        self._min_name(method.input_type, scopes),
                        "stream " * method.server_streaming,
                        self._min_name(method.output_type, scopes),
                    )

                out += self._wrap_block("service", out2, service)

        extends = OrderedDict()
        for ext in desc.extension:
            extends.setdefault(ext.extendee, "")
            extends[ext.extendee] += self._fmt_field(ext, scopes, blocks, syntax, True)

        for name, value in blocks.items():
            out += value[:-1]

        for name, fields in extends.items():
            out += self._wrap_block("extend", fields, name=self._min_name(name, scopes))

        out = self._wrap_block("message" * is_msg, out, desc)
        return out

    def _fmt_value(self, val, options=None, desc=None, optarr=[]):
        if type(val) != str:
            if type(val) == bool:
                val = str(val).lower()
            elif desc and desc.enum_type:
                val = desc.enum_type.values_by_number[val].name
            val = str(val)
        else:
            val = '"%s"' % val.encode("unicode_escape").decode("utf8")

        if options:
            opts = [*optarr]
            for option, value in options.ListFields():
                opts.append(
                    "%s = %s" % (option.name, self._fmt_value(value, desc=option))
                )
            if opts:
                val += " [%s]" % ", ".join(opts)
        return val

    @property
    def _types(self):
        types = {
            v: k.split("_")[1].lower()
            for k, v in descriptor_pb2.FieldDescriptorProto.Type.items()
        }
        return types

    @property
    def _labels(self):
        labels = {
            v: k.split("_")[1].lower()
            for k, v in descriptor_pb2.FieldDescriptorProto.Label.items()
        }
        return labels

    def _fmt_field(self, field, scopes, blocks, syntax, extend=False):
        type_ = self._types[field.type]

        default = ""
        if field.default_value:
            if field.type == field.TYPE_STRING:
                default = ["default = %s" % self._fmt_value(field.default_value)]
            elif field.type == field.TYPE_BYTES:
                default = ['default = "%s"' % field.default_value]
            else:
                # Guess whether it ought to be more readable as base 10 or 16,
                # based on the presence of repeated digits:

                if (
                    ("int" in type_ or "fixed" in type_)
                    and int(field.default_value) >= 0x10000
                    and not any(
                        len(list(i)) > 3 for _, i in groupby(str(field.default_value))
                    )
                ):
                    field.default_value = hex(int(field.default_value))

                default = ["default = %s" % field.default_value]

        out = ""
        if field.type_name:
            type_ = self._min_name(field.type_name, scopes)
            short_type = type_.split(".")[-1]

            if short_type in blocks and (
                (not extend and not field.HasField("oneof_index"))
                or blocks[short_type].startswith(" map<")
            ):
                out += blocks.pop(short_type)[1:]

        if out.startswith("map<"):
            line = out + " %s = %s;\n" % (
                field.name,
                self._fmt_value(field.number, field.options, optarr=default),
            )
            out = ""
        elif field.type != field.TYPE_GROUP:
            line = "%s %s %s = %s;\n" % (
                self._labels[field.label],
                type_,
                field.name,
                self._fmt_value(field.number, field.options, optarr=default),
            )
        else:
            line = "%s group %s = %d " % (
                self._labels[field.label],
                type_,
                field.number,
            )
            out = out.split(" ", 2)[-1]

        if field.HasField("oneof_index") or (
            syntax == "proto3" and line.startswith("optional")
        ):
            line = line.split(" ", 1)[-1]
        if out:
            line = "\n" + line

        if field.HasField("oneof_index"):
            blocks.setdefault("_oneof_%d" % field.oneof_index, "")
            blocks["_oneof_%d" % field.oneof_index] += line + out
            return ""
        else:
            return line + out

    def _min_name(self, name, scopes):
        name, cur_scope = name.split("."), scopes[0].split(".")
        short_name = [name.pop()]

        while name and (
            cur_scope[: len(name)] != name
            or any(
                self._list_rfind(scope.split("."), short_name[0]) > len(name)
                for scope in scopes
            )
        ):
            short_name.insert(0, name.pop())

        return ".".join(short_name)

    def _wrap_block(self, type_, value, desc=None, name=None):
        out = ""
        if type_:
            out = "\n%s %s {\n" % (type_, name or desc.name)

        if desc:
            for option, optval in desc.options.ListFields():
                value = (
                    "option %s = %s;\n"
                    % (option.name, self._fmt_value(optval, desc=option))
                    + value
                )

        value = value.replace("\n\n\n", "\n\n")
        if type_:
            out += "\n".join(" " * 4 + line for line in value.strip("\n").split("\n"))
            out += "\n}\n\n"
        else:
            out += value
        return out

    def _fmt_ranges(self, name, ranges):
        text = []
        for range_ in ranges:
            if type(range_) != str and range_.end - 1 > range_.start:
                if range_.end < 0x20000000:
                    text.append("%d to %d" % (range_.start, range_.end - 1))
                else:
                    text.append("%d to max" % range_.start)
            elif type(range_) != str:
                text.append(self._fmt_value(range_.start))
            else:
                text.append(self._fmt_value(range_))
        if text:
            return "\n%s %s;\n" % (name, ", ".join(text))
        return ""

    # Fulfilling a blatant lack of the Python language.
    def _list_rfind(self, x, i):
        return len(x) - 1 - x[::-1].index(i) if i in x else -1
