def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowalphabet = alphabet.lower()
    key = len(keyword)

    for i in range(len(plaintext)):
        if plaintext[i] in alphabet:
            shift = ord(keyword[i % key]) - ord("A")
            ciphertext = ciphertext + alphabet[(alphabet.find(plaintext[i]) + shift) % 26]
        elif plaintext[i] in lowalphabet:
            shift = ord(keyword[i % key]) - ord("a")
            ciphertext = ciphertext + lowalphabet[(lowalphabet.find(plaintext[i]) + shift) % 26]
        else:
            ciphertext = ciphertext + plaintext[i]
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowalphabet = alphabet.lower()
    key = len(keyword)

    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet:
            shift = ord(keyword[i % key]) - ord("A")
            plaintext = plaintext + alphabet[(alphabet.find(ciphertext[i]) - shift) % 26]
        elif ciphertext[i] in lowalphabet:
            shift = ord(keyword[i % key]) - ord("a")
            plaintext = plaintext + lowalphabet[(lowalphabet.find(ciphertext[i]) - shift) % 26]
        else:
            plaintext = plaintext + ciphertext[i]
    return plaintext




