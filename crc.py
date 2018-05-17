# -*- coding: utf-8 -*-
from bitarray import bitarray

def xor_at(a, b, offset=0):
    for k, bk in enumerate(b):
        index = offset + k
        a[index] = a[index] ^ bk

def crc(d, g):
	# We'd prefer not to modify the argument in xor_at
    dcopy = d.copy()  
	#
	# TODO: compute and return remainder "r"
	#


if __name__ == '__main__':

    print("From Kurose & Ross (7e), page 478:")
    g = bitarray('1001')            # generator
    d = bitarray('101110')          # data (without padding/shifting)
    p = bitarray('000')             # padding
    r = crc(d + p, g)               # error-correction bits
    assert r == bitarray('011')     # known quotient
    assert crc(d + r, g) == p       # perform CRC check
    
    print("From Wikipedia, [en.wikipedia.org/wiki/Cyclic_redundancy_check]:")
    g = bitarray('1011')            # generator
    d = bitarray('11010011101100')  # data (without padding/shifting) 
    p = bitarray('000')             # padding
    r = crc(d + p, g)               # error-correction bits
    assert r == bitarray('100')     # known quotient
    assert crc(d + r, g) == p       # perform CRC check
    