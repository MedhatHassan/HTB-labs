import struct
import random

# Open the "flag.enc" file in binary read mode
with open("SimpleEncryptor/rev_simpleencryptor/flag.enc", "rb") as fp:
    # Read the entire file into memory
    file_contents = fp.read()

    # Extract the seed value (first 4 bytes) from the file contents
    seed = struct.unpack("<I", file_contents[:4])[0]
    print(f"Seed: {seed}")

    # Initialize the random number generator with the extracted seed
    random.seed(seed)

    decrypted_data = []

    # Decrypt the data starting from the 5th byte
    for byte in file_contents[4:]:
        # Generate two random numbers for each byte
        rand1 = random.randint(0, 2**31 - 1)
        rand2 = random.randint(0, 7)

        print(f"current byte: {byte:02X}")
        print(f"right shift: {rand2}")
        print(f"XOR key: {rand1:02X}")

        # Perform right shift and XOR operations
        decrypted_byte = ((byte >> rand2) | (byte << (8 - rand2))) ^ rand1

        print(f"byte after rotate right: {decrypted_byte:02X}")

        # Append the decrypted byte to the result
        decrypted_data.append(decrypted_byte)

        print(f"byte after full decryption: {decrypted_byte:02X}")
    
    # Convert the decrypted data to a bytes object
    decrypted_bytes = bytes(decrypted_data)

    # Print the decrypted flag as a string
    print("Decrypted Flag:")
    print(decrypted_bytes.decode("utf-8"))
