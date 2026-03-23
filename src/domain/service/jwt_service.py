from flask_jwt_extended import create_access_token, create_refresh_token, decode_token, verify_jwt_in_request
from flask import jsonify, request
from datetime import timedelta
from functools import wraps
import json


class JwtProvider():
    def generate_access_token(self, uuid_user: str, login_user: str):
        access_token = create_access_token(identity=str({"uuid_user": uuid_user, "login_user": login_user}), expires_delta=timedelta(hours=1))
        return access_token

    def generate_refresh_token(self, uuid_user: str, login_user: str):
        refresh_token = create_refresh_token(identity=str({"uuid_user": uuid_user, "login_user": login_user}), expires_delta=timedelta(days=30))
        return refresh_token

    def validate_access_token():
        def wrapper(f):
            @wraps(f)
            def decorator(*args, **kwargs):
                token = None
                if 'Authorization' in request.headers:
                    token = request.headers['Authorization']

                if not token:
                    return jsonify({'error': 'Token is missing !!'}), 402

                try:
                    token_value = token.split(" ")[1]
                    decode_token(token_value)
                    verify_jwt_in_request()
                    return f(*args, **kwargs)
                except Exception as e:
                    print(e)
                    return jsonify({'error': 'Token is invalid !!'}), 403

            return decorator

        return wrapper

    def validate_refresh_token(self, refresh_token):
        try:
            decode_token(refresh_token)
            return True
        except Exception as e:
            return False

    def get_uuid_from_token(self, token):
        decoded = decode_token(token)

        data_token = json.loads(decoded["sub"].replace("'", '"'))

        return data_token["uuid_user"]