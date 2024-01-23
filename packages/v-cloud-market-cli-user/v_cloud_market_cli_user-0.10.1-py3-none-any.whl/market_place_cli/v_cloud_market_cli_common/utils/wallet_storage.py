import os
import json
from collections import namedtuple
from .vsyschain.error import throw_error
from .service_error import (
    WalletStorageLoadingException,
    WalletStorageSavingException)

WalletData = namedtuple("WalletData", ["seed", "nonce", "agent"])

def get_cache_file_path(file_name):
    home_path = os.path.expanduser("~")
    cache_dir = os.path.join(home_path, '.vcloud')
    if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    file_path = os.path.join(cache_dir, file_name)
    return file_path

class WalletStorage:

    def __init__(self, path = None):
        self.path = path

    def save(self, wallet_data, cipher=None):
        """
        :param wallet_data: a json dict
        :param cipher: an instance of cipher class for encrypting json data
        :return: None
        """
        try:
            parentPath = os.path.dirname(self.path)
            if not os.path.exists(parentPath):
                os.mkdir(parentPath)
            data = json.dumps(wallet_data._asdict())
            with open(self.path, "w") as wallet:
                if cipher:
                    wallet.write(cipher.encrypt(data))
                else:
                    wallet.write(data)
        except:
            msg = "Failed to save information to wallet file."
            throw_error(msg, WalletStorageSavingException)

    def load(self, cipher=None):
        """
        :param cipher: an instance of cipher class, default: None
        :param show_err: not show error message when used to judge if wallet has password, default: True
        :return: a json dict, walletData, with keys: seed, accountSeeds, nonce, agent
        """
        try:
            with open(self.path, "r") as wallet:
                data = wallet.read()
                # cannot open wallet saved as plain text with cipher
                if cipher:
                    plain_data = cipher.decrypt(data)
                    return json.loads(plain_data, object_hook=self._wallet_data_decoder)
                else:
                    return json.loads(data, object_hook=self._wallet_data_decoder)
        except FileNotFoundError as e:
            return None
        except:
            pass

    def _wallet_data_decoder(self, walletDict):
        return namedtuple("WalletData", walletDict.keys())(*walletDict.values())

    def is_json(self,input):
        try:
            json.load(input)
            return True
        except:
            return False
