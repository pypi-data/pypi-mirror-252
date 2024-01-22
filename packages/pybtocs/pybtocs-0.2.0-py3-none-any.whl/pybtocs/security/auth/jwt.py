from ..plugins import PluginCheckAuthInterface
from ...context.user import UserContext
from ...context.session import SessionInterface
from ...security.context import SecurityContext

import jwt

class UserContextJWT(UserContext):
    def __init__(self, jwt_payload: dict):
        self.jwt_payload = jwt_payload

    def set_is_validated(self):
        self.validated = True


class PluginCheckAuthJWT(PluginCheckAuthInterface):

    def get_id(self) -> str:
        return "pybtocs.PluginCheckAuthJWT"

    def get_title(self) -> str:
        return "Check Auth for JWT Token"

    def get_user_context(self, session: SessionInterface, security_context: SecurityContext = None, validate: bool = True) -> UserContext:
        try:
            # check jwt bearer
            auth_header = session.get_headers().get(self.HEADER_AUTHORIZATION)
            if not str(auth_header).startswith(self.HEADER_AUTHORIZATION_BEARER):
                session.get_logger().trace("JWT Bearer token not found")
                return None

            # check payload without validation
            token_encoded = auth_header.split(" ")[1]
            payload_decoded = jwt.decode(token_encoded, options={"verify_signature": False})
            if not payload_decoded:
                session.get_logger().trace("invalid JWT token found")
                return None
            else:
                session.get_logger().trace("valid JWT token found")

            # set user context unchecked
            user_context = UserContextJWT(jwt_payload=payload_decoded)
            if not validate:
                session.get_logger().trace("validating JWT token not required")
                return user_context

            # check security context and get secret
            if not security_context:
                session.get_logger().trace("Security context required for validating JWT token")
                return

            secret = security_context.get_secret()
            if not secret:
                session.get_logger().trace("Security context required for validating JWT token")
                return


            # validate token
            validated_payload = jwt.decode(token_encoded, secret, algorithms="HS256")
            if validated_payload == payload_decoded:
                user_context.set_is_validated()
                session.get_logger().trace("JWT payload is valid")
            else:
                session.get_logger().trace("JWT payload is not valid. return invalid user context")

            # return
            return user_context
        except Exception as exc:
            session.get_logger().error(f"errors occured while validating jwt token: {exc}")
            return None