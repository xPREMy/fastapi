from fastapi.security import HTTPBearer
from fastapi import Request ,status ,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis_config import CHECK_JTI_IN_BLOCKLIST
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import Userservice
user_service= Userservice()
from typing import List

class TokenBearer(HTTPBearer):
    
    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token_data=decode_token(creds.credentials)

        if token_data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        
        jti=token_data['jti']
        jti_valid = await CHECK_JTI_IN_BLOCKLIST(jti)
        if jti_valid is True :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token revoked or invalid")
        self.verify_token_data(token_data)
        return token_data
    
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data : dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide valid access token"
            ) 
        return token_data
    
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data : dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="please provide refresh token"
            ) 
        return token_data
    
async def get_current_user(token_details : dict = Depends(AccessTokenBearer()) , session : AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email,session)
    return user 

class RoleChecker:
    def __init__(self):
        