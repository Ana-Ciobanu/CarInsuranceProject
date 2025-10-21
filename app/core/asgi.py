from asgiref.wsgi import WsgiToAsgi
from main import create_app

asgi_app = WsgiToAsgi(create_app())
