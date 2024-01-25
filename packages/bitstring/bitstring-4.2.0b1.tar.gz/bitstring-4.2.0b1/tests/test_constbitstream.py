#!/usr/bin/env python

import unittest
import sys
import bitstring
import io
import os
from bitstring import ConstBitStream as CBS

sys.path.insert(0, '..')


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class All(unittest.TestCase):
    def testFromFile(self):
        s = CBS(filename=os.path.join(THIS_DIR, 'test.m1v'))
        self.assertEqual(s[0:32].hex, '000001b3')
        self.assertEqual(s.read(8 * 4).hex, '000001b3')
        width = s.read(12).uint
        height = s.read(12).uint
        self.assertEqual((width, height), (352, 288))

    def testFromFileWithOffsetAndLength(self):
        s = CBS(filename=os.path.join(THIS_DIR, 'test.m1v'), offset=24, length=8)
        self.assertEqual(s.h, 'b3')
        reconstructed = ''
        for bit in s:
            reconstructed += '1' if bit is True else '0'
        self.assertEqual(reconstructed, s.bin)


class InterleavedExpGolomb(unittest.TestCase):
    def testReading(self):
        s = CBS(uie=333)
        a = s.read('uie')
        self.assertEqual(a, 333)
        s = CBS('uie=12, sie=-9, sie=9, uie=1000000')
        u = s.unpack('uie, 2*sie, uie')
        self.assertEqual(u, [12, -9, 9, 1000000])

    def testReadingErrors(self):
        s = CBS(10)
        with self.assertRaises(bitstring.ReadError):
            s.read('uie')
        self.assertEqual(s.pos, 0)
        with self.assertRaises(bitstring.ReadError):
            s.read('sie')
        self.assertEqual(s.pos, 0)


class ReadTo(unittest.TestCase):
    def testByteAligned(self):
        a = CBS('0xaabb00aa00bb')
        b = a.readto('0x00', bytealigned=True)
        self.assertEqual(b, '0xaabb00')
        self.assertEqual(a.bytepos, 3)
        b = a.readto('0xaa', bytealigned=True)
        self.assertEqual(b, '0xaa')
        with self.assertRaises(bitstring.ReadError):
            b.readto('0xcc', bytealigned=True)

    def testNotAligned(self):
        a = CBS('0b00111001001010011011')
        a.pos = 1
        self.assertEqual(a.readto('0b00'), '0b011100')
        self.assertEqual(a.readto('0b110'), '0b10010100110')
        with self.assertRaises(ValueError):
            a.readto('')

    def testDisallowIntegers(self):
        a = CBS('0x0f')
        with self.assertRaises(ValueError):
            a.readto(4)

    def testReadingLines(self):
        s = b"This is a test\nof reading lines\nof text\n"
        b = CBS(bytes=s)
        n = bitstring.Bits(bytes=b'\n')
        self.assertEqual(b.readto(n).bytes, b'This is a test\n')
        self.assertEqual(b.readto(n).bytes, b'of reading lines\n')
        self.assertEqual(b.readto(n).bytes, b'of text\n')


class Subclassing(unittest.TestCase):

    def testIsInstance(self):
        class SubBits(CBS):
            pass
        a = SubBits()
        self.assertTrue(isinstance(a, SubBits))

    def testClassType(self):
        class SubBits(CBS):
            pass
        self.assertEqual(SubBits().__class__, SubBits)


class PadToken(unittest.TestCase):

    def testRead(self):
        s = CBS('0b100011110001')
        a = s.read('pad:1')
        self.assertEqual(a, None)
        self.assertEqual(s.pos, 1)
        a = s.read(3)
        self.assertEqual(a, CBS('0b000'))
        a = s.read('pad:1')
        self.assertEqual(a, None)
        self.assertEqual(s.pos, 5)

    def testReadList(self):
        s = CBS('0b10001111001')
        t = s.readlist('pad:1, uint:3, pad:4, uint:3')
        self.assertEqual(t, [0, 1])
        s.pos = 0
        t = s.readlist('pad:1, pad:5')
        self.assertEqual(t, [])
        self.assertEqual(s.pos, 6)
        s.pos = 0
        t = s.readlist('pad:1, bin, pad:4, uint:3')
        self.assertEqual(t, ['000', 1])
        s.pos = 0
        t = s.readlist('pad, bin:3, pad:4, uint:3')
        self.assertEqual(t, ['000', 1])


