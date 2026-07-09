from passlib.context import CryptContext
from datetime import datetime , timedelta
import jwt
from src.config import settings
import uuid
import  logging

passwd_context= CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password:str) -> str:
    hash= passwd_context.hash(password)
    return hash

def verify_password(password: str, hash : str) -> bool:
    return passwd_context.verify(password,hash)

def create_access_token(userdata : dict , expiry : timedelta = None , refresh : bool = False):
    
    payload={}

    payload['user']= userdata
    payload['exp']=datetime.now()+ (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key= settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )

    return token

def decode_token(token : str) -> dict:
    try:
        token_data= jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None