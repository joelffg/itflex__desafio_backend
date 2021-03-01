from itflex.http_config import setup_app
from itflex.openapi import setup_openapi_api

app, socketio = setup_app(["itflex_service"])
#setup_openapi_api(app)
