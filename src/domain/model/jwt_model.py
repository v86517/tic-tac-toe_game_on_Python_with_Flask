import base64

class JwtRequest():
    def __init__(self, login = "noname", password = "password"):
        self.login = login
        self.password = base64.b64encode(password.encode())

class JwtResponse():
    def __init__(self, accessToken = None, refreshToken = None):
        self.accessToken = accessToken
        self.refreshToken = refreshToken

class RefreshJwtRequest():
    def __init__(self, refreshToken = None):
        self.refreshToken = refreshToken