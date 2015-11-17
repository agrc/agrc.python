import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from agrc import parse_address

add = '123 S Main Street'
dic = {
    'N': ['NORTH', 'NO']
}


class ParseAddressTests(unittest.TestCase):
    def test_getSuffixTypes(self):
        self.assertEqual(parse_address.sTypes['ALY'], ['ALLEE', 'ALLEY', 'ALLY', 'ALY'])
        with self.assertRaises(KeyError):
            parse_address.sTypes['PostalServiceStandardSuffixAbbreviation']

    def test_returnNormalizedAddress(self):
        result = parse_address.parse('123 S Main Street')

        self.assertIsInstance(result, parse_address.NormalizedAddress)

    def test_houseNumber(self):
        result = parse_address.parse(add)

        self.assertEqual(result.houseNumber, '123')

    def test_whiteSpace(self):
        result = parse_address.parse(' 123 S Main Street ')

        self.assertEqual(result.houseNumber, '123')

    def test_prefixDirection(self):
        result = parse_address.parse(add)

        self.assertEqual(result.prefixDirection, 'S')

    def test_streetName(self):
        result = parse_address.parse(add)

        self.assertEqual(result.streetName, 'MAIN')

    def test_multiWordStreetName(self):
        result = parse_address.parse('123 S Main Hello Street')

        self.assertEqual(result.streetName, 'MAIN HELLO')

    def test_noPrefixDirectionStreetName(self):
        result = parse_address.parse('123 Main Street')

        self.assertEqual(result.streetName, 'MAIN')
        self.assertIsNone(result.prefixDirection)

    def test_suffixDirection(self):
        result = parse_address.parse('123 E 400 N')

        self.assertEqual(result.suffixDirection, 'N')
        self.assertIsNone(result.suffixType)

    def test_normalizedAddressString(self):
        result = parse_address.parse('123 EA Fifer Place ')

        self.assertEqual(result.normalizedAddressString, '123 E FIFER PL')

        result = parse_address.parse(' 123 east 400 w  ')

        self.assertEqual(result.normalizedAddressString, '123 E 400 W')

    def test_doubleSpaces(self):
        result = parse_address.parse('  123  ea main  st')

        self.assertEqual(result.houseNumber, '123')
        self.assertEqual(result.prefixDirection, 'E')
        self.assertEqual(result.streetName, 'MAIN')
        self.assertEqual(result.suffixType, 'ST')

    def test_noPreDir(self):
        result = parse_address.parse('1901 Sidewinder Dr')

        self.assertEqual(result.houseNumber, '1901')
        self.assertEqual(result.prefixDirection, None)
        self.assertEqual(result.streetName, 'SIDEWINDER')
        self.assertEqual(result.suffixType, 'DR')
        self.assertEqual(result.suffixDirection, None)
        self.assertEqual(result.normalizedAddressString, '1901 SIDEWINDER DR')

    def test_stripPeriods(self):
        result = parse_address.parse('  123 ea main st.')

        self.assertEqual(result.houseNumber, '123')
        self.assertEqual(result.prefixDirection, 'E')
        self.assertEqual(result.streetName, 'MAIN')
        self.assertEqual(result.suffixType, 'ST')
        self.assertEqual(result.suffixDirection, None)
        self.assertEqual(result.normalizedAddressString, '123 E MAIN ST')

    # tests from Steve's geocoder...
    def test_steves(self):
        result = parse_address.parse("5301 w jacob hill cir")
        self.assertEqual('5301', result.houseNumber)
        self.assertEqual("JACOB HILL", result.streetName)
        self.assertEqual('CIR', result.suffixType)

        result = parse_address.parse("400 S 532 E")
        self.assertEqual('400', result.houseNumber)
        self.assertEqual("532", result.streetName)
        self.assertEqual('E', result.suffixDirection)

        result = parse_address.parse("5625 S 995 E")
        self.assertEqual('5625', result.houseNumber)
        self.assertEqual("995", result.streetName)
        self.assertEqual('E', result.suffixDirection)

        result = parse_address.parse("372 North 600 East")
        self.assertEqual('372', result.houseNumber)
        self.assertEqual("600", result.streetName)
        self.assertEqual('E', result.suffixDirection)

        result = parse_address.parse("30 WEST 300 NORTH")
        self.assertEqual('30', result.houseNumber)
        self.assertEqual("300", result.streetName)
        self.assertEqual('N', result.suffixDirection)

        result = parse_address.parse("126 E 400 N")
        self.assertEqual('126', result.houseNumber)
        self.assertEqual("400", result.streetName)
        self.assertEqual('N', result.suffixDirection)

        result = parse_address.parse("270 South 1300 East")
        self.assertEqual('270', result.houseNumber)
        self.assertEqual("1300", result.streetName)
        self.assertEqual('E', result.suffixDirection)

        result = parse_address.parse("126 W SEGO LILY DR")
        self.assertEqual('126', result.houseNumber)
        self.assertEqual("SEGO LILY", result.streetName)
        self.assertEqual('DR', result.suffixType)

        result = parse_address.parse("261 E MUELLER PARK RD")
        self.assertEqual('261', result.houseNumber)
        self.assertEqual("MUELLER PARK", result.streetName)
        self.assertEqual('RD', result.suffixType)

        result = parse_address.parse("17 S VENICE MAIN ST")
        self.assertEqual('17', result.houseNumber)
        self.assertEqual("VENICE MAIN", result.streetName)
        self.assertEqual('ST', result.suffixType)

        result = parse_address.parse("20 W Center St")
        self.assertEqual('20', result.houseNumber)
        self.assertEqual('W', result.prefixDirection)
        self.assertEqual("CENTER", result.streetName)
        self.assertEqual('ST', result.suffixType)

        result = parse_address.parse("9314 ALVEY LN")
        self.assertEqual('9314', result.houseNumber)
        self.assertEqual("ALVEY", result.streetName)
        self.assertEqual('LN', result.suffixType)

        result = parse_address.parse("167 DALY AVE")
        self.assertEqual('167', result.houseNumber)
        self.assertEqual("DALY", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1147 MCDANIEL CIR")
        self.assertEqual('1147', result.houseNumber)
        self.assertEqual("MCDANIEL", result.streetName)
        self.assertEqual('CIR', result.suffixType)

        result = parse_address.parse("300 Walk St")
        self.assertEqual('300', result.houseNumber)
        self.assertEqual("WALK", result.streetName)
        self.assertEqual('ST', result.suffixType)

        result = parse_address.parse("5 Cedar Ave")
        self.assertEqual('5', result.houseNumber)
        self.assertEqual("CEDAR", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1238 E 1ST Avenue")
        self.assertEqual('1238', result.houseNumber)
        self.assertEqual("1ST", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1238 E FIRST Avenue")
        self.assertEqual('1238', result.houseNumber)
        self.assertEqual("FIRST", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1238 E 2ND Avenue")
        self.assertEqual('1238', result.houseNumber)
        self.assertEqual("2ND", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1238 E 3RD Avenue")
        self.assertEqual('1238', result.houseNumber)
        self.assertEqual("3RD", result.streetName)
        self.assertEqual('AVE', result.suffixType)

        result = parse_address.parse("1573 24TH Street")
        self.assertEqual('1573', result.houseNumber)
        self.assertEqual("24TH", result.streetName)
        self.assertEqual('ST', result.suffixType)

        # if you dont' have a street name but you have a prefix direction then the
        # prefix diretion is probably the street name.
        result = parse_address.parse("168 N ST")
        self.assertEqual('168', result.houseNumber)
        self.assertEqual("N", result.streetName)
        self.assertEqual('ST', result.suffixType)

        result = parse_address.parse("168 N N ST")
        self.assertEqual('168', result.houseNumber)
        self.assertEqual("N", result.streetName)
        self.assertEqual('ST', result.suffixType)

        result = parse_address.parse("478 S WEST FRONTAGE RD")
        self.assertEqual('478', result.houseNumber)
        self.assertEqual("WEST FRONTAGE", result.streetName)
        self.assertEqual('RD', result.suffixType)

        result = parse_address.parse("1048 W 1205 N")
        self.assertEqual('1048', result.houseNumber)
        self.assertEqual("1205", result.streetName)
        self.assertEqual(None, result.suffixType)
        self.assertEqual('N', result.suffixDirection)

        result = parse_address.parse("2139 N 50 W")
        self.assertEqual('2139', result.houseNumber)
        self.assertEqual("50", result.streetName)
        self.assertEqual(None, result.suffixType)
        self.assertEqual('W', result.suffixDirection)

    def test_streetTypeNames(self):
        result = parse_address.parse('123 E PARKWAY AVE')

        self.assertEqual(result.houseNumber, '123')
        self.assertEqual(result.prefixDirection, 'E')
        self.assertEqual(result.streetName, 'PARKWAY')
        self.assertEqual(result.suffixType, 'AVE')
        self.assertEqual(result.suffixDirection, None)
        self.assertEqual(result.normalizedAddressString, '123 E PARKWAY AVE')

        result = parse_address.parse('123 E PARKWAY TRAIL AVE')

        self.assertEqual(result.houseNumber, '123')
        self.assertEqual(result.prefixDirection, 'E')
        self.assertEqual(result.streetName, 'PARKWAY TRAIL')
        self.assertEqual(result.suffixType, 'AVE')
        self.assertEqual(result.suffixDirection, None)
        self.assertEqual(result.normalizedAddressString, '123 E PARKWAY TRAIL AVE')


class checkWordTests(unittest.TestCase):

    def test_returnNormalizedValue(self):
        self.assertEqual(parse_address.checkWord('NO', dic), 'N')
        self.assertEqual(parse_address.checkWord('NORTH', dic), 'N')

    def test_returnFalse(self):
        self.assertFalse(parse_address.checkWord('blah', dic))


class NormalizedAddressTests(unittest.TestCase):

    def test_getPreviousWord(self):
        word = 'blah'
        lastWord = 'last'
        add = 'hello {} {}'.format(word, lastWord)

        nAdd = parse_address.NormalizedAddress(add)

        self.assertEqual(nAdd.getPreviousWord(lastWord), word.upper())

    def test_none(self):
        result = parse_address.parse("2819 E Louise")
        self.assertEqual('2819 E LOUISE', result.normalizedAddressString)


if __name__ == '__main__':
    unittest.main()
