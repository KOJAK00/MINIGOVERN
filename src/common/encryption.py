from cryptography.fernet import Fernet
from src.config import Config

fernet = Fernet(Config.ENCRYPTION_KEY.encode())


def encrypt_password(password: str) -> str:
    return fernet.encrypt(
        password.encode()
    ).decode()


def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(
        encrypted_password.encode()
    ).decode()