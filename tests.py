conv_dict = {'0': 0, '1': 1, '2': 2, '3': 3,
             '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'a': 10, 'b': 11,
             'c': 12, 'd': 13, 'e': 14, 'f': 15}
# A map


def conv_num(num_str):
    """Function 1: Create num_str into a string for which
    handles empty cases. Handles strings of integers, floating
    point numbers, hexadecimal to determine their returned value
    of True or False. if True the representation will be returned.
    If False then returns None. Map for case insensitive."""
    num_str = num_str.strip().lower()
    if not len(num_str):
        return None
    neg: bool = num_str[0] == '-'
    if neg:
        num_str = num_str[1:]
    hex_num: bool = num_str[0:2] == '0x'
    if hex_num:
        num_str = num_str[2:]
    if not len(num_str) or num_str.count('.') > 1:
        return None
    result = 0
    power = (num_str.find('.') - len(num_str) + 1) if '.' in num_str else 0
    for pos in range(len(num_str) - 1, -1, -1):
        if num_str[pos] != '.':
            if not num_str[pos] in conv_dict.keys():
                return None
            if not hex_num and conv_dict[num_str[pos]] > 9:
                return None
            result = result + (conv_dict[num_str[pos]] * 16 ** power
                               if hex_num
                               else conv_dict[num_str[pos]] * 10 ** power)
            power += 1
    return -result if neg else result


int_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'A', 'B', 'C', 'D', 'E', 'F']


def conv_endian(num, endian='big'):
    """
    Takes a decimal integer and returns it as a hexadecimal string with an
    even number of bytes and spaces between the bytes. The value of the
    'endian' parameter determines whether the hex number displayed is in
    big or little endian form.
    """
    negative_flag = 0
    if num < 0:
        negative_flag = 1
        num = remove_minus(num)

    if num == 0:
        return '00'

    hex_rem = ''

    # While loop conversion algorithm found at https://pencilprogrammer.com
    # /python-programs/convert-decimal-to-hexadecimal/. Corresponds also to
    # algorithm pseudocode at https://www.permadi.com/tutorial/numDecToHex/.
    # My original work can be found in commit history. It was based on the
    # steps outlined in the binary to hex conversion wikiHow article linked
    # in the assignment page. My implementation had a bug that came to light
    # during random testing.
    while num > 0:
        rem = num % 16
        hex_rem = int_hex[rem] + hex_rem
        num = num // 16

    # if the hex number is odd, we'll have to add a zero to have even bytes.
    if len(hex_rem) % 2 != 0:
        hex_rem = '0' + hex_rem

    ret_value = add_spaces(hex_rem)
    ret_value = generate_return_val(ret_value, endian, negative_flag)
    return ret_value


def generate_return_val(ret_value, endian, negative_flag):
    """
    Helper function to simplify conv_endian function. Takes the converted
    hex string and adds a negative sign and/or reverses the bytes, depending
    on if the original number was negative or the endian flag is 'little'.
    """
    # String is already in big endian order and num > 0. Return.
    if endian == 'big':
        if negative_flag == 0:
            return ret_value

        # String is in big endian order but num is negative. Add '-' to number
        if negative_flag == 1:
            return add_minus(ret_value)

    # If endian is 'little', start by reversing the order of the string
    if endian == 'little':
        little_ret = reverse_bytes(ret_value)
        if negative_flag == 0:
            return little_ret

        # Original number was negative, add the popped minus at the front.
        if negative_flag == 1:
            return add_minus(little_ret)

    # If the endian parameter is invalid, return None.
    return


def add_spaces(num):
    """
    Helper function to add spaces after every two digits to symbolize bytes in
    hexadecimal form.
    """
    # create new string hex representation with spaces between the bytes.
    count = 0
    val = ""
    for i in range(len(num), 0, -1):

        i = i - 1  # correctly offsets index because we're iterating backward.
        if count == 1 and i != 0:
            val = ' ' + num[i] + val
            count = 0

        else:
            val = num[i] + val
            count += 1

    return val


