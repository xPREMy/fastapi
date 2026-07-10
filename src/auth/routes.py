from fastapi import APIRouter, HTTPException , Depends ,status , Query
from fastapi.responses import JSONResponse
from typing import Optional , List
from .schemas import Usercreatemodel , UserModel , User_login_model
from src.db.main import get_session
from .service import Userservice
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token , decode_token , verify_password
from datetime import timedelta , datetime
from .dependancies import RefreshTokenBearer , AccessTokenBearer , get_current_user
from src.db.redis_config import add_JTI_to_Blocklist
from .models import User

auth_routes=APIRouter()
User_service=Userservice()

REFRESH_TOKEN_EXPIRY=2

@auth_routes.get("/serverside",response_model=list[str],status_code=status.HTTP_200_OK)
async def get_all_acc(session:AsyncSession = Depends(get_session)):
    return await User_service.get_all_accounts_usernames(session)

@auth_routes.post("/signup",response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def create_user_Account(userdata: Usercreatemodel , session : AsyncSession = Depends(get_session)):
    email=userdata.email
    username=userdata.username
    user_existance = await User_service.user_exist_by_email(email,session)
    if user_existance is True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user email already exists")
    user_existance = await User_service.user_exist_by_username(username,session)
    if user_existance is True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user username already exists")
    return await User_service.create_user(userdata,session)

@auth_routes.get("/email/{email}",response_model=UserModel,status_code=status.HTTP_200_OK)
async def get_user(email:str , session : AsyncSession = Depends(get_session)):
    User_by_email=await User_service.get_user_by_email(email,session)
    if User_by_email is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with email does not exist")
    return User_by_email

@auth_routes.delete("/delete_account",response_model=UserModel,status_code=status.HTTP_200_OK)
async def delete_acc(email : Optional[str] = Query(None) , username : Optional[str] = Query(None), session : AsyncSession = Depends(get_session)):

    if email is None and username is None :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="please either provide email or username")
    
    if email is not None and username is not None:
        user = await User_service.get_user_by_email(email,session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with email does not exist.")
        
        if user.username != username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username does not match the provided email.")
        
        await session.delete(user)
        await session.commit()
        return user
    
    if email is not None :
        deleted_user= await User_service.delete_user_by_email(email,session)
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with email does not exist")
        return deleted_user
    
    if username is not None :
        deleted_user= await User_service.delete_user_by_username(username,session)
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with username does not exist")
        return deleted_user
    
@auth_routes.post('/login')
async def login_user(userdata : User_login_model, session : AsyncSession = Depends(get_session)):
    email = userdata.email
    password= userdata.password
    user= await User_service.get_user_by_email(email,session)
    if user :
        password_hash=user.Password_hash
        password_valid=verify_password(password=password,hash=password_hash)
        if password_valid :
            userdata={}
            userdata['email']=user.email
            userdata['uid']=str(user.uid)
            userdata['role']=user.role
            access_token = create_access_token(
                userdata=userdata
            )

            refresh_token = create_access_token(
                userdata=userdata,
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "LOGGED IN SUCCESSFULLY",
                    "ACCESS_TOKEN" : access_token,
                    "REFRESH_TOKEN" : refresh_token,
                    'userdata' : userdata
                }
            )
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Password And Email")

@auth_routes.post("/refresh_token")
async def get_new_access_token(token_details : dict = Depends(RefreshTokenBearer())):
    expiry_timestamp= token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(userdata=token_details['user'])
        return JSONResponse(
            content={
                "access_token" : new_access_token
            }
        )
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="token expired")
@auth_routes.get("/me")
async def get_about_info(user :User= Depends(get_current_user)):
    return user

@auth_routes.get("/logout")
async def revoke_token(token_details : dict = Depends(AccessTokenBearer())):
    jti=token_details['jti']
    await add_JTI_to_Blocklist(jti=jti)
    return JSONResponse(
        content={
            "message" : "LOGGED OUT SUCCESSFULLY"
        },
        status_code=status.HTTP_200_OK
    )

        