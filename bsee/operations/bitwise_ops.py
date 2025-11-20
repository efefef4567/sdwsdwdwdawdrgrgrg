"""
# DISABLED: Bitwise operations for binary transformation.
"""

# DISABLED: import struct
# DISABLED: from typing import Callable, Dict, List, Tuple, Any


# DISABLED: class BitwiseOperations:
    """Collection of bitwise operations."""

# DISABLED:     def __init__(self):
        """Initialize bitwise operations."""
# DISABLED:         self.operations = self._create_operations()

# DISABLED:     def _create_operations(self) -> Dict[str, Callable]:
        """Create all bitwise operations."""
# DISABLED:         return {
# DISABLED:             'xor_constant': self.xor_with_constant,
# DISABLED:             'xor_range': self.xor_with_range,
# DISABLED:             'not_bytes': self.not_bytes,
# DISABLED:             'and_constant': self.and_with_constant,
# DISABLED:             'or_constant': self.or_constant,
# DISABLED:             'rotate_left': self.rotate_bits_left,
# DISABLED:             'rotate_right': self.rotate_bits_right,
# DISABLED:             'shift_left': self.shift_bits_left,
# DISABLED:             'shift_right': self.shift_bits_right,
# DISABLED:             'swap_nibbles': self.swap_nibbles,
# DISABLED:             'swap_bits': self.swap_bits_in_byte,
# DISABLED:             'reverse_bits': self.reverse_bits_in_byte,
# DISABLED:             'extract_high_nibble': self.extract_high_nibble,
# DISABLED:             'extract_low_nibble': self.extract_low_nibble,
# DISABLED:             'clear_bit': self.clear_bit,
# DISABLED:             'set_bit': self.set_bit,
# DISABLED:             'toggle_bit': self.toggle_bit,
# DISABLED:             'mask_bits': self.mask_bits,
# DISABLED:             'interleave_bits': self.interleave_bits,
# DISABLED:             'deinterleave_bits': self.deinterleave_bits
# DISABLED:         }

# DISABLED:     def get_operations(self) -> Dict[str, Callable]:
        """Get all operations."""
# DISABLED:         return self.operations

# DISABLED:     def get_metadata(self, operation_name: str) -> Dict[str, Any]:
        """Get metadata for an operation."""
# DISABLED:         metadata_map = {
# DISABLED:             'xor_constant': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'XOR all bytes with a constant value',
# DISABLED:                 'required_params': ['constant'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'xor_range': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'XOR a range of bytes with a constant',
# DISABLED:                 'required_params': ['offset', 'length', 'constant'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'not_bytes': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Apply bitwise NOT to all bytes',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'and_constant': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Apply bitwise AND with constant',
# DISABLED:                 'required_params': ['constant'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'or_constant': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Apply bitwise OR with constant',
# DISABLED:                 'required_params': ['constant'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'rotate_left': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Rotate bits left in each byte',
# DISABLED:                 'required_params': ['shift'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'rotate_right': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Rotate bits right in each byte',
# DISABLED:                 'required_params': ['shift'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'shift_left': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Shift bits left in each byte',
# DISABLED:                 'required_params': ['shift'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'shift_right': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Shift bits right in each byte',
# DISABLED:                 'required_params': ['shift'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'swap_nibbles': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Swap high and low nibbles in each byte',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'swap_bits': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Swap two bit positions in each byte',
# DISABLED:                 'required_params': ['bit1', 'bit2'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'reverse_bits': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Reverse bit order in each byte',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'extract_high_nibble': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Extract high nibble from each byte',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'extract_low_nibble': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Extract low nibble from each byte',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'clear_bit': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Clear a specific bit position in all bytes',
# DISABLED:                 'required_params': ['bit_position'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'set_bit': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Set a specific bit position in all bytes',
# DISABLED:                 'required_params': ['bit_position'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'toggle_bit': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Toggle a specific bit position in all bytes',
# DISABLED:                 'required_params': ['bit_position'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'mask_bits': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Apply bit mask to all bytes',
# DISABLED:                 'required_params': ['mask'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': False
# DISABLED:             },
# DISABLED:             'interleave_bits': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Interleave bits from adjacent bytes',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'deinterleave_bits': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Deinterleave bits from adjacent bytes',
# DISABLED:                 'required_params': [],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(operation_name, {})

    # Operation implementations

# DISABLED:     def xor_with_constant(self, binary_data: bytes, constant: int) -> Tuple[bytes, Callable, Dict]:
        """XOR all bytes with a constant value."""
