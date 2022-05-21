import unittest
import random
from task import conv_num
from datetime import datetime
from task import conv_endian
from task import remove_minus
from task import add_spaces
from task import generate_return_val
from task import my_datetime


class TestCase(unittest.TestCase):

    # Empty String and negative
    def test1_fun1(self):
        val = ''
        self.assertIsNone(conv_num(val))

    def test2_fun1(self):
        val = '-'
        self.assertIsNone(conv_num(val))

    # Test for -0x and 0x
    def test3_fun1(self):
        val = '-0x'
        self.assertIsNone(conv_num(val))

    def test4_fun1(self):
        val = '0x'
        self.assertIsNone(conv_num(val))

    # Test String of an Integer + and -
    def test5_fun1(self):
        val = '64731'
        self.assertEqual(conv_num(val), 64731)

    def test6_fun1(self):
        val = '-64731'
        self.assertEqual(conv_num(val), -64731)

    # Test Float with with decimal
    def test7_fun1(self):
        val = '647.31'
        self.assertEqual(conv_num(val), 647.31)

    def test8_fun1(self):
        val = '647.'
        self.assertEqual(conv_num(val), 647.0)

    def test9_fun1(self):
        val = '0647'
        self.assertEqual(conv_num(val), 647)

    def test10_fun1(self):
        val = '.31'
        self.assertAlmostEqual(conv_num(val), 0.31)

    def test11_fun1(self):
        val = '64.7.31'
        self.assertIsNone(conv_num(val))

    # Test Hexadecimal in multiple settings
    def test12_fun1(self):
        val = '0xCF5'
        self.assertEqual(conv_num(val), 3317)

    def test13_fun1(self):
        val = '-0xAB'
        self.assertEqual(conv_num(val), -171)

    def test14_fun1(self):
        val = '0xFH5'
        self.assertIsNone(conv_num(val))

    def test15_fun1(self):
        val = '0xF.5'
        self.assertEqual(conv_num(val), 15.3125)

    def test16_fun1(self):
        val = '0xfH5'
        self.assertIsNone(conv_num(val))

    def test17_fun1(self):
        val = '64731F'
        self.assertIsNone(conv_num(val))

    def test18_fun1(self):
        val = '0xcf5'
        self.assertEqual(conv_num(val), 3317)

    def test19_fun1(self):
        val = '0x-CF5'
        self.assertIsNone(conv_num(val))

    # random testing
    def test20_fun1(self):
        for x in range(1000000):
            hex_value = random.randint(-0xffffffff, 0xffffffff)
            self.assertEqual(hex_value, conv_num(str(hex(hex_value))))

    def test21_fun1(self):
        for x in range(1000000):
            round_fl = random.uniform(-.99999999, .99999999)
            self.assertAlmostEqual(round_fl, conv_num(f'{round_fl:.16f}'))

    def test22_fun1(self):
        for x in range(1000000):
            int_value = random.randint(-99999999, 99999999)
            self.assertEqual(int_value, conv_num(str(int_value)))

    def test1_fun3(self):
        num = 954786
        self.assertEqual('0E 91 A2', conv_endian(num))

    def test2_fun3(self):
        num = 954786
        self.assertEqual('A2 91 0E', conv_endian(num, 'little'))

    def test3_fun3(self):
        num = 954786
        self.assertEqual(None, conv_endian(num, 'teeny'))

    def test4_fun3(self):
        num = 0
        self.assertEqual('00', conv_endian(num, 'big'))

    def test5_fun3(self):
        num = 0
        self.assertEqual('00', conv_endian(num, 'little'))

    def test6_fun3(self):
        num = 0
        self.assertEqual('00', conv_endian(num))

    def test6_1_fun3(self):
        num = -0
        self.assertEqual('00', conv_endian(num))

    def test7_fun3(self):
        num = 954786
        self.assertEqual('0E 91 A2', conv_endian(num, 'big'))

    def test8_fun3(self):
        num = -56789
        self.assertEqual('-DD D5', conv_endian(num))

    def test9_fun3(self):
        num = 56789
        self.assertEqual('D5 DD', conv_endian(num, 'little'))

    def test10_fun3(self):
        num = -954786
        self.assertEqual('-0E 91 A2', conv_endian(num, 'big'))

    def test11_fun3(self):
        num = -954786
        self.assertEqual('-A2 91 0E', conv_endian(num, 'little'))

    def test12_fun3(self):
        num = 954786
        self.assertEqual(self.test22_fun3(num), conv_endian(num))

    def test13_fun3(self):
        num = 12357
        self.assertEqual(self.test22_fun3(num), conv_endian(num))

    def test14_fun3(self):
        num = -9999999
        self.assertEqual(self.test22_fun3(num, 'little'),
                         conv_endian(num, 'little'))

    def test15_fun3(self):
        num = 954786
        self.assertEqual(self.test22_fun3(num, 'little'),
                         conv_endian(num, 'little'))

    def test16_fun3(self):
        num = 954786
        self.assertEqual(self.test22_fun3(num, 'big'),
                         conv_endian(num, 'big'))

    def test17_fun3(self):
        num = 255
        self.assertEqual(self.test22_fun3(num, 'big'),
                         conv_endian(num, 'big'))

    def test18_fun3(self):
        num = 67977
        self.assertEqual(self.test22_fun3(num, 'big'), conv_endian(num, 'big'))

    # Random tests comparing conv_endian with hex()
    def test19_fun3(self):
        n = 10000
        for i in range(n):
            num = random.randint(-9999999, 9999999)
            self.assertEqual(self.test22_fun3(num), conv_endian(num), num)

    # Random tests comparing conv_endian with hex()
    def test20_fun3(self):
        n = 10000
        for i in range(n):
            num = random.randint(-9999999, 9999999)
            self.assertEqual(self.test22_fun3(num, 'big'),
                             conv_endian(num, 'big'), num)

    # Random tests comparing conv_endian with hex()
    def test21_fun3(self):
        n = 10000
        for i in range(n):
            num = random.randint(-9999999, 9999999)
            self.assertEqual(self.test22_fun3(num, 'little'),
                             conv_endian(num, 'little'), num)

    def test22_fun3(self, num=1, endian='big'):
        """
        Test function using python built-in function hex() to compare results
        with from-scratch function conv_endian().
        """
        negative_flag = 0
        if num < 0:
            negative_flag = 1
            num = remove_minus(num)

        num = hex(num)
        num = list(str(num))

        # Remove 0x at beginning of hex number.
        num.pop(0), num.pop(0)

        # Change lowercase hex letters to uppercase, change to string form.
        for i in range(len(num)):
            if num[i].isalpha():
                num[i] = num[i].upper()

        num = ''.join(num)

        # if the hex number is odd, add a zero to have even bytes.
        if len(num) % 2 != 0:
            num = '0' + num

        val = add_spaces(num)
        val = generate_return_val(val, endian, negative_flag)
        return val

    def test1_fun2(self):
        epoch = '01-01-1970'
        self.assertEqual(epoch, my_datetime(0))

    def test2_fun2(self):
        self.assertEqual('11-29-1973', my_datetime(123456789))

    def test3_fun2(self):
        self.assertEqual('12-22-2282', my_datetime(9876543210))

    def test4_fun2(self):
        self.assertEqual('02-29-8360', my_datetime(201653971200))

    # testing edge case of yr 9999, the largest yr we have to deal with
    def test5_fun2(self):
        num_sec = 253400421600
        test_time = str(datetime.utcfromtimestamp(num_sec)
                        .strftime('%m-%d-%Y'))
        self.assertEqual(test_time, my_datetime(num_sec))

    # test a leap year and dec 31st
    def test6_fun2(self):
        # dec 31st 1994
        num_sec = 788853600
        test_time = str(datetime.utcfromtimestamp(num_sec)
                        .strftime('%m-%d-%Y'))
        self.assertEqual(test_time, my_datetime(num_sec))

    # test leap day
    def test7_fun2(self):
        # feb 29 9992
        num_sec = 253154959200
        test_time = str(datetime.utcfromtimestamp(num_sec)
                        .strftime('%m-%d-%Y'))
        self.assertEqual(test_time, my_datetime(num_sec))

    # testing january 1st
    def test8_fun2(self):
        # jan 1st 2050
        num_sec = 2524629600
        test_time = str(datetime.utcfromtimestamp(num_sec)
                        .strftime('%m-%d-%Y'))
        self.assertEqual(test_time, my_datetime(num_sec))

    # random testing using datetime's utcfromtimestamp module
    def test9_fun2(self):
        n = 20000
        for i in range(n):
            num_sec = random.randint(0, 9999999999)
            test_date = str(datetime.utcfromtimestamp(num_sec)
                            .strftime('%m-%d-%Y'))
            self.assertEqual(test_date, my_datetime(num_sec))


if __name__ == '__main__':
    unittest.main()
