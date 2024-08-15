"""_summary_
"""
import logging
from dataclasses import dataclass
from typing import Any, Dict

from iisi.exception import AuthenticationException
from iisi.principal import Principal
from iisi.resolvers.resolver import PrincipalResolver

log = logging.getLogger(__name__)


@dataclass
class JwtPrincipalResolver(PrincipalResolver):
    """Handle JWT token claims."""

    domain_name: str

    def resolve(self, event: Dict[str, Any]):
        """_summary_

        Args:
            event (Dict[str, Any]): _description_

        Raises:
            AuthenticationException: _description_

        Returns:
            _type_: _description_
        """
        try:
            log.debug("%s: %s, domain: %s", self.__class__.__name__, event, self.domain_name)
            claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
            return Principal.new(
                user_id=claims[f"{self.domain_name}/user_id"],
                customer_id=claims[f"{self.domain_name}/customer_id"],
                roles=claims[f"{self.domain_name}/roles"].lstrip("[").rstrip("[").split(),
            )
        except Exception as exc:
            log.exception(exc)
            raise AuthenticationException("Error handling jwt claims.") from exc
