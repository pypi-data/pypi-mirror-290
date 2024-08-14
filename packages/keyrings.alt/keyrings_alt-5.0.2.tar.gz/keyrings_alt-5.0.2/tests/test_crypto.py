import getpass
from unittest import mock

import pytest

from keyrings.alt import file

from .test_file import FileKeyringTests


def is_crypto_supported():
    try:
        __import__('Cryptodome.Cipher.AES')
        __import__('Cryptodome.Protocol.KDF')
        __import__('Cryptodome.Random')
    except ImportError:
        try:
            __import__('Crypto.Cipher.AES')
            __import__('Crypto.Protocol.KDF')
            __import__('Crypto.Random')
        except ImportError:
            return False
    return True


@pytest.mark.skipif(not is_crypto_supported(), reason="Need pycryptodomex module")
class TestCryptedFileKeyring(FileKeyringTests):
    @pytest.fixture(autouse=True)
    def mocked_getpass(self, monkeypatch):
        fake_getpass = mock.Mock(return_value='abcdef')
        monkeypatch.setattr(getpass, 'getpass', fake_getpass)

    def init_keyring(self):
        return file.EncryptedKeyring()
