from asgiref.wsgi import WsgiToAsgi
from app.main import create_app

asgi_app = WsgiToAsgi(create_app())
