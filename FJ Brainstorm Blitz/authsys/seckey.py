import secrets

# Generate a secure random key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)
print("Generated Secret Key:", secret_key)
