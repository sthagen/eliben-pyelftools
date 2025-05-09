from __future__ import annotations


def int_to_bin(number: int, width: int = 32) -> bytes:
    r"""
    Convert an integer into its binary representation in a bytes object.
    Width is the amount of bits to generate. If width is larger than the actual
    amount of bits required to represent number in binary, sign-extension is
    used. If it's smaller, the representation is trimmed to width bits.
    Each "bit" is either '\x00' or '\x01'. The MSBit is first.

    Examples:

        >>> int_to_bin(19, 5)
        b'\x01\x00\x00\x01\x01'
        >>> int_to_bin(19, 8)
        b'\x00\x00\x00\x01\x00\x00\x01\x01'
    """
    if number < 0:
        number += 1 << width
    i = width - 1
    bits = bytearray(width)
    while number and i >= 0:
        bits[i] = number & 1
        number >>= 1
        i -= 1
    return bytes(bits)


_bit_values: dict[int, int] = {
    0: 0,
    1: 1,
    48: 0, # '0'
    49: 1, # '1'
    }

def bin_to_int(bits: bytes, signed: bool = False) -> int:
    r"""
    Logical opposite of int_to_bin. Both '0' and '\x00' are considered zero,
    and both '1' and '\x01' are considered one. Set sign to True to interpret
    the number as a 2-s complement signed integer.
    """
    number = 0
    bias = 0
    if signed and _bit_values[bits[0]] == 1:
        bits = bits[1:]
        bias = 1 << len(bits)
    for b in bits:
        number <<= 1
        number |= _bit_values[b]
    return number - bias


def swap_bytes(bits: bytes, bytesize: int = 8) -> bytes:
    r"""
    Bits is a b'' object containing a binary representation. Assuming each
    bytesize bits constitute a bytes, perform a endianness byte swap. Example:

        >>> swap_bytes(b'00011011', 2)
        b'11100100'
    """
    i = 0
    l = len(bits)
    output = [b""] * ((l // bytesize) + 1)
    j = len(output) - 1
    while i < l:
        output[j] = bits[i : i + bytesize]
        i += bytesize
        j -= 1
    return b"".join(output)


_char_to_bin = {}
_bin_to_char = {}
for i in range(256):
    ch = bytes((i,))
    bin = int_to_bin(i, 8)
    _char_to_bin[i] = bin
    _bin_to_char[bin] = ch


def encode_bin(data: bytes) -> bytes:
    r"""
    Create a binary representation of the given b'' object. Assume 8-bit
    ASCII. Example:

        >>> encode_bin(b'ab')
        b'\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00'
    """
    return b"".join(_char_to_bin[ch] for ch in data)


def decode_bin(data: bytes) -> bytes:
    """
    Logical opposite of decode_bin.
    """
    if len(data) & 7:
        raise ValueError("Data length must be a multiple of 8")
    i = 0
    j = 0
    l = len(data) // 8
    chars = [b""] * l
    while j < l:
        chars[j] = _bin_to_char[data[i:i+8]]
        i += 8
        j += 1
    return b"".join(chars)
