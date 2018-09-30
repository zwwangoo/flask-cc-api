from .. import auth_ctrl

urls = [
    '/auth/login', auth_ctrl.UserLoginHandler,
    '/auth/token/refrech', auth_ctrl.UserTokenRefrech
]
