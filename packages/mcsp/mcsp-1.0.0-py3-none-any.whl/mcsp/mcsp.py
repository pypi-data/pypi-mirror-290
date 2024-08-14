import os
import json
import base64
from cryptography.fernet import Fernet
from datetime import datetime
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class EPC:
    """Encrypt Package Class"""
    def __init__(self, exts=['.txt', '.py', '.ipynb', '.json', '.bat', '.reg', '.html', '.log']):
        load_dotenv()
        self.exts = exts
        self.fernet = Fernet(self._get_key(os.environ['FKEY']))
        self.akey = self._get_key(os.environ['AKEY'])

    def _get_key(self, encoded_key):
        return base64.b64decode(encoded_key)

    def _is_valid_ext(self, path_file):
        return sum([path_file.endswith(ext) for ext in self.exts]) > 0

    def _get_merged_text(self, path_project):
        merged_text = ''
        for path_file_hierarchy in os.walk(path_project):
            if sum([False if dir_name == '..' else dir_name.startswith('.') for dir_name in path_file_hierarchy[0].split(os.path.sep)]) == 0:
                grabbed_file = [path_file for path_file in path_file_hierarchy[2] if self._is_valid_ext(path_file)]
                if len(grabbed_file) > 0:
                    for file_name in grabbed_file:
                        path_file = os.path.join(path_file_hierarchy[0], file_name)
                        
                        merged_text += f'## CS : {path_file}\n'
                        if path_file.endswith('.ipynb'):
                            with open(path_file, encoding='utf-8') as f:
                                ipy = json.load(f)
    
                            merged_text += '\n\n'.join([''.join(cell['source']) for cell in ipy['cells']])
                        else:
                            with open(path_file, encoding='utf-8') as fr:
                                merged_text += fr.read()
                            
                        merged_text += '\n\n'

        return merged_text.encode('utf-8')
    
    def _shuffle(self, plain_text):
        enc = [44, 59, 73, 6, 26, 68, 32, 95, 36, 80, 41, 33, 23, 18, 16, 89, 48, 75, 53, 62, 24, 5, 90, 65, 11, 77, 87, 50, 82, 17, 54, 13, 76, 93, 61, 35, 30, 43, 31, 15, 86, 51, 84, 29, 19, 71, 56, 3, 46, 78, 27, 79, 83, 74, 7, 25, 70, 64, 98, 47, 38, 63, 42, 12, 91, 21, 81, 10, 67, 2, 4, 99, 39, 49, 14, 22, 37, 94, 96, 69, 60, 20, 92, 1, 55, 58, 34, 28, 0, 9, 52, 57, 66, 88, 97, 8, 40, 45, 85, 72]
        partitions = len(enc)
        stride = len(plain_text)//partitions
        remains = len(plain_text)%stride
        if remains > 0:
            last_text = plain_text[-remains:]
        else:
            last_text = b''
        
        splitted_text = [plain_text[stride*i:stride*(i+1)] for i in range(partitions)]
        shuffled_text = b''.join([splitted_text[ei] for ei in enc])+last_text

        return shuffled_text
    
    def enc(self, path_project):
        postfix = datetime.today().strftime('%Y%m%d%H%M%S')
        text = self._get_merged_text(path_project)
        encrypted_F = self.fernet.encrypt(text)
        encrypted_F_corrupted = b'\x00\xFF\x00\xFF' + encrypted_F

        cipher = AES.new(self.akey, AES.MODE_CBC)
        encrypted_A_corrupted_encrypted_F = cipher.encrypt(pad(encrypted_F_corrupted, AES.block_size))

        shuffled_encrypted_A_corrupted_encrypted_F = self._shuffle(cipher.iv+encrypted_A_corrupted_encrypted_F)
    
        with open(f'{os.path.basename(path_project)}__{postfix}.enc', 'wb') as f:
            f.write(shuffled_encrypted_A_corrupted_encrypted_F)
