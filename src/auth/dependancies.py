from fastapi.security import HTTPBearer
from fastapi import Request ,status ,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.redis_config import CHECK_JTI_IN_BLOCKLIST
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import Userservice
from typing import List
from src.db.models import User
from src.errors import *

user_service= Userservice()


class TokenBearer(HTTPBearer):
    
    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token_data=decode_token(creds.credentials)

        if token_data is None:
            raise InvalidToken()
        
        jti=token_data['jti']
        jti_valid = await CHECK_JTI_IN_BLOCKLIST(jti)
        if jti_valid is True :
            raise InvalidToken()
        self.verify_token_data(token_data)
        return token_data
    
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data : dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()
        return token_data
    
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data : dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()
        return token_data
    
async def get_current_user(token_details : dict = Depends(AccessTokenBearer()) , session : AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email,session)
    return user 

class RoleChecker:
    def __init__(self,allowed_roles : List[str]):
        self.allowed_roles = allowed_roles
    def __call__(self, current_user : User = Depends(get_current_user)):
        if(current_user.role in self.allowed_roles):
            return True
        raise InsufficientPermission()
    