from src.datasource.repository.ds_repository import Repository
from src.datasource.service.ds_game_service import Service
from src.datasource.service.ds_auth_service import AuthService


class Container:
    def __init__(self):
        self.repository = Repository()
        self.service = Service(self.repository)
        self.authorization_service = AuthService(self.repository)
