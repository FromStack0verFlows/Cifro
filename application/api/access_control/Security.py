import hashlib
from typing import Tuple
from .Token import Token


class Security:

    @staticmethod
    def create_hash(password: str) -> Tuple[bytes, bytes]:
        """ PBKDF2 стандарт формирования ключа на основе пароля (* Wiki)
            В Российской Федерации использование функции PBKDF2 регламентируется рекомендациями
            по стандартизации  Р 50.1.111-2016 "Парольная защита ключевой информации".
            В качестве псевдослучайной функции мы будем использовать sha512 c 200 000 итерациями.
        """
        salt = b'\x83?\xd1\x19\x11\xf4\x8a\xc5\xc9Ct\xa7x\xd4\x846oo{d\\\x83\x87\xd1 \x97\x88\x05\xfe\xf8E\xc9'
        return salt, hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 200000)

    @staticmethod
    def verify_hash(user, auth_pass: str) -> bool:
        return hashlib.pbkdf2_hmac('sha512', auth_pass.encode('utf-8'), user.salt, 200000) == user.password

    token = Token()
