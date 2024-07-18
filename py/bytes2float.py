import struct

# Byte sequence
byte_sequence = bytes([0x3C, 0x9D, 0x81, 0x3F])

# Unpack the byte sequence as a float
unpacked_float = struct.unpack('<f', byte_sequence)[0]

print(f"Unpacked float value: {unpacked_float}")
