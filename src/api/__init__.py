from .auth.routes import router as auth_router
from .lot.routes import router as lot_router
from .user.routes import router as user_router

routers = [auth_router, lot_router, user_router]
