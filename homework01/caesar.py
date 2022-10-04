def encrypt_caesar(text: str, shift: int = 3) -> str:
    plaintext = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            if 65 <= ord(char) + shift <= 90:
                plaintext = plaintext + chr((ord(char) + shift))
            else:
                plaintext = plaintext + chr((ord(char) + shift) - 26)
        elif char.islower():
            if 97 <= ord(char) + shift <= 122:
                plaintext = plaintext + chr((ord(char) + shift))
            else:
                plaintext = plaintext + chr((ord(char) + shift) - 26)
        elif char.isdigit() or not char.isupper() or not char.islower():
            plaintext = plaintext + char
    return plaintext


def decrypt_caesar(text: str, shift: int = 3) -> str:
    plaintext = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            if 65 <= ord(char) - shift <= 90:
                plaintext = plaintext + chr((ord(char) - shift))
            else:
                plaintext = plaintext + chr((ord(char) - shift) + 26)
        elif char.islower():
            if 97 <= ord(char) - shift <= 122:
                plaintext = plaintext + chr((ord(char) - shift))
            else:
                plaintext = plaintext + chr((ord(char) - shift) + 26)
        elif char.isdigit() or not char.isupper() or not char.islower():
            plaintext = plaintext + char
    return plaintext


