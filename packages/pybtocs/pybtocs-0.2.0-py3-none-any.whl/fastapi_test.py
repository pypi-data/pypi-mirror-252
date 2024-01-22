from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from pybtocs.service import ServiceManager
from pybtocs.rest.fastapi.core import FastAPIService
from pybtocs.security import SecurityManager, SecurityManagerInterface


# configure B-Tocs Layer
VERSION = '0.1.0'
service = FastAPIService()
#service.configure(title="B-Tocs Demo Service", description="Template for use B-Tocs FastAPI SDK Layer", version="1.0.0")


# configure fastapi layer
app = service.get_app()


@app.get("/healthcheck")
async def healthcheck(request: Request):
    return HTMLResponse(content="healthy")


@app.get("/test/{account}/{tenant}")
async def test_get_request(request: Request, account: str = None, tenant: str = None):
    session = service.session_start(request, "test_get_request", account=account, tenant=tenant, access_level=SecurityManagerInterface.ACCESS_LAYER_SERVICE, required_role=SecurityManagerInterface.REQUIRED_ROLE_PUBLIC)
    result = session.get_response()
    if not result:
        result = service.create_response_ok({
            "session": session.get_uuid(),
            "tenant": tenant,
            "account": account,
            "headers": session.get_headers().get_dict(),
            "parameters": session.get_parameters().get_dict()
        })
    return service.session_finish(session, result)

@app.post("/test")
async def test_post_request(request: Request, payload: dict = Body()):
    session = service.session_start(request, "test_post_request", access_level=SecurityManagerInterface.ACCESS_LAYER_SERVICE, required_role=SecurityManagerInterface.REQUIRED_ROLE_PUBLIC)
    result = session.get_response()
    if not result:
        result = service.create_response_ok({
            "session": session.get_uuid(),
            "payload": payload,
            "headers": session.get_headers().get_dict(),
            "parameters": session.get_parameters().get_dict()

        })
    return service.session_finish(session, result)


if __name__ == "__main__":
    ServiceManager.register("B-Tocs FastAPI Example", VERSION, "Demo Template for building python based containers for enterprise usage ")
    ServiceManager.startup()
    service.run()
    ServiceManager.stop()
