from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash

from src.ext.database import db
from src.models import User


def verify_login(user):
    """Valida o usuario e senha para efetuar o login"""
    username = user.get("username")
    password = str(user.get("password")).strip()

    print(f"A senha é: {password}")

    if not username or not password:
        return False
    existing_user = User.query.filter_by(username=username).first()

    if not existing_user:
        return False
    if check_password_hash(existing_user.password, password):
        print("Deu bom!")

        return True
    else:
        print("Deu ruim!")

        return False


def verify_permission(user, uri):
    existing_user = User.query.filter_by(username=user).first()
    if existing_user.signature is None:
        return False

    print(f"A URI É {uri} e o acesso é {existing_user.signature}")

    if existing_user and (
        existing_user.signature in uri
        or existing_user.signature == "full"
        or existing_user.signature == "admin"
        or (
            existing_user.signature == "freemium"
            and ("maps" in uri)
        )
    ):
        
        print("teste verify")
        return True

    else:
        print("teste falso")
        return False


def seach_signature(user):
    existing_user = User.query.filter_by(username=user).first()

    if existing_user:
        return existing_user.signature

    else:
        return False


def create_user(username, password):
    """Registra um novo usuario caso nao esteja cadastrado"""

    username = str(username).strip()
    password = str(password).strip()

    if User.query.filter_by(username=username).first():
        return "Usuário existente"
    user = User(
        username=username,
        password=generate_password_hash(password),
        signature="freemium",
    )
    db.session.add(user)
    db.session.commit()
    return "Usuário cadastrado com sucesso!"


def init_app(app):
    SimpleLogin(app, login_checker=verify_login)
