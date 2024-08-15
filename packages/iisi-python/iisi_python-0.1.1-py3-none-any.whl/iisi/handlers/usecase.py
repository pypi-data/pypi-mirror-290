"""_summary_"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Union

import punq

from iisi.context import app_context
from iisi.domain.usecasestack import UseCaseStack
from iisi.handlers.handler import UsecaseHandler
from iisi.handlers.result import ResultHandler
from iisi.resolvers import ParameterResolver, PrincipalResolver, UsecaseStackResolver

log = logging.getLogger(__name__)


@dataclass
class DefaultUsecaseHandler(UsecaseHandler):
    """_summary_"""

    container: punq.Container
    principal_resolver: PrincipalResolver
    parameter_resolver: ParameterResolver
    usecase_stack_resolver: UsecaseStackResolver
    result_handler: ResultHandler

    def handle(self, event: Dict[str, Any], _result: Any = None) -> Union[Dict, None]:
        """
        Resolve request params

        :param event: The event to handle.
        """
        log.debug("%s", event)
        app_context().principal = self.principal_resolver.resolve(event)

        # Resolve usecase handler
        usecase_stack: UseCaseStack = self.usecase_stack_resolver.resolve(event)

        self.container.register(usecase_stack.controller)
        self.container.register(usecase_stack.service)
        self.container.register(usecase_stack.repository_port, usecase_stack.repository)
        usecase_handler = self.container.resolve(usecase_stack.controller)

        # Resolve params
        params = self.parameter_resolver.resolve(event)

        # Execute handler
        result = usecase_handler(**params)  # type: ignore
        return self.result_handler.handle(result)
