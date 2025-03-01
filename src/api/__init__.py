from .auth.routes import router as auth_router
from .user.routes import router as user_router

routers = [auth_router, user_router]
