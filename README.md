# Megabonk Save Decryptor

A simple Python tool for decrypting and encrypting **Megabonk** game save files (`progression.json` and `stats.json`) stored locally on Windows.  
This utility makes it easy to view, modify, or back up your save data by handling the AES encryption used by the game.

---

## Features

-  **AES-CBC Decryption & Encryption**
-  **Auto-Detection** of Megabonk save files in the correct directory  
-  **Supports both progression and stats saves**
-  **Encryption validation (already encrypted/decrypted)**
---

## Default Save Location

The script automatically scans your save directory:

%USERPROFILE%\AppData\LocalLow\Ved\Megabonk\Saves\CloudDir\

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/GuardianN06/Megabonk-Save-Decryptor.git
cd Megabonk-Save-Decryptor
python decrypt_megabonk.py
```

### Open file in text editor, modify what you like and enjoy!
