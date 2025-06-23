import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

class CryptoUtils:
    @staticmethod
    def generate_rsa_keys():
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem.decode('utf-8'), public_pem.decode('utf-8')
    
    @staticmethod
    def encrypt_message(message, public_key_pem):
        """Encrypt message using RSA public key"""
        try:
            public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
            
            # RSA can only encrypt small messages, so for larger messages we would need hybrid encryption
            # For demo purposes, we'll limit message size
            message_bytes = message.encode('utf-8')
            
            if len(message_bytes) > 190:  # RSA 2048 can encrypt up to ~245 bytes, leaving some margin
                raise ValueError("Message too long for RSA encryption. Maximum ~190 characters.")
            
            encrypted = public_key.encrypt(
                message_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_message(encrypted_message, private_key_pem):
        """Decrypt message using RSA private key"""
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None
            )
            
            encrypted_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
            
            decrypted = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return decrypted.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_md5_hash(message):
        """Generate MD5 hash of message"""
        return hashlib.md5(message.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_md5_hash(message, expected_hash):
        """Verify MD5 hash"""
        actual_hash = CryptoUtils.generate_md5_hash(message)
        return actual_hash == expected_hash
