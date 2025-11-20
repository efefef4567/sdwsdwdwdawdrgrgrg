"""
# DISABLED: Substitution operations for binary transformation.
"""

# DISABLED: from typing import Callable, Dict, List, Tuple, Any


# DISABLED: class SubstitutionOperations:
    """Collection of substitution operations."""

# DISABLED:     def __init__(self):
        """Initialize substitution operations."""
# DISABLED:         self.operations = self._create_operations()

# DISABLED:     def _create_operations(self) -> Dict[str, Callable]:
        """Create all substitution operations."""
# DISABLED:         return {
# DISABLED:             'byte_substitution': self.byte_substitution,
# DISABLED:             'caesar_cipher': self.caesar_cipher,
# DISABLED:             'xor_key': self.xor_key,
# DISABLED:         }

# DISABLED:     def get_operations(self) -> Dict[str, Callable]:
        """Get all operations."""
# DISABLED:         return self.operations

# DISABLED:     def get_metadata(self, operation_name: str) -> Dict[str, Any]:
        """Get metadata for an operation."""
# DISABLED:         metadata_map = {
# DISABLED:             'byte_substitution': {
# DISABLED:                 'category': 'substitution',
# DISABLED:                 'description': 'Simple byte substitution',
# DISABLED:                 'required_params': ['substitution_table'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'caesar_cipher': {
# DISABLED:                 'category': 'substitution',
# DISABLED:                 'description': 'Caesar cipher substitution',
# DISABLED:                 'required_params': ['shift'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             },
# DISABLED:             'xor_key': {
# DISABLED:                 'category': 'substitution',
# DISABLED:                 'description': 'XOR with repeating key',
# DISABLED:                 'required_params': ['key'],
# DISABLED:                 'optional_params': {},
# DISABLED:                 'reversible': True
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(operation_name, {})

# DISABLED:     def caesar_cipher(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Caesar cipher substitution."""
# DISABLED:         shift = shift % 256
# DISABLED:         new_data = bytes([(b + shift) % 256 for b in binary_data])

# DISABLED:         def inverse():
# DISABLED:             return bytes([(b - shift) % 256 for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'caesar_cipher',
# DISABLED:             'shift': shift,
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def xor_key(self, binary_data: bytes, key: bytes) -> Tuple[bytes, Callable, Dict]:
        """XOR with repeating key."""
# DISABLED:         if not key:
# DISABLED:             raise ValueError("Key cannot be empty")

# DISABLED:         new_data = bytes([b ^ key[i % len(key)] for i, b in enumerate(binary_data)])

# DISABLED:         def inverse():
            # XOR is self-inverse
# DISABLED:             return bytes([b ^ key[i % len(key)] for i, b in enumerate(new_data)])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'xor_key',
# DISABLED:             'key_length': len(key),
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata

# DISABLED:     def byte_substitution(self, binary_data: bytes, substitution_table: List[int]) -> Tuple[bytes, Callable, Dict]:
        """Simple byte substitution."""
# DISABLED:         if len(substitution_table) != 256:
# DISABLED:             raise ValueError("Substitution table must have 256 entries")

        # Check if table contains all values 0-255 (permutation)
# DISABLED:         if set(substitution_table) != set(range(256)):
# DISABLED:             raise ValueError("Substitution table must be a permutation of 0-255")

# DISABLED:         new_data = bytes([substitution_table[b] for b in binary_data])

# DISABLED:         def inverse():
            # Create inverse table
# DISABLED:             inverse_table = [0] * 256
# DISABLED:             for i, val in enumerate(substitution_table):
# DISABLED:                 inverse_table[val] = i

# DISABLED:             return bytes([inverse_table[b] for b in new_data])

# DISABLED:         metadata = {
# DISABLED:             'operation': 'byte_substitution',
# DISABLED:             'bytes_affected': len(binary_data)
# DISABLED:         }

# DISABLED:         return new_data, inverse, metadata