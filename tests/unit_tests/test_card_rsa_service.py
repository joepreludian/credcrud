import os
from unittest import mock

import pytest

from credcrud.card.services import RSABuilder, RSAService


class TestRSABuilder:
    @staticmethod
    def setup_method(cls):
        os.environ['RSA_KEY_PASSWORD'] = "MYPASSWORD"

    @pytest.mark.parametrize(('key_file_exists',), (
            (True, ), (False, )
    ))
    def test_get_rsa_service_from_first_time(self, key_file_exists, rsa_private_key_as_text_1024):
        with mock.patch("builtins.open", mock.mock_open(read_data=rsa_private_key_as_text_1024)), mock.patch("os.path.isfile", return_value=key_file_exists):
            kr = RSABuilder()
            assert type(kr.get_rsa_service()) is RSAService


class TestRSAService:
    def test_init_service(self):
        rsa = RSAService(private_key_passwd="MYPASSWORD")

        assert "-BEGIN ENCRYPTED PRIVATE KEY-" in rsa.private_key_as_text
        assert "-END ENCRYPTED PRIVATE KEY-" in rsa.private_key_as_text

    def test_init_service_by_private_key_text_and_password(self, rsa_private_key_as_text_1024):
        rsa = RSAService(private_key_passwd="MYPASSWORD", private_key_as_text=rsa_private_key_as_text_1024)
        assert rsa.private_key_as_text == rsa_private_key_as_text_1024

    def test_init_service_by_private_key_text_and_wrong_password(self, rsa_private_key_as_text_1024):
        with pytest.raises(ValueError) as exception:
            RSAService(private_key_passwd="MY_WRONG_PASSWORD", private_key_as_text=rsa_private_key_as_text_1024)

        assert exception.value.args[0] == "Bad decrypt. Incorrect password?"

    def test_encryption(self, rsa_text_decrypted_example):
        rsa = RSAService(private_key_passwd="MYPASSWORD")
        output = rsa.encrypt(content="MY SECRET MESSAGE")

        assert type(output) is str
        assert len(output) > 0

    def test_encrypt_with_known_rsa_key(self, rsa_private_key_as_text_1024,
                                        rsa_text_decrypted_example,
                                        rsa_text_encrypted_example):
        """In this case, due to the nature of encryption padding OAEP,
        it's expected that the encoded text has always a different encrypted value each time it runs"""

        rsa = RSAService(private_key_passwd="MYPASSWORD", private_key_as_text=rsa_private_key_as_text_1024)
        output = rsa.encrypt(rsa_text_decrypted_example)

        assert type(output) is str
        assert len(output) > 0
        assert output != rsa_text_encrypted_example

    def test_decrypt_with_known_rsa_key(self, rsa_private_key_as_text_1024,
                                        rsa_text_decrypted_example,
                                        rsa_text_encrypted_example):

        rsa = RSAService(private_key_passwd="MYPASSWORD",
                         private_key_as_text=rsa_private_key_as_text_1024)

        output = rsa.decrypt(rsa_text_encrypted_example)

        assert output == rsa_text_decrypted_example
