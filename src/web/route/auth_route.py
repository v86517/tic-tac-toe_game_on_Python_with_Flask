from flask import Blueprint, redirect, url_for, render_template, request, current_app, jsonify

from src.domain.model.jwt_model import JwtRequest
from src.domain.model.jwt_model import RefreshJwtRequest

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        auth_service = current_app.config["container"].authorization_service
        username = request.json.get("login", None)
        password = request.json.get("password", None)
        jwt_request = JwtRequest(username, password)

        jwt_response = auth_service.authorization(jwt_request)

        if jwt_response.accessToken is not None and jwt_response.refreshToken is not None:
            return jsonify(message="login successful", accessToken=jwt_response.accessToken,
                           refreshToken=jwt_response.refreshToken), 200
        else:
            return jsonify({"error": "login failed"}), 401

    return render_template('login.html')


@auth.route('/sign_up', methods=['post', 'get'])
def sign_up():
    if request.method == 'POST':
        auth_service = current_app.config["container"].authorization_service
        username = request.json.get("login", None)
        password = request.json.get("password", None)
        jwt_request = JwtRequest(username, password)

        result_request = auth_service.registration(jwt_request)
        if result_request:
            jwt_response = auth_service.authorization(jwt_request)
            return jsonify(message="sign up successful", accessToken=jwt_response.accessToken,
                           refreshToken=jwt_response.refreshToken), 200
        else:
            return jsonify({"error": "A user with this login already exists."}), 401

    return render_template('signup.html')


@auth.route('/refresh_access_token/<refresh_token>')
def refresh_access_token(refresh_token):
    auth_service = current_app.config["container"].authorization_service

    new_refresh_jwt_request = RefreshJwtRequest(refresh_token)

    jwt_response = auth_service.refresh_access_token(new_refresh_jwt_request)

    return jsonify(message="successful", accessToken=jwt_response.accessToken,
                   refreshToken=jwt_response.refreshToken), 200


@auth.route('/refresh_refresh_token/<refresh_token>')
def refresh_refresh_token(refresh_token):
    auth_service = current_app.config["container"].authorization_service

    new_refresh_jwt_request = RefreshJwtRequest(refresh_token)

    jwt_response = auth_service.refresh_refresh_token(new_refresh_jwt_request)

    return jsonify(message="successful", accessToken=jwt_response.accessToken,
                   refreshToken=jwt_response.refreshToken), 200