# DISABLED:         if not 0 <= constant <= 255:
# DISABLED:             raise ValueError("Constant must be in range 0-255")

# DISABLED:         new_data = bytes([b ^ constant for b in binary_data])

# DISABLED:         def inverse():
            # XOR is self-inverse
# DISABLED:             return bytes([b ^ constant for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'xor_constant',
# DISABLED:             'constant': constant,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def xor_with_range(self, binary_data: bytes, offset: int, length: int, constant: int) -> Tuple[bytes, Callable, Dict]:
        """XOR a range of bytes with a constant."""
# DISABLED:         if not 0 <= constant <= 255:
# DISABLED:             raise ValueError("Constant must be in range 0-255")
# DISABLED:         if offset < 0 or offset >= len(binary_data):
# DISABLED:             raise ValueError("Offset out of range")
# DISABLED:         if offset + length > len(binary_data):
# DISABLED:             raise ValueError("Range exceeds file size")

# DISABLED:         data_list = list(binary_data)
# DISABLED:         for i in range(offset, offset + length):
# DISABLED:             data_list[i] ^= constant

# DISABLED:         new_data = bytes(data_list)

# DISABLED:         def inverse():
            # XOR is self-inverse
# DISABLED:             inverse_list = list(new_data)
# DISABLED:             for i in range(offset, offset + length):
# DISABLED:                 inverse_list[i] ^= constant
# DISABLED:             return bytes(inverse_list)

