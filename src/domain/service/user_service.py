from abc import ABC, abstractmethod


class UserService(ABC):

    @abstractmethod
    def registration(self, sign_up_request):
        pass

    @abstractmethod
    def authorization(self, login_password):
        pass