from unittest import TestCase

from buidl.ecc import FieldElement, Point, G, N, S256Point, PrivateKey, Signature
from buidl.helper import decode_bech32

from random import randint


class FieldElementTest(TestCase):
    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        self.assertEqual(a + b, FieldElement(17, 31))
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_pow(self):
        a = FieldElement(17, 31)
        self.assertEqual(a ** 3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a ** 5 * b, FieldElement(16, 31))

    def test_div(self):
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a ** -3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a ** -4 * b, FieldElement(13, 31))


class PointTest(TestCase):
    def test_ne(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_on_curve(self):
        with self.assertRaises(ValueError):
            Point(x=-2, y=4, a=5, b=7)
        # these should not raise an error
        Point(x=3, y=-7, a=5, b=7)
        Point(x=18, y=77, a=5, b=7)

    def test_add0(self):
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        a = Point(x=-1, y=1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=-77, a=5, b=7))


class ECCTest(TestCase):
    def test_on_curve(self):
        # tests the following points whether they are on the curve or not
        # on curve y^2=x^3-7 over F_223:
        # (192,105) (17,56) (200,119) (1,193) (42,99)
        # the ones that aren't should raise a ValueError
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))

        # iterate over valid points
        for x_raw, y_raw in valid_points:
            # Initialize points this way:
            # x = FieldElement(x_raw, prime)
            # y = FieldElement(y_raw, prime)
            # Point(x, y, a, b)
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            # Creating the point should not result in an error
            Point(x, y, a, b)

        # iterate over invalid points
        for x_raw, y_raw in invalid_points:
            # Initialize points this way:
            # x = FieldElement(x_raw, prime)
            # y = FieldElement(y_raw, prime)
            # Point(x, y, a, b)
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            # check that creating the point results in a ValueError
            # with self.assertRaises(ValueError):
            #     Point(x, y, a, b)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        # tests the following additions on curve y^2=x^3-7 over F_223:
        # (192,105) + (17,56)
        # (47,71) + (117,141)
        # (143,98) + (76,66)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        additions = (
            # (x1, y1, x2, y2, x3, y3)
            (192, 105, 17, 56, 170, 142),
            (47, 71, 117, 141, 60, 139),
            (143, 98, 76, 66, 47, 71),
        )
        # iterate over the additions
        for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
            # Initialize points this way:
            # x1 = FieldElement(x1_raw, prime)
            # y1 = FieldElement(y1_raw, prime)
            # p1 = Point(x1, y1, a, b)
            # x2 = FieldElement(x2_raw, prime)
            # y2 = FieldElement(y2_raw, prime)
            # p2 = Point(x2, y2, a, b)
            # x3 = FieldElement(x3_raw, prime)
            # y3 = FieldElement(y3_raw, prime)
            # p3 = Point(x3, y3, a, b)
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            x2 = FieldElement(x2_raw, prime)
            y2 = FieldElement(y2_raw, prime)
            p2 = Point(x2, y2, a, b)
            x3 = FieldElement(x3_raw, prime)
            y3 = FieldElement(y3_raw, prime)
            p3 = Point(x3, y3, a, b)
            # check that p1 + p2 == p3
            self.assertEqual(p1 + p2, p3)

    def test_rmul(self):
        # tests the following scalar multiplications
        # 2*(192,105)
        # 2*(143,98)
        # 2*(47,71)
        # 4*(47,71)
        # 8*(47,71)
        # 21*(47,71)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            # (coefficient, x1, y1, x2, y2)
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
            # Initialize points this way:
            # x1 = FieldElement(x1_raw, prime)
            # y1 = FieldElement(y1_raw, prime)
            # p1 = Point(x1, y1, a, b)
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            # initialize the second point based on whether it's the point at infinity
            # x2 = FieldElement(x2_raw, prime)
            # y2 = FieldElement(y2_raw, prime)
            # p2 = Point(x2, y2, a, b)
            if x2_raw is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)
            # check that the product is equal to the expected point
            self.assertEqual(s * p1, p2)


