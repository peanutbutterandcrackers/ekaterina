"""
Laska: Konstantin "Kostya" Dmitrievich Levin's doggo in 'Anna Karenina'.

Utilities, wrappers, helper-functions around gnucash python.
"""
import gnucash

def get_dummy_session():
    """Returns a dummy GNUCash Session"""
    return gnucash.gnucash_core.Session()

def get_dummy_book():
    """Returns a dummy GNUCash Book"""
    return get_dummy_session().book

def get_dummy_commodity_table():
    """Return a dummy GNUCash Commodity table"""
    return get_dummy_book().get_table()

def is_valid_currency(currency_code):
    """Return whether or not given currency_code is a valid
       currency or not."""
    if not isinstance(currency_code, str):
        raise ValueError("Expected 3 (uppercase) letter currency code.")
    return bool(get_dummy_commodity_table()
                .lookup("CURRENCY",
                        currency_code))

def is_valid_account_specification(account):
    """
    Return whether or not the given account specification is
    a valid one, based on the specification format. Account
    specification should match the format seen in GNUCash.
    i.e. "Root Account:Sub Account:Sub-Sub Account"

    Note: This test is merely regular expression based.

    >>> is_valid_account_specification("Assets")
    True
    >>> is_valid_account_specification("Assets:Cash in wallet")
    True
    >>> is_valid_account_specification("Assets: Poorly formatted sub:")
    False
    """
    assert isinstance(account, str), "Expecting String."

    return not False in list(
        map(
            (lambda substr:
             (substr.strip() == substr
              # "Asdf:" splits to ["Asdf", ""] (and pass this test)
              # so make sure that there are no empty strings in the
              # splited list.
              and substr != ""
              and ":" not in substr)),
            account.split(":")))

# The following is adapted from GNUCash API doxygen Docs
def gnc_numeric_from_decimal(decimal_value):
    """Return a gnucash.GncNumeric() when given a decimal.Decimal()"""
    from decimal import Decimal
    from gnucash import GncNumeric
    sign, digits, exponent = decimal_value.as_tuple()
    # convert decimal digits to a fractional numerator
    # equivlent to
    # numerator = int(''.join(digits))
    # but without the wated conversion to string and back,
    # this is probably the same algorithm int() uses
    numerator = 0
    TEN = int(Decimal(0).radix()) # this is always 10
    numerator_place_value = 1
    # add each digit to the final value multiplied by the place value
    # from least significant to most sigificant
    for i in range(len(digits)-1,-1,-1):
        numerator += digits[i] * numerator_place_value
        numerator_place_value *= TEN

    if decimal_value.is_signed():
        numerator = -numerator

    # if the exponent is negative, we use it to set the denominator
    if exponent < 0 :
        denominator = TEN ** (-exponent)
        # if the exponent isn't negative, we bump up the numerator
        # and set the denominator to 1
    else:
        numerator *= TEN ** exponent
        denominator = 1

    return GncNumeric(numerator, denominator)
