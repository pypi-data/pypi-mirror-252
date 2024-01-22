from fastapi import Request, Response
from ...context.session import RestAPISession

class FastAPISession(RestAPISession):
    def __init__(self, request: Request, api_method: str, access_level: int = 0, required_role: int = 0, tenant: str = None, account: str = None):
        super().__init__(api_method=api_method, access_level=access_level, required_role=required_role, tenant=tenant, account=account)
        self.request: Request = request
        self.response: Response = None

        if not self.init_session_from_request(request):
            self.get_logger().error("init session from request failed")

    def get_response(self) -> Response:
        return self.response

    def set_response(self, response: Response):
        self.response = response

    def init_session_from_request(self, request: Request) -> bool:
        if not request:
            return False
        else:
            try:
                self.get_logger().trace(f"Start init session from request for uuid {self.session_uuid}")

                # headers
                self.get_headers().clear()
                for hkey in request.headers:
                    hvalue = request.headers.get(hkey)
                    if hvalue:
                        self.get_headers().set(hkey, hvalue)

                # parameters
                self.get_parameters().clear()
                for qkey in request.query_params:
                    qvalue = request.query_params.get(qkey)
                    if qvalue:
                        self.get_parameters().set(qkey, qvalue)

                for pkey in request.path_params:
                    pvalue = request.path_params.get(pkey)
                    if qvalue:
                        self.get_parameters().set(pkey, pvalue)

                return True
            except Exception as exc:
                self.get_logger().error(f"init session from request failed: {exc}")
                return False

