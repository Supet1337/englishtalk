from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import talkapp.routing

application = ProtocolTypeRouter({
	# Empty for now (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			talkapp.routing.websocket_urlpatterns
		)
	),
})