class ReadingBytes(unittest.TestCase):

    def testUnpackingBytes(self):
        s = CBS(80)
        t = s.unpack('bytes:1')
        self.assertEqual(t[0], b'\x00')
        a, b, c = s.unpack('bytes:1, bytes, bytes2')
        self.assertEqual(a, b'\x00')
        self.assertEqual(b, b'\x00'*7)
        self.assertEqual(c, b'\x00'*2)

    def testUnpackingBytesWithKeywords(self):
        s = CBS('0x55'*10)
        t = s.unpack('pad:a, bytes:b, bytes, pad:a', a=4, b=6)
        self.assertEqual(t, [b'\x55'*6, b'\x55'*3])


class ReadingBitsAsDefault(unittest.TestCase):

    def testReadBits(self):
        s = CBS('uint:31=14')
        v = s.read(31)
        self.assertEqual(v.uint, 14)
        s.pos = 0

    def testReadListBits(self):
        s = CBS('uint:5=3, uint:3=0, uint:11=999')
        v = s.readlist([5, 3, 11])
        self.assertEqual([x.uint for x in v], [3, 0, 999])
        s.pos = 0
        v = s.readlist(['5', '3', 11])
        self.assertEqual([x.uint for x in v], [3, 0, 999])


class Lsb0Reading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        bitstring.lsb0 = True

    @classmethod
    def tearDownClass(cls):
        bitstring.lsb0 = False

    def testReadingHex(self):
        s = CBS('0xabcdef')
        self.assertEqual(s.read('hex:4'), 'f')
        self.assertEqual(s.read(4), '0xe')
        self.assertEqual(s.pos, 8)

    def testReadingOct(self):
        s = CBS('0o123456')
        self.assertEqual(s.read('o6'), '56')
        self.assertEqual(s.pos, 6)

    def testReadingBin(self):
        s = CBS('0b00011')
        self.assertEqual(s.read('bin:3'), '011')
        self.assertEqual(s.pos, 3)

    def testReadingBytes(self):
        s = CBS(bytes=b'54321')
        self.assertEqual(s.pos, 0)
        s.pos = 8
        self.assertEqual(s.read('bytes:2'), b'32')


class BytesIOCreation(unittest.TestCase):

    def testSimpleCreation(self):
        f = io.BytesIO(b"\x12\xff\x77helloworld")
        s = CBS(f)
        self.assertEqual(s[0:8], '0x12')
        self.assertEqual(len(s), 13 * 8)
        s = CBS(f, offset=8, length=12)
        self.assertEqual(s, '0xff7')

    def testExceptions(self):
        f = io.BytesIO(b"123456789")
        _ = CBS(f, length=9*8)
        with self.assertRaises(bitstring.CreationError):
            _ = CBS(f, length=9*8 + 1)
        with self.assertRaises(bitstring.CreationError):
            _ = CBS(f, length=9*8, offset=1)


class CreationWithPos(unittest.TestCase):

    def testDefaultCreation(self):
        s = CBS('0xabc')
        self.assertEqual(s.pos, 0)

    def testPositivePos(self):
        s = CBS('0xabc', pos=0)
        self.assertEqual(s.pos, 0)
        s = CBS('0xabc', pos=1)
        self.assertEqual(s.pos, 1)
        s = CBS('0xabc', pos=12)
        self.assertEqual(s.pos, 12)
        with self.assertRaises(bitstring.CreationError):
            _ = CBS('0xabc', pos=13)

    def testNegativePos(self):
        s = CBS('0xabc', pos=-1)
        self.assertEqual(s.pos, 11)
        s = CBS('0xabc', pos=-12)
        self.assertEqual(s.pos, 0)
        with self.assertRaises(bitstring.CreationError):
            _ = CBS('0xabc', pos=-13)

    def testStringRepresentation(self):
        s = CBS('0b110', pos=2)
        self.assertEqual(s.__repr__(), "ConstBitStream('0b110', pos=2)")

    def testStringRepresentationFromFile(self):
        filename = os.path.join(THIS_DIR, 'test.m1v')
        s = CBS(filename=filename, pos=2001)
        self.assertEqual(s.__repr__(), f"ConstBitStream(filename={repr(str(filename))}, length=1002400, pos=2001)")
        s.pos = 0
        self.assertEqual(s.__repr__(), f"ConstBitStream(filename={repr(str(filename))}, length=1002400)")
