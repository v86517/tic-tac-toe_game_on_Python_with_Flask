from src.domain.service.user_service import UserService
from src.domain.service.jwt_service import JwtProvider
from src.domain.model.jwt_model import JwtResponse
from src.domain.model.jwt_model import RefreshJwtRequest
from src.datasource.model.ds_model import UsersTable
from src.datasource.mapper.ds_mapper import DataMapper
import uuid


class AuthService(UserService, JwtProvider):
    def __init__(self, repository):
        self.repository = repository

    def registration(self, sign_up_request):
        new_user = UsersTable(ds_user_uuid=uuid.uuid4(),
                              ds_user_login=sign_up_request.login,
                              ds_user_password=sign_up_request.password,
                              ds_user_count_games=0,
                              ds_user_count_wins=0,
                              ds_user_count_lose=0,
                              ds_user_count_draw=0)

        result = self.repository.add_ds_user(new_user)
        return result

    def authorization(self, jwt_request):
        new_accessToken = None
        new_refreshToken = None

        user = self.repository.get_ds_user_by_login_user(jwt_request.login)
        if user is not None and user.ds_user_password == jwt_request.password:
            new_accessToken = self.generate_access_token(str(user.ds_user_uuid), str(user.ds_user_login))
            new_refreshToken = self.generate_refresh_token(str(user.ds_user_uuid), str(user.ds_user_login))

        result = JwtResponse(new_accessToken, new_refreshToken)
        return result

    def get_user_by_uuid_user(self, uuid_user):
        return DataMapper.ds_user_to_user(self.repository.get_ds_user_by_uuid_user(uuid_user))

    def get_user_by_login_user(self, login_user):
        return DataMapper.ds_user_to_user(self.repository.get_ds_user_by_login_user(login_user))

    def refresh_access_token(self, refresh_request: RefreshJwtRequest):
        if not self.validate_refresh_token(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        uuid_user = self.get_uuid_from_token(refresh_request.refreshToken)

        user = self.get_user_by_uuid_user(uuid_user)

        if not user:
            raise ValueError("User not found")

        new_access_token = self.generate_access_token(str(user.user_uuid), str(user.user_login))
        result = JwtResponse(new_access_token, refresh_request.refreshToken)
        return result

    def refresh_refresh_token(self, refresh_request: RefreshJwtRequest):
        if not self.validate_refresh_token(refresh_request.refreshToken):
            raise ValueError("Invalid refresh token")
        uuid_user = self.get_uuid_from_token(refresh_request.refreshToken)

        user = self.get_user_by_uuid_user(uuid_user)

        if not user:
            raise ValueError("User not found")

        new_refresh_token = self.generate_refresh_token(str(user.user_uuid), str(user.user_login))
        new_access_token = self.generate_access_token(str(user.user_uuid), str(user.user_login))
        result = JwtResponse(new_access_token, new_refresh_token)
        return result