class S256Test(TestCase):
    def test_order(self):
        point = N * G
        self.assertIsNone(point.x)

    def test_pubpoint(self):
        # write a test that tests the public point for the following
        points = (
            # secret, x, y
            (
                7,
                0x5CBDF0646E5DB4EAA398F365F2EA7A0E3D419B7E0330E39CE92BDDEDCAC4F9BC,
                0x6AEBCA40BA255960A3178D6D861A54DBA813D0B813FDE7B5A5082628087264DA,
            ),
            (
                1485,
                0xC982196A7466FBBBB0E27A940B6AF926C1A74D5AD07128C82824A11B5398AFDA,
                0x7A91F9EAE64438AFB9CE6448A1C133DB2D8FB9254E4546B6F001637D50901F55,
            ),
            (
                2 ** 128,
                0x8F68B9D2F63B5F339239C1AD981F162EE88C5678723EA3351B7B444C9EC4C0DA,
                0x662A9F2DBA063986DE1D90C2B6BE215DBBEA2CFE95510BFDF23CBF79501FFF82,
            ),
            (
                2 ** 240 + 2 ** 31,
                0x9577FF57C8234558F293DF502CA4F09CBC65A6572C842B39B366F21717945116,
                0x10B49C67FA9365AD7B90DAB070BE339A1DAF9052373EC30FFAE4F72D5E66D053,
            ),
        )

        # iterate over points
        for secret, x, y in points:
            # initialize the secp256k1 point (S256Point)
            point = S256Point(x, y)
            # check that the secret*G is the same as the point
            self.assertEqual(secret * G, point)

    def test_sec(self):
        coefficient = 999 ** 3
        uncompressed = "049d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d56fa15cc7f3d38cda98dee2419f415b7513dde1301f8643cd9245aea7f3f911f9"
        compressed = (
            "039d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d5"
        )
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))
        coefficient = 123
        uncompressed = "04a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5204b5d6f84822c307e4b4a7140737aec23fc63b65b35f86a10026dbd2d864e6b"
        compressed = (
            "03a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5"
        )
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))
        coefficient = 42424242
        uncompressed = "04aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e21ec53f40efac47ac1c5211b2123527e0e9b57ede790c4da1e72c91fb7da54a3"
        compressed = (
            "03aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e"
        )
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))

    def test_address(self):
        tests = (
            (
                888 ** 3,
                "148dY81A9BmdpMhvYEVznrM45kWN32vSCN",
                "mnabU9NCcRE5zcNZ2C16CnvKPELrFvisn3",
            ),
            (
                321,
                "1FNgueDbMYjNQ8HT77sHKxTwdrHMdTGwyN",
                "mfx3y63A7TfTtXKkv7Y6QzsPFY6QCBCXiP",
            ),
            (
                4242424242,
                "1HUYfVCXEmp76uh17bE2gA72Vuqv4wrM1a",
                "mgY3bVusRUL6ZB2Ss999CSrGVbdRwVpM8s",
            ),
        )
        for secret, mainnet_legacy, testnet_legacy in tests:
            point = secret * G
            self.assertEqual(point.address(testnet=False), mainnet_legacy)
            self.assertEqual(
                point.address(compressed=False, testnet=True), testnet_legacy
            )

    def test_bech32_address(self):
        tests = (
            (
                888 ** 3,
                "bc1qyfvunnpszmjwcqgfk9dsne6j4edq3fglx9y5x7",
                "tb1qyfvunnpszmjwcqgfk9dsne6j4edq3fglvrl8ad",
            ),
            (
                321,
                "bc1qnk4u7vkat6ck9t4unlgvvle8dhsqp40mrssamm",
                "tb1qnk4u7vkat6ck9t4unlgvvle8dhsqp40mfktwqg",
            ),
            (
                4242424242,
                "bc1qkjm6e3c79zy7clsfx86q4pvy46ccc5u9xa6f6e",
                "tb1qkjm6e3c79zy7clsfx86q4pvy46ccc5u9vmp6p2",
            ),
        )
        for secret, mainnet_bech32, testnet_bech32 in tests:
            point = secret * G
            self.assertEqual(point.bech32_address(testnet=False), mainnet_bech32)
            self.assertEqual(decode_bech32(mainnet_bech32)[2], point.hash160())
            self.assertEqual(point.bech32_address(testnet=True), testnet_bech32)

    def test_p2sh_p2wpkh_address(self):
        tests = (
            (
                888 ** 3,
                "32cE3VHX5k1Z4gDCJBXMSLgd1akUzvqNvH",
                "2MtAS7EDYhCWuGTqjyK9E4HftDvxek7ELQn",
            ),
            (
                321,
                "3KPpFmmGNoKi5ikrH4QsMNmNnQtzkdw4Kx",
                "2NAx2KWhHzFq4HWPPxC2jyKkdzm7AVsEge4",
            ),
            (
                4242424242,
                "3M7oCrExZ6ZYjyn2oxXxYnE14m813espco",
                "2NCg1GbAzAZ4twmQaV69qAjDGH7LApz5kA4",
            ),
        )
        for secret, mainnet_p2sh, testnet_p2sh in tests:
            point = secret * G
            self.assertEqual(point.p2sh_p2wpkh_address(testnet=False), mainnet_p2sh)
            self.assertEqual(point.p2sh_p2wpkh_address(testnet=True), testnet_p2sh)

    def test_verify(self):
        point = S256Point(
            0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C,
            0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34,
        )
        z = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
        r = 0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395
        s = 0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4
        self.assertTrue(point.verify(z, Signature(r, s)))
        z = 0x7C076FF316692A3D7EB3C3BB0F8B1488CF72E1AFCD929E29307032997A838A3D
        r = 0xEFF69EF2B1BD93A66ED5219ADD4FB51E11A840F404876325A1E8FFE0529A2C
        s = 0xC7207FEE197D27C618AEA621406F6BF5EF6FCA38681D82B2F06FDDBDCE6FEAB6
        self.assertTrue(point.verify(z, Signature(r, s)))

    def test_parse(self):
        sec = bytes.fromhex(
            "0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a"
        )
        point = S256Point.parse(sec)
        want = 0xA56C896489C71DFC65701CE25050F542F336893FB8CD15F4E8E5C124DBF58E47
        self.assertEqual(point.y.num, want)


class SignatureTest(TestCase):
    def test_der(self):
        testcases = (
            (1, 2),
            (randint(0, 2 ** 256), randint(0, 2 ** 255)),
            (randint(0, 2 ** 256), randint(0, 2 ** 255)),
        )
        for r, s in testcases:
            sig = Signature(r, s)
            der = sig.der()
            sig2 = Signature.parse(der)
            self.assertEqual(sig2.r, r)
            self.assertEqual(sig2.s, s)


class PrivateKeyTest(TestCase):
    def test_sign(self):
        pk = PrivateKey(randint(0, 2 ** 256))
        z = randint(0, 2 ** 256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))

    def test_sign_message(self):
        pk = PrivateKey(randint(0, 2 ** 256))
        message = b"This is a test message"
        sig = pk.sign_message(message)
        self.assertTrue(pk.point.verify_message(message, sig))
