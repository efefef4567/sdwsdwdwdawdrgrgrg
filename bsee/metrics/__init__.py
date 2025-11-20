"""
Metrics module for BSEE
Contains metrics calculation functions.
"""

def calculate_metric(data: bytes, metric_name: str) -> float:
    """Calculate a specific metric for binary data"""
    if metric_name == "entropy":
        return calculate_entropy(data)
    elif metric_name == "compression_ratio":
        return calculate_compression_ratio(data)
    else:
        return 0.0

def calculate_entropy(data: bytes) -> float:
    """Calculate entropy of binary data"""
    if not data:
        return 0.0

    # Count byte frequencies
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1

    # Calculate entropy
    entropy = 0.0
    data_len = len(data)
    for count in freq:
        if count > 0:
            p = count / data_len
            import math
            entropy -= p * math.log2(p)

    return entropy

def calculate_compression_ratio(data: bytes) -> float:
    """Simple compression ratio calculation"""
    import zlib
    if not data:
        return 1.0
    compressed = zlib.compress(data)
    return len(compressed) / len(data)