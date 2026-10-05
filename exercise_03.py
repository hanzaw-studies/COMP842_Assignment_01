import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

def run_exercise_3():
    # 1. Generate ECDSA public/private key pair on the secp256k1 curve
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()

    # Extract raw bytes to accurately compare cryptographic sizes
    # Private key is a 256-bit scalar integer (32 bytes)
    private_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')
    
    # Uncompressed public key contains a 1-byte prefix (0x04) + X (32 bytes) + Y (32 bytes)
    uncompressed_pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    print("--- 1. Key Generation & Size Comparison ---")
    print(f"Private Key (Hex): {private_bytes.hex()}")
    print(f"Private Key Size: {len(private_bytes)} bytes ({len(private_bytes.hex())} hex chars)")
    
    print(f"\nUncompressed Public Key (Hex): {uncompressed_pub_bytes.hex()}")
    print(f"Uncompressed Public Key Size: {len(uncompressed_pub_bytes)} bytes ({len(uncompressed_pub_bytes.hex())} hex chars)")

    # 2. Compress the public key
    # Extract the X and Y coordinates
    x_coordinate = public_key.public_numbers().x
    y_coordinate = public_key.public_numbers().y
    
    # Check if the Y coordinate is even or odd to assign the prefix
    prefix = b'\x02' if y_coordinate % 2 == 0 else b'\x03'
    x_bytes = x_coordinate.to_bytes(32, 'big')
    compressed_pub_bytes = prefix + x_bytes

    print("\n--- 2. Public Key Compression ---")
    print(f"Compressed Public Key (Hex): {compressed_pub_bytes.hex()}")
    print(f"Compressed Public Key Size: {len(compressed_pub_bytes)} bytes ({len(compressed_pub_bytes.hex())} hex chars)")
    
    # Calculate percentage reduction in storage size
    original_size = len(uncompressed_pub_bytes)
    compressed_size = len(compressed_pub_bytes)
    reduction = ((original_size - compressed_size) / original_size) * 100
    print(f"Percentage Reduction in Storage Size: {reduction:.2f}%")

    # 3 & 4. Verify the compressed public key can validate a digital signature
    print("\n--- 3. Digital Signature Verification ---")
    message = b"COMP842 Blockchain Security"
    
    # Sign the message with the original private key
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    print(f"Message: {message.decode()}")
    print(f"Signature (Hex): {signature.hex()}")

    # Reconstruct the public key object directly from the compressed bytes
    reconstructed_pub_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256K1(), compressed_pub_bytes
    )

    # Verify the signature using the reconstructed (compressed) public key
    try:
        reconstructed_pub_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        print("\nVerification Result: SUCCESS - Signature is valid using the compressed public key.")
    except Exception as e:
        print("\nVerification Result: FAILED - Signature is invalid.")

if __name__ == "__main__":
    run_exercise_3()