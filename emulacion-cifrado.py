#Emulacion de cifrado asimetrico
#Fuente: OpenAI. (2025). Implementación de cifrado asimétrico con RSA en Python [Código fuente]. ChatGPT. https://openai.com
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# 1. Generar claves pública y privada
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# 2. Cifrar un mensaje con la clave pública
def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# 3. Descifrar el mensaje con la clave privada
def decrypt_message(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# 4. Firmar un mensaje con la clave privada
def sign_message(private_key, message):
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# 5. Verificar la firma con la clave pública (emulando una CA)
def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# Prueba del sistema
if __name__ == "__main__":
    private_key, public_key = generate_keys()
    
    message = "Hola, este es un mensaje seguro."
    print(f"Mensaje original: {message}")
    
    encrypted_message = encrypt_message(public_key, message)
    print(f"Mensaje cifrado: {encrypted_message.hex()}")
    
    decrypted_message = decrypt_message(private_key, encrypted_message)
    print(f"Mensaje descifrado: {decrypted_message}")
    
    signature = sign_message(private_key, message)
    print(f"Firma digital: {signature.hex()}")
    
    verification = verify_signature(public_key, message, signature)
    print(f"¿La firma es auténtica?: {verification}")
