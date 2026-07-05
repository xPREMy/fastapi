from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemas import Usercreatemodel
from sqlmodel import select ,desc
from .utils import generate_passwd_hash

class Userservice:
    async def get_user_by_email(self,email: str , session : AsyncSession):
        statement = select(User).where(User.email==email)
        result= await session.exec(statement=statement)
        user= result.first()
        return user
    
    async def get_user_by_username(self,username: str , session : AsyncSession):
        statement = select(User).where(User.username==username)
        result= await session.exec(statement=statement)
        user= result.first()
        return user

    async def user_exist_by_email(self,email: str , session : AsyncSession):
        user=await self.get_user_by_email(email,session)
        return True if user is not None else False      
    
    async def user_exist_by_username(self,username: str , session : AsyncSession):
        user=await self.get_user_by_username(username,session)
        return True if user is not None else False

    async def create_user(self,userdata: Usercreatemodel, session: AsyncSession):
        user_data_dict=userdata.model_dump()
        new_user= User(
            **user_data_dict
        )
        new_user.Password_hash=generate_passwd_hash(user_data_dict['password'])
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    async def delete_user_by_email(self,email : str, session : AsyncSession):
        user_to_delete=await self.get_user_by_email(email,session)
        if user_to_delete is not None:
            await session.delete(user_to_delete)
            await session.commit()
            return user_to_delete
        return None
    
    async def delete_user_by_username(self,username : str, session : AsyncSession):
        user_to_delete=await self.get_user_by_username(username,session)
        if user_to_delete is not None:
            await session.delete(user_to_delete)
            await session.commit()
            return user_to_delete
        return None