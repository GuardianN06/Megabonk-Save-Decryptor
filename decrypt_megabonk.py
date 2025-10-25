import base64
from Crypto.Cipher import AES
from pathlib import Path
import os
import binascii

# KEY AND IV UP UNTIL VERSION 1.0.17
KEY = bytes.fromhex("D940840D5AE7C7907B092437BC0C5B44AAF70E273E12D0FB4DA2B8C767CC911D")
IV  = bytes.fromhex("37864EF15C24BC0ACBC60E3978EF1F06")

def pad(b): return b + bytes([AES.block_size - len(b) % AES.block_size] * (AES.block_size - len(b) % AES.block_size))
def unpad(b): return b[:-b[-1]]

def crypt_file(path, encrypt=True):
    data = path.read_bytes()
    if encrypt:
        data = base64.b64encode(AES.new(KEY, AES.MODE_CBC, IV).encrypt(pad(data)))
    else:
        data = unpad(AES.new(KEY, AES.MODE_CBC, IV).decrypt(base64.b64decode(data)))
    path.write_bytes(data)
    print(f"{'Encrypted' if encrypt else 'Decrypted'} {path}")

def find_saves():
    base = Path(os.getenv("USERPROFILE")) / "AppData/LocalLow/Ved/Megabonk/Saves/CloudDir"
    return [f for folder in base.iterdir() if folder.is_dir() and folder.name.isdigit()
            for f in (folder / "progression.json", folder / "stats.json") if f.exists()]

try:
    action = input("Encrypt or Decrypt (E/D)? ").strip().lower()
    for file in find_saves():
        crypt_file(file, encrypt=(action == "e"))
except (binascii.Error, ValueError) as e:
    print("Probably already decrypted.")
