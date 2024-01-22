"""
B-Tocs Container SDK for Python - FastAPI Layer
Fast API Support

mdjoerg@b-tocs.com
"""
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, HTMLResponse
from ...service import ServiceManager
from ...security import SecurityManager
from ...security.context import SecurityContext
from .session import FastAPISession
from ...config import ConfigManager
from ...rest.const import RESTAPI_HOST, RESTAPI_PORT


class FastAPIService:

    def __init__(self):
        self.tags_metadata = None
        self.description = None
        self.docs_url = "/apidoc"
        self.title = None
        self.version = None
        self.app: FastAPI = None

    def configure(self,
                  version: str = None,
                  title: str = None,
                  description: str = None,
                  tags_metadata: list = None,
                  docs_url: str = None
                  ):
        if version:
            self.version = version
        if title:
            self.title = title
        if description:
            self.description = description
        if tags_metadata:
            self.tags_metadata = tags_metadata
        if docs_url:
            self.docs_url = docs_url

    def set_app(self, app: FastAPI):
        self.app = app

    def get_app(self) -> FastAPI:
        if not self.app:
            self.app = FastAPI(
                version=self.get_version(),
                title=self.get_title(),
                description=self.get_description(),
                openapi_tags=self.tags_metadata,
                docs_url=self.docs_url
            )
        return self.app

    def get_version(self) -> str:
        if self.version:
            return self.version
        else:
            return ServiceManager.get_version()

    def get_title(self) -> str:
        if self.title:
            return self.title
        else:
            return ServiceManager.get_title()

    def get_description(self) -> str:
        if self.description:
            return self.description
        else:
            return ServiceManager.get_description()

    def add_tag_meta(self, name: str, description: str):
        if not self.tags_metadata:
            self.tags_metadata = []
        self.tags_metadata.append({"name": name, "description": description})

    def create_response_ok(self, msg=None, status_code: int = 200) -> Response:
        if not msg:
            msg = "OK"
        return JSONResponse(content={"msg": msg}, status_code=status_code)

    def create_response_bad(self, reason: str = None) -> Response:
       detail = "bad request"
       if reason:
           detail = reason
       return JSONResponse(content={ "detail": detail}, status_code=400)

    def create_response_invalid_auth(self, reason: str = None) -> Response:
       detail = "invalid authorization"
       if reason:
           detail = reason
       return JSONResponse(content={ "detail": detail}, status_code=400)


    def run(self, port: int = int(ConfigManager.get_manager().get_config(RESTAPI_PORT, "8000")), host: str = ConfigManager.get_manager().get_config(RESTAPI_HOST, "0.0.0.0"), layout: str = ServiceManager.get_service_layout()):
        print(f"Starting REST API with layout {layout} accepting requests from {host} at port {port}")
        uvicorn.run(self.get_app(), port=port, host=host)
        print(f"REST API stopped at port {port} - layout {layout}")

    def session_start(self, request: Request, api_method: str, access_level: str = None, required_role: str = None, tenant: str = None, account: str = None) -> FastAPISession:
        # init session
        session = FastAPISession(request=request, api_method=api_method, access_level=access_level, required_role=required_role, tenant=tenant, account=account)

        # check authentification
        security_context = SecurityManager.get_security_context(access_level=access_level, account=account, tenant=tenant)
        if not security_context.is_authorized(session=session, required_role=required_role):
            session.get_logger().error("authorization failed")
            session.set_response(self.create_response_invalid_auth())
        #else:  TODO: getUserContext

        # return session
        return session


    def session_finish(self, session: FastAPISession, result, reason: str = None):

        final_result = result

        if not final_result:
            final_result = self.create_bad_request()

        return final_result