def remove_minus(num):
    """
    Takes an int, converts it into a string, then a list, removes the
    negative sign, converts it back into an int, then returns it.
    """
    num = str(num)
    num = list(num)
    num.pop(0)
    num = ''.join(num)
    num = int(num)
    return num


def add_minus(num):
    """
    takes a string version of a number, converts it to a list, inserts
    a minus at the beginning, converts it back into a string and returns it.
    """
    num = list(num)
    num.insert(0, '-')
    num = ''.join(num)
    return num


def reverse_bytes(num):
    """
    Helper function to reverse the hexadecimal bytes and display number in
    Little endian order.
    """
    num = num[::-1]

    # change string into list of chars so we can swap byte order
    num = list(num)
    i = 0
    i2 = 1

    # Swap byte order, join result back into string
    while i2 < len(num):
        num[i], num[i2] = num[i2], num[i]
        i += 3
        i2 += 3

    num = ''.join(num)
    return num


def my_datetime(num_sec):
    """
    Function that takes in an int, the number of seconds that represents the
    number of seconds that elapsed since epoch - 01-01-1970 and returns the
    date as a string in MM-DD-YYYY format. Takes into account leap years
    """

    # seconds in a day
    sec_in_day = 86400
    # days in year
    days_in_year = 365

    # variables that will hold the yr
    cur_yr = 1970

    # calculate total number of days
    # + 1 since we are taking the floor, if less than 86400
    tot_days = (num_sec // sec_in_day) + 1

    # if total days are greater than the days in yr, means we have 1 yr
    while tot_days >= days_in_year:
        cur_yr += 1
        # check
        if is_leap(cur_yr):
            tot_days = tot_days - 1 - days_in_year

        else:
            tot_days = tot_days - days_in_year

    # now check leap year one more time
    leap_yr = is_leap(cur_yr)

    # holds our date cut off for each month
    # which will be used later to check the month and the date of the month
    months = []
    if leap_yr:
        tot_days += 1
        months = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    else:
        months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    # now get month and date
    cur_mth = get_month(tot_days, months)
    cur_d = get_date(tot_days, cur_mth, months)

    # now check for dec 31st
    # if dec and 31st, we need to decrement the year by 1
    if is_dec_31st(cur_d, cur_mth):
        cur_yr -= 1

    # create a list - makes it easier to join later
    datetime_cache = [add_leading_zero(cur_mth), add_leading_zero(cur_d),
                      str(cur_yr)]

    return '-'.join(datetime_cache)


def is_leap(year):
    """
    function that takes an integer value that represents the current year
    returns True or False if the year is a leap year
    """

    # if a year is divisible by 4 it is a leap year
    # except when it is divisible by 100
    # then it must be divisible by 400 too be a leap year

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True

    # Not a leap year if not evenly divisible by 4
    return False


def get_month(days, months):
    """
    days: takes in remaining days (int),
    months: list of days marking the last day of each month
    returns an integer: month based on the days remaining
    """

    # when we have no days remaining, that is a special case Dec. 31st
    if days == 0:
        return 12

    for i in range(1, len(months)):
        if days <= months[i]:
            return i


def get_date(days, month, months):
    """
    days: takes in remaining days (int),
    month: the current month (int)
    months: list of days marking the last day of each month
    returns and integer value for the day based on the month and days remaining
    """

    # when we have no days remaining, that is a special case Dec. 31st
    if days == 0:
        return 31

    return days - months[month - 1]


def add_leading_zero(n):
    """
    takes an int and converts it to a string and
    adds a leading zero to it if the int is less than 10
    else it just turns it into a string and returns it
    """

    if n < 10:
        return '0' + str(n)
    else:
        return str(n)


def is_dec_31st(d, m):
    """
    function that takes the date (int) and month (int) and checks if
    it is the 31st and December if so return True, else false
    """

    if d == 31 and m == 12:
        return True

    return False
