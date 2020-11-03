from unittest import mock

import pytest
import gnucash

from context import gnucash_laska as gncl

def test_get_dummy_session():
    s = gncl.get_dummy_session()
    assert isinstance(s, gnucash.gnucash_core.Session)

def test_get_dummy_book():
    b = gncl.get_dummy_book()
    assert isinstance(b, gnucash.gnucash_core.Book)

def test_get_dummy_commodity_table():
    c = gncl.get_dummy_commodity_table()
    assert isinstance(c, gnucash.gnucash_core.GncCommodityTable)

class TestIsValidCurrency:

    @pytest.mark.parametrize(
        "valid_currency",
        ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG",
         "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND"])
    def test_valid(self, valid_currency):
        assert gncl.is_valid_currency(valid_currency) == True

    @pytest.mark.parametrize(
        "invalid_currency",
        ["LOL", "HOH", "DOH", "MOH", "TOD", "usd", "nrs",
         "asdf", "name of currency", "Nepalese Rupee", "$",])
    def test_invalid(self, invalid_currency):
        assert gncl.is_valid_currency(invalid_currency) == False

    @pytest.mark.parametrize(
        "invalid_input",
        [None, 1, mock.Mock()])
    def test_invalid_input(self, invalid_input):
        with pytest.raises(ValueError):
            gncl.is_valid_currency(invalid_input)

class TestIsValidAccountSpecification:

    @pytest.mark.parametrize(
        "account_spec",
        ["Assets",
         "Assets:Current Assets",
         "Assets:Current Assets:Cash in Wallet",
         "Assets:Current Assets:Cash in Wallet:Unicode नाम"])
    def test_correct_inputs(self, account_spec):
        assert gncl.is_valid_account_specification(account_spec) == True

    @pytest.mark.parametrize(
        "account_spec",
        [" Assets",
         "Assets ",
         "Assets:",
         "Assets: Current Assets",
         "Assets:Current Assets :Cash in Wallet",
         "Assets:Current Assets:Cash in Wallet:Unicode नाम:"])
    def test_slightly_incorrect_inputs(self, account_spec):
        assert gncl.is_valid_account_specification(account_spec) == False
