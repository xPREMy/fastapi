from fastapi.security import HTTPBearer
from fastapi import Request ,status 
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException 

class TokenBearer(HTTPBearer):
    
    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token_valid=self.token_valid(creds.credentials)
        if token_valid is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
        token_data=decode_token(creds.credentials)
        self.verify_token_data(token_data)
        return token_data

    def token_valid(self,token : str) -> bool:

        token_data=decode_token(token)

        if token_data is not None:
            return True
        
        return False
    
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