import base64
from Crypto.Cipher import AES
from pathlib import Path
import os
import binascii
import json

# KEY AND IV UP UNTIL VERSION 1.0.17
KEY = bytes.fromhex("D940840D5AE7C7907B092437BC0C5B44AAF70E273E12D0FB4DA2B8C767CC911D")
IV  = bytes.fromhex("37864EF15C24BC0ACBC60E3978EF1F06")

def pad(b): return b + bytes([AES.block_size - len(b) % AES.block_size] * (AES.block_size - len(b) % AES.block_size))
def unpad(b): return b[:-b[-1]]

def crypt_file(path, encrypt=True):
    data = path.read_bytes()
    is_json = False

    try:
        json.loads(data.decode("utf-8"))
        is_json = True
    except Exception:
        is_json = False

    if encrypt and not is_json:
        confirm = input(f"{path.name} doesn't look decrypted (probably already encrypted). Continue encrypting? (y/n): ").strip().lower()
        if confirm != "y":
            print(f"Skipped {path}")
            return
    elif not encrypt and is_json:
        confirm = input(f"{path.name} looks like valid JSON (probably already decrypted). Continue decrypting? (y/n): ").strip().lower()
        if confirm != "y":
            print(f"Skipped {path}")
            return

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

action = input("Encrypt or Decrypt (E/D)? ").strip().lower()
for file in find_saves():
    crypt_file(file, encrypt=(action == "e"))
