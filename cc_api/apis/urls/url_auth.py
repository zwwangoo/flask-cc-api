from .. import ctrl_auth

urls = [
    '/auth/login', ctrl_auth.UserLoginHandler,
    '/auth/token/refrech', ctrl_auth.UserTokenRefrech
]
