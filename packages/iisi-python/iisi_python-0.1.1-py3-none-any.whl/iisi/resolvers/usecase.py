"""_summary_"""
import importlib
import inspect
import logging as log
import os
import os.path
import pkgutil
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Dict, Type

from iisi.domain.usecasestack import UseCaseStack
from iisi.exception import ApplicationException
from iisi.resolvers.resolver import UsecaseResolver, UsecaseStackResolver
from iisi.routes import routes
from iisi.usecase import IController, IPort, IRepository, IService


@dataclass
class DefaultUsecaseStackResolver(UsecaseStackResolver):
    """_summary_"""

    usecase_resolver: UsecaseResolver

    def resolve(self, event: Dict[str, Any]) -> UseCaseStack:  # noqa: C901
        """_summary_"""
        try:
            controller: Type[IController]
            service: Type[IService]
            repository: Type[IRepository]
            repository_port: Type[IPort]

            fnc = self.usecase_resolver.resolve(event)
            package_path = ".".join(inspect.getmodule(fnc).__name__.split(".")[:-1])  # type: ignore
            usecase_module = importlib.import_module(package_path)
            package_path = os.path.dirname(usecase_module.__file__)  # type: ignore
            for module_info in pkgutil.iter_modules([package_path]):  # type: ignore
                usecase_module_name = usecase_module.__name__ + "." + module_info.name
                imported_usecase_module = importlib.import_module(usecase_module_name)
                for _, uc_class in inspect.getmembers(imported_usecase_module):
                    if inspect.isclass(uc_class) and uc_class.__module__ == usecase_module_name:
                        if issubclass(uc_class, IController):
                            controller = uc_class
                        if issubclass(uc_class, IService):
                            service = uc_class
                        if issubclass(uc_class, IRepository):
                            if len(uc_class.__subclasses__()) == 0:
                                repository = uc_class
                            if len(uc_class.__subclasses__()) > 0:
                                repository_port = uc_class  # type: ignore
            return UseCaseStack(controller, service, repository_port, repository)  # type: ignore
        except Exception as exc:
            log.exception(exc)
            raise ApplicationException("Error resolving usecase stack.") from exc


@dataclass
class DefaultUsecaseResolver(UsecaseResolver):
    """_summary_"""

    def resolve(self, event: Dict[str, Any]) -> ModuleType:
        """_summary_"""
        return routes[event.get("routeKey", "$default")]
