"""_summary_"""
import importlib
import logging
import os
import pkgutil
from types import ModuleType
from typing import Any, Dict

import punq

from iisi.exception import ApplicationException
from iisi.factories import DynamoDbTableConnectionFactory, TableFactory
from iisi.handlers import DefaultUsecaseHandler, HttpResultHandler, ResultHandler, UsecaseHandler
from iisi.resolvers import (
    DefaultParameterResolver,
    DefaultUsecaseResolver,
    DefaultUsecaseStackResolver,
    JwtPrincipalResolver,
    ParameterResolver,
    PrincipalResolver,
    UsecaseResolver,
    UsecaseStackResolver,
)

log_level = os.environ.get("LOGLEVEL", "DEBUG").upper()

if len(logging.getLogger().handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr.
    # If a handler is already configured, `.basicConfig` does not execute.
    # Thus we set the level directly.
    logging.getLogger().setLevel(log_level)

else:
    logging.basicConfig(level=log_level)

for name in ["boto", "urllib3", "s3transfer", "boto3", "botocore", "nose"]:
    logging.getLogger(name).setLevel(logging.ERROR)


class App:
    """_summary_"""

    def __init__(self, table_name: str, domain_name: str):
        container = punq.Container()
        container.register(ParameterResolver, DefaultParameterResolver)
        container.register(UsecaseStackResolver, DefaultUsecaseStackResolver)
        container.register(ResultHandler, HttpResultHandler)
        container.register(UsecaseHandler, DefaultUsecaseHandler)
        container.register(UsecaseResolver, DefaultUsecaseResolver)
        container.register(TableFactory, DynamoDbTableConnectionFactory, table_name=table_name)
        container.register(PrincipalResolver, JwtPrincipalResolver, domain_name=domain_name)

        self.container = container
        self.register = self.container.register
        self.resolve = self.container.resolve

    def handle_event(self, event: Dict, _context: Dict) -> Any:
        """_summary_"""
        logging.debug("APP.handle_event")

    def register_component(self, component_module: ModuleType) -> None:
        try:
            package_path = os.path.dirname(component_module.__file__)  # type: ignore
            for module_info in pkgutil.iter_modules([package_path]):  # type: ignore
                if module_info.ispkg:
                    usecase_module_name = component_module.__name__ + "." + module_info.name
                    usecase_module = importlib.import_module(usecase_module_name)
                    package_path = os.path.dirname(usecase_module.__file__)  # type: ignore
                    for module_info in pkgutil.iter_modules([package_path]):  # type: ignore
                        usecase_module_name = usecase_module.__name__ + "." + module_info.name
                        importlib.import_module(usecase_module_name)

        except Exception as exc:
            logging.exception(exc)
            raise ApplicationException("Error registering application component.") from exc
