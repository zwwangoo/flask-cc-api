from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import get_jwt_identity


def verify_hash(password, user_password):
    password_hash = generate_hash(user_password)
    return sha256.verify(password, password_hash)


def generate_hash(password):
    return sha256.hash(password)


def get_user_id():
    return get_jwt_identity()
