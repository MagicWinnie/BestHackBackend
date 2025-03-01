# from .auth.routes import router as auth_router
from .user.routes import router as user_router

routers = [user_router]
