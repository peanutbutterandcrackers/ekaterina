import decimal
import datetime
from unittest import mock

import pytest

from context import classes

@pytest.fixture
def random_ID():
    from random import randint
    return randint(0, 999999)

@pytest.fixture
def random_name():
    from random import choice
    return choice(
        ["Anna Karenina",
         "Alexei Alexandrovich Karenin",
         "Darya 'Dolly' Alexandrovna Oblonskaya",
         "Stepan 'Stiva' Arkadyevich Oblonsky"])

@pytest.fixture
def mock_customer(random_name, random_ID):
    customer = mock.Mock(classes.Customer)
    customer.__eq__ = classes.Customer.__eq__
    customer.name = random_name
    customer.ID = random_ID
    return customer

@pytest.fixture
def mock_currency():
    currency = mock.Mock(classes.Currency)
    currency.__eq__ = classes.Currency.__eq__
    currency.currency = "NPR"
    return currency

@pytest.fixture
def mock_sale(mock_customer, mock_currency):
    sale = mock.Mock(classes.Sale)
    sale.customer = mock_customer
    sale.description = "Description"
    sale.quantity = 1
    sale.unitprice = decimal.Decimal(100)
    sale.notes = "Notes"
    sale.income_account = mock.Mock(classes.Account)
    sale.date = datetime.date.today()
    sale.currency = mock_currency
    return sale

@pytest.fixture
def mock_saleslist(mock_sale):
    from copy import deepcopy
    from random import randint
    saleslist = mock.Mock(classes.SalesList)
    saleslist.sales = (deepcopy(mock_sale) for x in range(randint(1, 7)))
    saleslist.customer = mock_sale.customer
    saleslist.currency = mock_sale.currency
    return saleslist

class TestAccount:

    @pytest.mark.parametrize("account",
                             ["Assets", "Assets:Petty Cash",
                              "Assets:Bank Account:This thing account",
                              "We:ev en:haz:u n i code:here:हेर हेर साथी"])
    def test_init_normal(self, account):
        acc = classes.Account(account)

    @pytest.mark.parametrize("account",
                             ["Assets", "Assets:Current Assets:Cash In Wallet",
                              "Root:Sub Root:युनिकोड Characters"])
    def test_str(self, account):
        assert str(classes.Account(account)) == account

class TestCurrency:

    def test_init_normal(self):
        NPR = classes.Currency("NPR")

    def test_init_invalid(self):
        with pytest.raises(AssertionError):
            c = classes.Currency(1)

    def test_init_not_currency(self):
        with pytest.raises(AssertionError, match=r"(?i)Invalid Currency"):
            c = classes.Currency("NRS")

    def test_str(self):
        USD = classes.Currency("USD")
        assert str(USD) == "USD"

class TestCustomer:

    def test_init_normal(self, random_name, random_ID):
        customer = classes.Customer(random_name, random_ID)

    @pytest.mark.parametrize("badname", [1, None, "validname"])
    @pytest.mark.parametrize("badID", ["001", 1.5, None, -1])
    def test_invalid_init(self, badname, badID):
        with pytest.raises(AssertionError):
            classes.Customer(badname, badID)

    @pytest.mark.parametrize("id,expect",
                             [(0, "000000"), (1, "000001"), (999999, "999999")])
    def test_ID_handling(self, id, expect):
        customer = classes.Customer("asdf", id)
        assert customer.ID == expect

    def test_equality_equal(self):
        customer1 = classes.Customer("asdf", 1)
        customer2 = classes.Customer("asdf", 1)
        assert customer1 == customer2

    def test_equality_not_equal(self):
        Customer = classes.Customer
        assert Customer("asdf", 1) != Customer("asdf", 2)
        assert Customer("Asdf", 1) != Customer("asdf", 1)
        assert Customer("jkl;", 2) != Customer("asdf", 2)

class TestSale:

    def test_init_normal(self):
        sale = classes.Sale(customer=mock.Mock(classes.Customer),
                            description="Potato Chips",
                            quantity=3,
                            unitprice=decimal.Decimal(40),
                            notes="Random Notes",
                            income_account=mock.Mock(classes.Account),
                            date=datetime.date.today(),
                            currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_customer",
                             ["Count Vronsky", None, False, 12345, mock.Mock()])
    def test_invalid_customer(self, invalid_customer):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=invalid_customer,
                description=mock.Mock(str),
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_description",
                             [None, 1234, mock.Mock(), False])
    def test_invalid_description(self, invalid_description):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=invalid_description,
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_quantity",
                             [None, False, mock.Mock()])
    def test_invalid_quantity(self, invalid_quantity):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=invalid_quantity,
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_unitprice",
                             [1, 23948, 123.34, None, False, mock.Mock()])
    def test_invalid_unitprice(self, invalid_unitprice):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=mock.Mock(str),
                unitprice=invalid_unitprice,
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_notes",
                             [None, 1234, mock.Mock(), False])
    def test_invalid_notes(self, invalid_notes):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=invalid_notes,
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_income_account",
                             ["String", None, 1234, mock.Mock(), False])
    def test_invalid_income_account(self, invalid_income_account):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=invalid_income_account,
                date=mock.Mock(datetime.date),
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_date",
                             ["String", None, 1234, mock.Mock(), False])
    def test_invalid_date(self, invalid_date):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=invalid_date,
                currency=mock.Mock(classes.Currency))

    @pytest.mark.parametrize("invalid_currency",
                             ["String", None, 1234, mock.Mock(), False])
    def test_invalid_currency(self, invalid_currency):
        with pytest.raises(AssertionError):
            classes.Sale(
                customer=mock.Mock(classes.Customer),
                description=mock.Mock(str),
                quantity=mock.Mock(int),
                unitprice=mock.Mock(decimal.Decimal),
                notes=mock.Mock(str),
                income_account=mock.Mock(classes.Account),
                date=mock.Mock(datetime.date),
                currency=invalid_currency)

class TestSalesList:

    def test_init_normal(self, mock_sale):
        from copy import deepcopy
        sale1 = deepcopy(mock_sale)
        sale2 = deepcopy(mock_sale)
        sales_list = classes.SalesList(mock_sale, mock_sale, mock_sale)

    def test_init_empty(self):
        with pytest.raises(ValueError):
            sales_list = classes.SalesList()

    def test_init_different_customer(self, mock_sale):
        from copy import deepcopy
        sale1 = deepcopy(mock_sale)
        sale2 = deepcopy(mock_sale)
        sale3 = deepcopy(mock_sale)
        sale4 = deepcopy(mock_sale)
        sale5 = deepcopy(mock_sale)
        sale5.customer = mock.Mock()
        with pytest.raises(AssertionError):
            sales_list = classes.SalesList(sale1, sale2, sale3, sale4, sale5)

    def test_init_different_currency(self, mock_sale):
        from copy import deepcopy
        sale1 = deepcopy(mock_sale)
        sale2 = deepcopy(mock_sale)
        sale2.currency = mock.Mock()
        with pytest.raises(AssertionError):
            sales_list = classes.SalesList(sale1, sale2)

class TestInvoice:

    def test_init_normal(self, mock_customer, mock_saleslist):
        customer = mock_customer
        sales = mock_saleslist
        today = datetime.date.today()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        Invoice1 = classes.Invoice(customer=customer, sales=sales)
        Invoice2 = classes.Invoice(mock_customer, sales)
        Invoice3 = classes.Invoice(mock_customer, sales, today)
        Invoice4 = classes.Invoice(mock_customer, sales, today, tomorrow)
