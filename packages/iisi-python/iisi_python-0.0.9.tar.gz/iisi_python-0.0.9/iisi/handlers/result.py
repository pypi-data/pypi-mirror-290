"""
Result handlers module.
"""
import json
from abc import ABC
from dataclasses import asdict, dataclass
from http import HTTPStatus
from typing import Any, Dict, Union

from authoritah import NotAuthorized

from iisi.exception import DataException, NotAuthorizedException


@dataclass
class ResultHandler(ABC):
    """_summary_"""

    def handle(self, result: Dict[str, Any]) -> Union[Dict, None]:
        """_summary_

        Args:
            result (Dict[str, Any]): _description_

        Returns:
            Union[Dict, None]: _description_
        """
        raise NotImplementedError(f"{type(self).__name__} not implemented.")


@dataclass
class HttpResultHandler(ResultHandler):
    """
    Http result handler
    """

    def handle(self, result: Dict[str, Any]) -> Union[Dict, None]:
        """
        Handle result

        :param event: The event to handle.
        """
        try:
            return self._ok_response(result)
        except (ValueError, TypeError) as value_error:
            return self._response(HTTPStatus.BAD_REQUEST, str(value_error))
        except (NotAuthorized, NotAuthorizedException) as not_authorized:
            return self._response(HTTPStatus.UNAUTHORIZED, str(not_authorized))
        except DataException as repo_error:
            return self._response(HTTPStatus.INTERNAL_SERVER_ERROR, str(repo_error))
        except Exception as error:  # pylint: disable=broad-except
            return self._response(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))

    def _ok_response(self, output: Any) -> Dict:
        """OK response."""
        body = (
            [asdict(item) for item in output]
            if isinstance(output, list)
            else asdict(output)
            if output is not None
            else None
        )
        return {
            "statusCode": HTTPStatus.OK,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body) if body is not None else None,
        }

    def _response(self, status_code: HTTPStatus, output: str) -> Dict:
        """Http status response."""
        body = output if output is not None else None
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": body,
        }


class CliResultHandler(ResultHandler):
    """
    Cli result handler.

    :param AppHandler: _description_.
    """

    def handle(self, _event: Dict[str, Any], result: Any = None) -> Union[Dict, None]:
        """
        Handle result as cli response.

        :param event: The event to handle.
        """
        try:
            self.ok_response(result)
        except (ValueError, TypeError) as value_error:
            self.error_response("Bad request:", value_error)
        except NotAuthorized as not_authorized:
            self.error_response("Not authorized:", not_authorized)
        except Exception as error:  # pylint: disable=broad-except
            self.error_response("Unknown error:", error)
        return None

    def ok_response(self, output: Any) -> None:
        """Print out ok response."""
        body = (
            [asdict(item) for item in output]
            if isinstance(output, list)
            else asdict(output)
            if output is not None
            else None
        )
        print("ok:" + str(body) if body is not None else "ok")

    def error_response(self, prefix: str, output: Any) -> None:
        """Print error out response."""
        print(prefix + str(asdict(output)) if output is not None else prefix)
