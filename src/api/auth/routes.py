from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.auth.dependencies import validate_credentials
from src.api.auth.schemas import TokenInfo
from src.api.auth.service import AuthService
from src.core.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/generate", response_model=TokenInfo)
def generate_tokens(user: Annotated[User, Depends(validate_credentials)]):
    return AuthService.generate_tokens(user)


# @router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
# def refresh_access_token(admin: Admin = Depends(AdminGetterFromToken(TokenType.REFRESH))):
#     return jwt_admin_service.refresh_token(admin)


# @router.get("/validate", response_model=ValidateReturnSchema)
# async def validate_token(
#     payload: JWTData = Depends(get_current_token_payload),
#     admin: Admin = Depends(AdminGetterFromToken(TokenType.ACCESS)),
# ):
#     return jwt_admin_service.get_admin_info(admin, payload)
