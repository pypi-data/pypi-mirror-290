from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from quick_api_tests.logger.log import LOGGER


class BaseGenerator(ABC):
    BASE_PATH: Path
    CORE_INIT_CONTENT: str = ""

    def __init__(self) -> None:
        if not self.BASE_PATH.exists():
            LOGGER.debug("base directory does not exists, creating...")
            self.BASE_PATH.mkdir(parents=True, exist_ok=True)

        for parent in self.BASE_PATH.parents:
            init_file = parent / "__init__.py"
            if not init_file.exists():
                init_file.touch()
        (self.BASE_PATH / "__init__.py").touch()

    # @property
    # def _config(self):
    #     return NukeConfig.read()

    @abstractmethod
    def generate(self) -> None: ...


class BaseApiDescriptor(ABC):
    @abstractmethod
    def handlers_by_api_name(self, api_name: str) -> None: ...

    @abstractmethod
    def handlers_by_method_type(self, method_type: str) -> None: ...

    @abstractmethod
    def models_by_api_name(self, api_name: str) -> None: ...

    @property
    @abstractmethod
    def client_type(self) -> str: ...

    @property
    @abstractmethod
    def apis(self) -> set[str]: ...

    @property
    @abstractmethod
    def service_name(self) -> str: ...
