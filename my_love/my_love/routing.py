from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

import news.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(SessionMiddlewareStack(
        URLRouter(news.routing.websocket_urlpatterns)
    )),
})