"""
Substitution operations for binary transformation.
"""

from typing import Callable, Dict, List, Tuple, Any


class SubstitutionOperations:
    """Collection of substitution operations."""

    def __init__(self):
        """Initialize substitution operations."""
        self.operations = self._create_operations()

    def _create_operations(self) -> Dict[str, Callable]:
        """Create all substitution operations."""
        return {
            'byte_substitution': self.byte_substitution,
            'caesar_cipher': self.caesar_cipher,
            'xor_key': self.xor_key,
        }

    def get_operations(self) -> Dict[str, Callable]:
        """Get all operations."""
        return self.operations

    def get_metadata(self, operation_name: str) -> Dict[str, Any]:
        """Get metadata for an operation."""
        metadata_map = {
            'byte_substitution': {
                'category': 'substitution',
                'description': 'Simple byte substitution',
                'required_params': ['substitution_table'],
                'optional_params': {},
                'reversible': True
            },
            'caesar_cipher': {
                'category': 'substitution',
                'description': 'Caesar cipher substitution',
                'required_params': ['shift'],
                'optional_params': {},
                'reversible': True
            },
            'xor_key': {
                'category': 'substitution',
                'description': 'XOR with repeating key',
                'required_params': ['key'],
                'optional_params': {},
                'reversible': True
            }
        }
        return metadata_map.get(operation_name, {})

    def caesar_cipher(self, binary_data: bytes, shift: int) -> Tuple[bytes, Callable, Dict]:
        """Caesar cipher substitution."""
        shift = shift % 256
        new_data = bytes([(b + shift) % 256 for b in binary_data])

        def inverse():
            return bytes([(b - shift) % 256 for b in new_data])

        metadata = {
            'operation': 'caesar_cipher',
            'shift': shift,
            'bytes_affected': len(binary_data)
        }

        return new_data, inverse, metadata

    def xor_key(self, binary_data: bytes, key: bytes) -> Tuple[bytes, Callable, Dict]:
        """XOR with repeating key."""
        if not key:
            raise ValueError("Key cannot be empty")

        new_data = bytes([b ^ key[i % len(key)] for i, b in enumerate(binary_data)])

        def inverse():
            # XOR is self-inverse
            return bytes([b ^ key[i % len(key)] for i, b in enumerate(new_data)])

        metadata = {
            'operation': 'xor_key',
            'key_length': len(key),
            'bytes_affected': len(binary_data)
        }

        return new_data, inverse, metadata

    def byte_substitution(self, binary_data: bytes, substitution_table: List[int]) -> Tuple[bytes, Callable, Dict]:
        """Simple byte substitution."""
        if len(substitution_table) != 256:
            raise ValueError("Substitution table must have 256 entries")

        # Check if table contains all values 0-255 (permutation)
        if set(substitution_table) != set(range(256)):
            raise ValueError("Substitution table must be a permutation of 0-255")

        new_data = bytes([substitution_table[b] for b in binary_data])

        def inverse():
            # Create inverse table
            inverse_table = [0] * 256
            for i, val in enumerate(substitution_table):
                inverse_table[val] = i

            return bytes([inverse_table[b] for b in new_data])

        metadata = {
            'operation': 'byte_substitution',
            'bytes_affected': len(binary_data)
        }

        return new_data, inverse, metadata