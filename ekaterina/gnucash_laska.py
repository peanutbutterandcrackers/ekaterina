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
    # Previous Solution:
    #     proper_spec = re.compile(
    #         r"^"
    #         r"(?P<RootAccount>[^ ]([^:])+[^ :])"
    #         r"("
    #         r"(:(?=(?P<SubAccount>[^ ]([^:])+[^ :])))"
    #         r"(?P=SubAccount)"
    #         r")*"
    #         r"$"
    #     )
    # return bool(proper_spec.match(account))
    # Regex Explanation:
    # r"^"
    #    Start of string
    # r"(?P<RootAccount>[^ ]([^:])+[^ :])"
    #    Named Pattern: [^ ] -> does not start with a space
    #                   ([^:])+ -> does not match ':'
    #                   [^ :] -> does not end with a space or a ':'
    # r"("
    #    Start a group
    # r"(:(?=(?P<SubAccount>[^ ]([^:])+[^ :])))"
    #    Match ':' only if it is followed by an account-name pattern
    # r"(?P=SubAccount)"
    #    Match the named pattern that followed the ':' previously
    # r")*"
    #    Close the group and make it optional
    # r"$"
    #    End of string
    # Caveats:
    # (Sub)-Account name must be at least 4 characters long. Fix this.
    # -----------------------------------------------------------
    # I'm still keeping this regex, for now, because I'd like to atleast
    # have it in git history as a note to go back to, just so.
    # ------------------------------------------------------------
    assert isinstance(account, str), "Expecting String."

    import re
    return not False in list(
        map(
            (lambda substr:
             (substr.strip() == substr and
              bool(re.match(r"^[^:]+$", substr)))),
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
