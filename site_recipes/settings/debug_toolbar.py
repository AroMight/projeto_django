from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INSTALLED_APPS += [
    'debug_toolbar',
]

# DJango Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
