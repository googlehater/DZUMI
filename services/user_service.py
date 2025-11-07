from fastapi import Depends, HTTPException, status
from dto.user_dto import UserDto, ChangeFirstNameDto,ChangeRoleDto
from dao.users_dao import UserDAO
import dependencies

class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    async def create_user(user_dto: UserDto, user_dao: UserDAO):
        new_user = user_dao.create(user_dto)
        return new_user
    
    async def change_first_name(change_role_dto: ChangeFirstNameDto, user_dao: UserDAO):
        new_first_name = user_dao.update(change_role_dto.new_first_name)
        return new_first_name
    
    async def change_phone_number(user_dto: UserDto, user_dao: UserDAO):
        new_phone_number = user_dao.update(user_dto.phone_number)
        return new_phone_number
    
    async def change_email(user_dto: UserDto, user_dao: UserDAO):
        new_email = user_dao.update(user_dto.email)
        return new_email
    
    async def change_role(change_role_dto: ChangeRoleDto, user_dao: UserDAO, current_user_id: int): # тут поправть условие на то как макс говорил
        
        current_user = user_dao.get_by_id(current_user_id)


        
        if current_user.role_id != "Начальник":  # != "Начальник" - хз какой id дать начальнику!
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Недостаточно прав для изменения ролей")
