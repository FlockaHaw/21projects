#!/usr/bin/env python3
import binascii
import re

# Your suspicious query
query = "dnscat.28b700329a268a0021636f6d6d616e642028426573742d4b6f6d702900"

# Extract the encoded part
encoded_part = query.split('.')[1]
print(f"Encoded: {encoded_part}")

# Decode hex
raw_bytes = binascii.unhexlify(encoded_part)
print(f"\nRaw bytes: {raw_bytes}")

# Split into components
session_id = raw_bytes[:8]  # First 8 bytes (16 hex chars)
session_id_hex = session_id.hex()
print(f"\n🔑 SESSION ID: {session_id_hex}")

# Remaining part contains the command
command_bytes = raw_bytes[8:]
try:
    command = command_bytes.decode('ascii').rstrip('\x00')
    print(f"📝 Command: {command}")
except:
    print(f"Command bytes: {command_bytes}")

# Extract the actual session key (might be the first 16 bytes)
session_key_full = raw_bytes[:16]  # First 16 bytes
session_key_hex = session_key_full.hex()
print(f"\n🔐 FULL SESSION KEY: {session_key_hex}")

# Output:
print("\n" + "="*50)
print("DNSCAT2 HANDSHAKE DECODED:")
print(f"Session Key: {session_key_hex}")
print(f"Command: {command}")
print("="*50)
