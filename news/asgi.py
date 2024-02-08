import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import main.routing  # Import your app's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        main.routing.websocket_urlpatterns
    ),
})
