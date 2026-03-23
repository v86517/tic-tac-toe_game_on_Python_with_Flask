from abc import ABC, abstractmethod


class InterfaceService(ABC):

    @abstractmethod
    def make_move(self, id_user, id_game, i, j):
        pass

    @abstractmethod
    def get_game_state(self, id_game):
        pass
