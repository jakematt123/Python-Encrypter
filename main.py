import sqlite3
from cryptography.fernet import Fernet
import base64

connection = sqlite3.connect('encrypted.db')
cur = connection.cursor()

key = b"ILoveSam!>3#c#4!@#"
def convert_key_to_fernet_key(key: bytes) -> bytes:
    encoded_key = base64.urlsafe_b64encode(key)
    

    while len(encoded_key) < 32:
        encoded_key += b'='  
    
    return encoded_key[:32]  


cipher = convert_key_to_fernet_key(key)
print("Fernet key:", cipher)


def closeDatabase():
    connection.close()

def main():
    username = input("Enter Username: ")
    prepassword = input("Enter Password: ")

    def createUser(username, password):
        password = cipher.encrypt(password.encode())
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()

    def decrypt(encrypted_password):
        decrypted_password = cipher.decrypt(encrypted_password).decode()
        return decrypted_password

    createUser(username, prepassword)

    print("Users in the database:")
    for row in cur.execute("SELECT * FROM users"):
        print(row)

    res = cur.execute("SELECT password FROM users")
    print("\nDecrypted passwords:")
    for row in res:
        try:
            decrypted_password = decrypt(row[0])
            print("Decrypted password:", decrypted_password)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    closeDatabase()
