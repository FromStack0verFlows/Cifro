import hmac
import json
import hashlib
import logging
import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple
from time import mktime


class ABCToken(ABC):
    """
    JSON Web Token – это открытый стандарт (RFC 7519), который определяет компактный и
    автономный способ безопасной передачи информации между сторонами в виде объекта JSON.
    -------------------------------------------------------------------------------------

    Доступные методы:

    encode_token(identifier: str) -> bytes
    -------------------------------------------------------------------------------------
        Метод создания токена на основе индентификатора пользователя.
        Идентификатор "identifier" присваивается пользователю при регистрации аккаунта

    decode_token(auth_token: str) -> str
    ------------------------------------------------------------------------------
        Метод проверки токена на целостность компонентов и его верификация.

    refresh_token() -> Bool
    ------------------------------------------------------------------------------
    """

    @abstractmethod
    def encode_token(self, identifier: str) -> None:
        pass

    @abstractmethod
    def decode_token(self, auth_token: str) -> None:
        pass

    @abstractmethod
    def refresh_token(self, auth_token: str) -> None:
        pass


class Components:
    def __init__(self, auth_token: str):
        try:
            self.header, self.payload, self.verifier_sig = auth_token.encode('utf-8').rsplit(b'.', 2)
        except ValueError:
            logging.error(f'Decode error {auth_token}\n')

    def verify(self, passphrase: bytes) -> bool:
        timestamp = mktime(datetime.now().timetuple())

        try:
            payload_obj = urlsafe_b64decode(self.payload + b"===").decode('utf-8')
            expire_timestamp = json.loads(payload_obj).get("exp")
        except (TypeError, ValueError, binascii.Error) as error:
            logging.error(f'Invalid expire timestamp value\n{error}')
            return False

        try:
            sig_hs512 = hmac.new(passphrase, self.header + b"." + self.payload, hashlib.sha512).digest()
            signature = urlsafe_b64encode(sig_hs512).replace(b"=", b"")
        except (TypeError, ValueError, binascii.Error):
            logging.error(f'Invalid signature')
            return False

        return self.verifier_sig == signature and timestamp > expire_timestamp


class Token(ABCToken):
    __secret = b"hello"
    __header = {"typ": "JWT", "alg": "HS512"}
    __payload = {"sub": "auth", "exp": None, "iat": None, "jti": None}

    def encode_token(self, identifier="0") -> bytes:
        issued = mktime(datetime.now().timetuple())
        expire = mktime((datetime.fromtimestamp(issued) + timedelta(days=30)).timetuple())
        self.__payload["jti"], self.__payload["exp"], self.__payload["iat"] = expire, issued, identifier
        header_b64, payload_b64 = self.__base64_encode()
        hs512signature = hmac.new(self.__secret, header_b64 + b"." + payload_b64, hashlib.sha512).digest()
        return b".".join([header_b64, payload_b64, urlsafe_b64encode(hs512signature).replace(b'=', b'')])

    def decode_token(self, auth_token: str) -> str:
        components = Components(auth_token=auth_token)
        if components.verify(passphrase=self.__secret):
            return json.loads(urlsafe_b64decode(components.payload + b'===').decode('utf-8')).get("iat")

    def refresh_token(self, token):
        pass

    def __base64_encode(self) -> Tuple[bytes, bytes]:
        header = json.dumps(self.__header, separators=(',', ':')).encode("utf-8")
        payload = json.dumps(self.__payload, separators=(',', ':')).encode("utf-8")
        return urlsafe_b64encode(header).replace(b'=', b''), urlsafe_b64encode(payload).replace(b'=', b'')