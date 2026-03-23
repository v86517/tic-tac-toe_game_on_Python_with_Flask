from flask import Blueprint, render_template, request, current_app, jsonify

from flask_jwt_extended import get_jwt_identity
import json
import uuid

from src.config import CROSS, NOUGHT
from src.web.mapper.web_mapper import WebMapper
from src.datasource.service.ds_auth_service import AuthService

game_view = Blueprint('game_view', __name__)


@game_view.route('/get_user_uuid')
@AuthService.validate_access_token()
def get_user_uuid():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    return jsonify(uuid_user=jwt_identity["uuid_user"], login_user=jwt_identity["login_user"]), 200

@game_view.route('/list_games')
def list_games():
    return render_template('list_games.html')


@game_view.route('/get_list_games', methods=['get'])
@AuthService.validate_access_token()
def get_list_games():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])

    service = current_app.config["container"].service

    result = service.get_started_ds_games_by_uuid_user(uuid_user)

    return jsonify(list_games=result), 200

@game_view.route('/game/<uuid_game>', methods=["GET"])
def game(uuid_game):
    uuid_game = uuid.UUID(uuid_game)
    service = current_app.config["container"].service
    game_state = service.get_game_state(uuid_game)

    if game_state in ["waiting players", "move X", "move O"]:
        return render_template('game.html')
    else:
        return render_template('end_game.html', result_game=game_state)

@game_view.route('/get_winner/<uuid_game>', methods=["GET"])
@AuthService.validate_access_token()
def get_winner(uuid_game):
    uuid_game = uuid.UUID(uuid_game)
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service
    game_model = service.get_game(uuid_game)
    web_game_model = WebMapper.game_to_web_game(game_model)
    web_game_model.web_game_board = web_game_model.web_game_board.__dict__

    if web_game_model.web_game_state == 'draw':
        service.add_count_draw(uuid_user)
        result = web_game_model.web_game_state
    else:
        if web_game_model.web_game_creator.web_user_uuid == uuid_user:
            if web_game_model.web_game_creator_x_or_y in web_game_model.web_game_state:
                service.add_count_wins(game_model.game_creator.user_uuid)
                result = 'True'
            else:
                service.add_count_lose(game_model.game_creator.user_uuid)
                result = 'False'
        else:
            if web_game_model.web_game_creator_x_or_y not in web_game_model.web_game_state:
                service.add_count_wins(game_model.game_enemy.user_uuid)
                result = 'True'
            else:
                service.add_count_lose(game_model.game_enemy.user_uuid)
                result = 'False'
    return jsonify({"game": web_game_model.web_game_board, "winner": result}), 200

@game_view.route('/game_info/<uuid_game>', methods=['get', 'post'])
@AuthService.validate_access_token()
def game_info(uuid_game):
    uuid_game = uuid.UUID(uuid_game)
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service

    if request.method == "POST":
        i = request.json.get("i", None)
        j = request.json.get("j", None)

        if i is None or j is None:
            return jsonify({"error": "Invalid move"}), 400

        service.make_move(uuid_user, uuid_game, i, j)

        return jsonify({"result": "OK"}), 200

    game_model = service.get_game(uuid_game)
    web_game_model = WebMapper.game_to_web_game(game_model)

    if web_game_model.web_game_creator.web_user_uuid == uuid_user:
        icon_user = web_game_model.web_game_creator_x_or_y
    else:
        icon_user = CROSS if web_game_model.web_game_creator_x_or_y == NOUGHT else NOUGHT

    if web_game_model.web_game_enemy is not None:
        web_game_model.web_game_enemy.web_user_password = ""
        web_game_model.web_game_enemy = web_game_model.web_game_enemy.__dict__
    web_game_model.web_game_board = web_game_model.web_game_board.__dict__
    web_game_model.web_game_creator.web_user_password = ""
    web_game_model.web_game_creator = web_game_model.web_game_creator.__dict__
    return jsonify({"game": web_game_model.__dict__, "type_player": icon_user}), 200


@game_view.route('/join_game/<uuid_game>')
@AuthService.validate_access_token()
def join_game(uuid_game):
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service

    result_join = service.join_to_game(uuid_user, uuid_game)

    if result_join:
        return jsonify({"new_url": "/game/" + uuid_game}), 200
    else:
        return jsonify({"new_url": "/list_games"}), 200


@game_view.route('/new_game')
def new_game():
    return render_template('new_game.html')

@game_view.route('/create_new_game/<two_players>')
@AuthService.validate_access_token()
def create_new_game(two_players):
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service

    bool_two_players = False

    if two_players.lower() == 'true':
        bool_two_players = True

    new_id_game = service.create_game(uuid_user, bool_two_players)

    if new_id_game:
        return jsonify({"new_url": "/game/" + str(new_id_game)}), 200
    else:
        return jsonify({"new_url": "/list_games"}), 200


@game_view.route('/profile/<uuid_user>')
def profile(uuid_user):
    print('******', uuid_user)
    return render_template('profile.html', uuid_user=uuid_user)


@game_view.route('/profile_info/<uuid_user>')
@AuthService.validate_access_token()
def profile_info(uuid_user):
    service = current_app.config["container"].service
    #print('******', uuid_user)
    user = service.get_user(uuid_user)
    web_user = WebMapper.user_to_web_user(user)
    web_user.web_user_password = ""
    return jsonify({"user_info": web_user.__dict__}), 200


@game_view.route('/history_games')
def history_games():
    return render_template('history_games.html')


@game_view.route('/get_history_games')
@AuthService.validate_access_token()
def get_history_games():
    jwt_identity = json.loads(get_jwt_identity().replace("'", '"'))
    uuid_user = uuid.UUID(jwt_identity["uuid_user"])
    service = current_app.config["container"].service
    result = service.get_finished_ds_games_by_uuid_user(uuid_user)
    return jsonify(list_games=result), 200


@game_view.route('/list_leaders')
def list_leaders():
    return render_template('list_leaders.html')


@game_view.route('/get_leaders_list')
@AuthService.validate_access_token()
def get_leaders_list():
    service = current_app.config["container"].service
    result = service.get_ds_users_leaders_list()
    return jsonify(list_leaders=result), 200