# DISABLED:         metadata = {
# DISABLED:             'operation': 'xor_range',
# DISABLED:             'offset': offset,
# DISABLED:             'length': length,
# DISABLED:             'constant': constant,
# DISABLED:             'bytes_affected': length
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def not_bytes(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Apply bitwise NOT to all bytes."""
# DISABLED:         new_data = bytes([~b & 0xFF for b in binary_data])

# DISABLED:         def inverse():
            # NOT is self-inverse
# DISABLED:             return bytes([~b & 0xFF for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'not_bytes',
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def and_with_constant(self, binary_data: bytes, constant: int) -> Tuple[bytes, Callable, Dict]:
        """Apply bitwise AND with constant."""
# DISABLED:         if not 0 <= constant <= 255:
# DISABLED:             raise ValueError("Constant must be in range 0-255")

# DISABLED:         new_data = bytes([b & constant for b in binary_data])

# DISABLED:         def inverse():
            # AND is not fully reversible without additional information
            # This is a lossy operation
# DISABLED:             raise RuntimeError("AND operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'and_constant',
# DISABLED:             'constant': constant,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def or_constant(self, binary_data: bytes, constant: int) -> Tuple[bytes, Callable, Dict]:
        """Apply bitwise OR with constant."""
# DISABLED:         if not 0 <= constant <= 255:
# DISABLED:             raise ValueError("Constant must be in range 0-255")

# DISABLED:         new_data = bytes([b | constant for b in binary_data])

# DISABLED:         def inverse():
            # OR is not fully reversible without additional information
            # This is a lossy operation
# DISABLED:             raise RuntimeError("OR operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'or_constant',
# DISABLED:             'constant': constant,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def rotate_bits_left(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Rotate bits left in each byte."""
# DISABLED:         if not 0 <= shift <= 7:
# DISABLED:             raise ValueError("Shift must be in range 0-7")

# DISABLED:         new_data = bytes([((b << shift) & 0xFF) | (b >> (8 - shift)) for b in binary_data])

# DISABLED:         def inverse():
            # Rotate right by the same amount
# DISABLED:             return bytes([((b >> shift) & 0xFF) | (b << (8 - shift)) & 0xFF for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'rotate_left',
# DISABLED:             'shift': shift,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def rotate_bits_right(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Rotate bits right in each byte."""
# DISABLED:         if not 0 <= shift <= 7:
# DISABLED:             raise ValueError("Shift must be in range 0-7")

# DISABLED:         new_data = bytes([(b >> shift) | ((b << (8 - shift)) & 0xFF) for b in binary_data])

# DISABLED:         def inverse():
            # Rotate left by the same amount
# DISABLED:             return bytes([((b << shift) & 0xFF) | (b >> (8 - shift)) for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'rotate_right',
# DISABLED:             'shift': shift,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def shift_bits_left(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Shift bits left in each byte."""
# DISABLED:         if not 0 <= shift <= 7:
# DISABLED:             raise ValueError("Shift must be in range 0-7")

# DISABLED:         new_data = bytes([(b << shift) & 0xFF for b in binary_data])

# DISABLED:         def inverse():
            # Left shift is lossy (bits are lost)
# DISABLED:             raise RuntimeError("Left shift operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'shift_left',
# DISABLED:             'shift': shift,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def shift_bits_right(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Shift bits right in each byte."""
# DISABLED:         if not 0 <= shift <= 7:
# DISABLED:             raise ValueError("Shift must be in range 0-7")

# DISABLED:         new_data = bytes([b >> shift for b in binary_data])

# DISABLED:         def inverse():
            # Right shift is lossy (bits are lost)
# DISABLED:             raise RuntimeError("Right shift operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'shift_right',
# DISABLED:             'shift': shift,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def swap_nibbles(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Swap high and low nibbles in each byte."""
# DISABLED:         new_data = bytes([((b & 0x0F) << 4) | ((b & 0xF0) >> 4) for b in binary_data])

# DISABLED:         def inverse():
            # Swap nibbles is self-inverse
# DISABLED:             return bytes([((b & 0x0F) << 4) | ((b & 0xF0) >> 4) for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'swap_nibbles',
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def swap_bits_in_byte(self, binary_data: bytes, bit1: int, bit2: int) -> Tuple[bytes, Callable, Dict]:
        """Swap two bit positions in each byte."""
# DISABLED:         if not 0 <= bit1 <= 7 or not 0 <= bit2 <= 7:
# DISABLED:             raise ValueError("Bit positions must be in range 0-7")
# DISABLED:         if bit1 == bit2:
# DISABLED:             raise ValueError("Bit positions must be different")

# DISABLED:         def swap_byte_bits(byte_val: int) -> int:
# DISABLED:             bit1_val = (byte_val >> bit1) & 1
# DISABLED:             bit2_val = (byte_val >> bit2) & 1

# DISABLED:             if bit1_val != bit2_val:
                # Clear both bits and set them in swapped positions
# DISABLED:                 result = byte_val & ~(1 << bit1) & ~(1 << bit2)
# DISABLED:                 result |= (bit1_val << bit2) | (bit2_val << bit1)
# DISABLED:                 return result
# DISABLED:             return byte_val

# DISABLED:         new_data = bytes([swap_byte_bits(b) for b in binary_data])

# DISABLED:         def inverse():
            # Swap bits is self-inverse
# DISABLED:             return bytes([swap_byte_bits(b) for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'swap_bits',
# DISABLED:             'bit1': bit1,
# DISABLED:             'bit2': bit2,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def reverse_bits_in_byte(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Reverse bit order in each byte."""
# DISABLED:         def reverse_byte(byte_val: int) -> int:
# DISABLED:             result = 0
# DISABLED:             for i in range(8):
# DISABLED:                 result = (result << 1) | ((byte_val >> i) & 1)
# DISABLED:             return result

# DISABLED:         new_data = bytes([reverse_byte(b) for b in binary_data])

# DISABLED:         def inverse():
            # Bit reversal is self-inverse
# DISABLED:             return bytes([reverse_byte(b) for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'reverse_bits',
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def clear_bit(self, binary_data: bytes, bit_position: int) -> Tuple[bytes, Callable, Dict]:
        """Clear a specific bit position in all bytes."""
# DISABLED:         if not 0 <= bit_position <= 7:
# DISABLED:             raise ValueError("Bit position must be in range 0-7")

# DISABLED:         mask = ~(1 << bit_position) & 0xFF
# DISABLED:         new_data = bytes([b & mask for b in binary_data])

# DISABLED:         def inverse():
            # Clear bit is lossy
# DISABLED:             raise RuntimeError("Clear bit operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'clear_bit',
# DISABLED:             'bit_position': bit_position,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def set_bit(self, binary_data: bytes, bit_position: int) -> Tuple[bytes, Callable, Dict]:
        """Set a specific bit position in all bytes."""
# DISABLED:         if not 0 <= bit_position <= 7:
# DISABLED:             raise ValueError("Bit position must be in range 0-7")

# DISABLED:         mask = 1 << bit_position
# DISABLED:         new_data = bytes([b | mask for b in binary_data])

# DISABLED:         def inverse():
            # Set bit is lossy
# DISABLED:             raise RuntimeError("Set bit operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'set_bit',
# DISABLED:             'bit_position': bit_position,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def toggle_bit(self, binary_data: bytes, bit_position: int) -> Tuple[bytes, Callable, Dict]:
        """Toggle a specific bit position in all bytes."""
# DISABLED:         if not 0 <= bit_position <= 7:
# DISABLED:             raise ValueError("Bit position must be in range 0-7")

# DISABLED:         mask = 1 << bit_position
# DISABLED:         new_data = bytes([b ^ mask for b in binary_data])

# DISABLED:         def inverse():
            # Toggle is self-inverse
# DISABLED:             return bytes([b ^ mask for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'toggle_bit',
# DISABLED:             'bit_position': bit_position,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def mask_bits(self, binary_data: bytes, mask: int) -> Tuple[bytes, Callable, Dict]:
        """Apply bit mask to all bytes."""
# DISABLED:         if not 0 <= mask <= 255:
# DISABLED:             raise ValueError("Mask must be in range 0-255")

# DISABLED:         new_data = bytes([b & mask for b in binary_data])

# DISABLED:         def inverse():
            # Mask is lossy
# DISABLED:             raise RuntimeError("Mask operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'mask_bits',
# DISABLED:             'mask': mask,
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def extract_high_nibble(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Extract high nibble from each byte."""
# DISABLED:         new_data = bytes([(b & 0xF0) >> 4 for b in binary_data])

# DISABLED:         def inverse():
            # Extract is lossy
# DISABLED:             raise RuntimeError("Extract high nibble operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'extract_high_nibble',
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def extract_low_nibble(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Extract low nibble from each byte."""
# DISABLED:         new_data = bytes([b & 0x0F for b in binary_data])

# DISABLED:         def inverse():
            # Extract is lossy
# DISABLED:             raise RuntimeError("Extract low nibble operation is not reversible")

# DISABLED:         metadata = {
# DISABLED:             'operation': 'extract_low_nibble',
# DISABLED:             'bytes_affected': len(binary_data),
# DISABLED:             'reversible': False
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def interleave_bits(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Interleave bits from adjacent bytes."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return binary_data, lambda: binary_data, {'operation': 'interleave_bits', 'bytes_affected': 0}

        # Handle odd length by padding with zero
# DISABLED:         padded_data = binary_data
# DISABLED:         if len(binary_data) % 2 != 0:
# DISABLED:             padded_data = binary_data + b'\x00'

# DISABLED:         result = bytearray()
# DISABLED:         for i in range(0, len(padded_data), 2):
# DISABLED:             byte1 = padded_data[i]
# DISABLED:             byte2 = padded_data[i + 1]

            # Interleave bits: bit0 from byte1, bit0 from byte2, bit1 from byte1, bit1 from byte2, etc.
# DISABLED:             for bit_pos in range(8):
# DISABLED:                 result.append(((byte1 >> bit_pos) & 1) << 1 | ((byte2 >> bit_pos) & 1))

# DISABLED:         new_data = bytes(result)

# DISABLED:         def inverse():
            # Deinterleave the bits back to original bytes
# DISABLED:             result = bytearray()
# DISABLED:             for i in range(0, len(new_data), 16):
# DISABLED:                 chunk = new_data[i:i+16]
# DISABLED:                 if len(chunk) < 16:
                    # Pad incomplete chunk
# DISABLED:                     chunk += b'\x00' * (16 - len(chunk))

# DISABLED:                 byte1 = 0
# DISABLED:                 byte2 = 0
# DISABLED:                 for bit_pos in range(8):
# DISABLED:                     byte1 |= ((chunk[bit_pos * 2] >> 1) & 1) << bit_pos
# DISABLED:                     byte2 |= (chunk[bit_pos * 2 + 1] & 1) << bit_pos

# DISABLED:                 result.append(byte1)
# DISABLED:                 result.append(byte2)

            # Remove padding if original was odd length
# DISABLED:             if len(binary_data) % 2 != 0:
# DISABLED:                 result = result[:-1]

# DISABLED:             return bytes(result)

# DISABLED:         metadata = {
# DISABLED:             'operation': 'interleave_bits',
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def deinterleave_bits(self, binary_data: bytes) -> Tuple[bytes, Callable, Dict]:
        """Deinterleave bits from adjacent bytes."""
        # This is essentially the inverse of interleave_bits
        # For simplicity, we'll call interleave_bits as it's self-inverse
# DISABLED:         new_data, inverse_fn, metadata = self.interleave_bits(binary_data)
# DISABLED:         metadata['operation'] = 'deinterleave_bits'
# DISABLED:         return new_data, inverse_fn, metadata