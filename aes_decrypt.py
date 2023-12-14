#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys

key = bytes([0x34, 0x52, 0x2A, 0x5B, 0x7A, 0x6E, 0x49, 0x2C, 0x08, 0x09, 0x0A, 0x9D, 0x8D, 0x2A, 0x23, 0xF8])

def decrypt_aes_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def encrypt_aes_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def main(hex_string):
    encrypted_bytes = bytes(hex_string)
    decrypted_text = decrypt_aes_ecb(encrypted_bytes, key)
    reecrypted_text = encrypt_aes_ecb(decrypted_text, key)

    clear_hex_string = ' '.join(f'{byte:02X}' for byte in decrypted_text)
    ori_hex_string = ' '.join(f'{byte:02X}' for byte in hex_string)
    reecrypted_hex_string = ' '.join(f'{byte:02X}' for byte in reecrypted_text)

    print(f"Original string: {ori_hex_string}")
    print(f"Decrypted:       {clear_hex_string}")
    print(f"Decminal:        {' '.join(f'{byte:02d}' for byte in decrypted_text)}")
    #print(f"Re-encrypted:    {reecrypted_hex_string}")
    #print()




if __name__ == "__main__":
    # red = bytearray.fromhex("2d ec 31 7e 71 81 cc b0 79 fc 66 5a e4 3f a9 dd")
    # green = bytearray.fromhex("7a 39 48 da de a3 c9 e8 b2 c3 7c 3c 4b 82 89 4d")
    # blue = bytearray.fromhex("6b c5 c6 0c 25 f6 ee 27 49 e0 1b 14 3b 5a 8c f9")
    # main(red)
    # main(green)
    # main(blue)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            hex_string = bytearray.fromhex(line)
            try:
                main(hex_string)
            except:
                print(' '.join(f'{byte:02X}' for byte in hex_string))
                continue
