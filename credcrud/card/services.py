import os
from base64 import b64decode, b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption

from credcrud.card.repositories import CardRepository
from credcrud.card.schemas import Card as CardSchema
from credcrud.card.schemas import CardPayload
from credcrud.database import db_session as default_db_session


class RSAService:
    def _persist_private_key_to_text(self, passwd):
        return self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=BestAvailableEncryption(passwd.encode()),
        ).decode("utf-8")

    def _generate_private_key(self, passwd):
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.private_key_as_text = self._persist_private_key_to_text(passwd)

    def _load_private_key(self, private_key_as_text, passwd):
        key_bytes = private_key_as_text.encode("utf-8")
        self._private_key = serialization.load_pem_private_key(
            key_bytes, password=passwd.encode(), backend=default_backend()
        )
        self.private_key_as_text = private_key_as_text

    def __init__(self, private_key_passwd, private_key_as_text: str = None):
        # Reference of private key
        self._private_key = None
        self.private_key_as_text = None

        if private_key_as_text:
            self._load_private_key(private_key_as_text, private_key_passwd)
        else:
            self._generate_private_key(private_key_passwd)

    def encrypt(self, content: str) -> str:
        return b64encode(
            self._private_key.public_key().encrypt(
                content.encode("utf-8"),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        ).decode("utf-8")

    def decrypt(self, encrypted_content: str) -> str:
        encrypted_message_bytes = b64decode(encrypted_content)

        decrypted_message = self._private_key.decrypt(
            encrypted_message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return decrypted_message.decode("utf-8")


class RSABuilder:
    _rsa: RSAService

    def _load_key_from_file(self):
        with open(self._key_file, "r") as file_handler:
            return file_handler.read()

    def _write_key_to_file(self):
        with open(self._key_file, "w") as file_handler:
            return file_handler.write(self._rsa.private_key_as_text)

    def get_rsa_service(self):
        return self._rsa

    def __init__(self):
        passwd = os.environ.get("RSA_KEY_PASSWORD", "MYPASSWORD")
        self._key_file = "_data/project_private_key.pem"

        if os.path.isfile(self._key_file):
            self._rsa = RSAService(
                private_key_passwd=passwd,
                private_key_as_text=self._load_key_from_file(),
            )
        else:
            self._rsa = RSAService(private_key_passwd=passwd)
            self._write_key_to_file()


class CardService:
    def __init__(self, db_session=default_db_session):
        self._repository: CardRepository = CardRepository(db_session)
        self._rsa: RSAService = RSABuilder().get_rsa_service()

    def create(self, card_payload: CardPayload):
        card_model = CardSchema.from_payload(card_payload).to_model(
            rsa_service=self._rsa
        )
        return CardSchema.from_model(
            self._repository.create(card_model), rsa_service=self._rsa
        )

    def get_by_id(self, id: str):
        card_model = self._repository.get_by_id(id)
        return CardSchema.from_model(card_model, rsa_service=self._rsa)

    def get_all(self):
        all_cards = self._repository.get_all()
        return (
            CardSchema.from_model(card, rsa_service=self._rsa) for card in all_cards
        )

    def delete(self, id: str):
        self._repository.delete(self._repository.get_by_id(id))
        return True
