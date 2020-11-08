"""
Custom classes to approximate GNUCash objects.

Ekaterina takes inputs from non-standard ways (CSV files for now),
parses them into an approximation of GNUCash objects (these things
here) and writes them to a given .gnucash file.

Since ekaterina is taking in transactions written in a certain form,
and adding it to the .gnucash file, en masse, we assume a few things:
The data file (csv, ods, etc) provides us with all the details about
the transaction, and that they are correctly formatted. However, we
do not know if the Customer("Vronsky") exists in the GNUCash book we
are going to write these transactions into. That is something we worry
about during the Mazurka (a Russian dance) - the actual writing to the
.gnucash file.

So what we have here is just a bunch of data structures to hold the
data in intermediate form. And these objects also act as a filter.
They are almost statically typed. We need to make absolutely sure that
no bad data passes through this stage.

The following classes will be referred to as ekaterina.X class.
"""
import re
import decimal
import datetime

from ekaterina.utils import gnucash_laska

class Account:

    """An intermediate form to hold GNUCash Account identifiers"""
    def __init__(self, account_identifier):
        assert isinstance(account_identifier, str)
        assert gnucash_laska.is_valid_account_specification(account_identifier)
        self.account = account_identifier

    def __str__(self):
        return self.account

    def get_account_identifier(self):
        """
        Same as self.account, but abstracting it so as to handle future changes
        """
        return self.account

class Currency:

    """An intermediate form for Currency"""
    def __init__(self, intl_curr_symbol):
        assert isinstance(intl_curr_symbol, str), "Expected string"
        assert gnucash_laska.is_valid_currency(intl_curr_symbol), "Invalid currency code."
        self.currency = intl_curr_symbol

    def __str__(self):
        return self.currency

    # See assertions in SalesList
    def __eq__(self, other):
        return self.currency == other.currency

class Customer:

    """An approximation of a GNUCash Customer"""
    def __init__(self, name, ID):
        assert isinstance(name, str), "Customer name must be a string"
        assert isinstance(ID, int), "Customer ID must be an integer"
        assert ID >= 0, "Customer ID can not be a negative integer"

        self.name = name
        self.ID = "%06d" % ID

    def __eq__(self, other):
        """We need this later on to compare whether or not two customers
           are indeed the same. (See assertions in the class Invoice)"""
        return self.name == other.name and self.ID == other.ID

    def getname(self):
        return self.name

    def getID(self):
        return self.ID

class Sale:

    """
    Sale (noun): an act of selling.
    Each Sale() object approximates a single entry in a GNUCash Invoice.
    A bunch of Sales (made to 1 customer) may go into an Invoice.
    """
    def __init__(self, customer, description, quantity, unitprice,
                 notes, income_account, date, currency):
        """
        Required Arguments:
        customer: Must be an ekaterina.Customer() instance
        description: Description of the sale
        quantity: Quantity sold
        unitprice: Price per unit. Must be a gnucash.GncNumeric()
        notes: Notes on the matter
        income_account: An ekaterina.Account() instance
        date: Date. Must be a datetime.date()
        currency: An ekaterina.Currency() instance
        """

        assert isinstance(customer, Customer)
        assert isinstance(description, str)
        assert not isinstance(quantity, bool)
        assert isinstance(quantity, int) or isinstance(quantity, float)
        assert isinstance(unitprice, decimal.Decimal)
        assert isinstance(notes, str)
        assert isinstance(income_account, Account)
        assert isinstance(date, datetime.date)
        assert isinstance(currency, Currency)

        self.customer = customer
        self.description = description
        self.quantity = quantity
        self.unitprice = unitprice
        self.notes = notes
        self.income_account = income_account
        self.date = date
        self.currency = currency

    def get_customer(self):
        return self.customer

    def get_currency(self):
        return self.currency

    def get_date(self):
        return self.date

    def get_description(self):
        return self.description

    def get_quantity(self):
        # Turns out, gnucash.* functions only take
        # gnu_numeric numbers. So fix that here.
        return gnucash_laska.gnc_numeric_from_decimal(
            decimal.Decimal(self.quantity))

    def get_unitprice(self):
        return gnucash_laska.gnc_numeric_from_decimal(
            self.unitprice)

    def get_notes(self):
        return self.notes

    def get_incomeaccount(self):
        return self.income_account

class SalesList:

    """
    A List of Sales.

    This class provides the necessary type-checking before a sales list
    is passed to an Invoice() constructor.
    """

    def __init__(self, *sales):
        if len(sales) == 0:
            raise ValueError("Must have non-zero arguments")
        for sale in sales:
            assert isinstance(sale, Sale), "Expected Sale Object"

        customer = sales[0].customer
        currency = sales[0].currency
        for sale in sales:
            assert sale.customer == customer, (
                "Expected Sale items to a single customer.")
            assert sale.currency == currency, (
                "All Sale items must transact in the same currency.")

        self.sales = sales
        self.customer = customer
        self.currency = currency

class Invoice:

    """
    An approximation of a GNUCash Invoice.

    A list of Sale()s to a single customer. A single Sale() object can make
    a GNUCash Invoice.
    """
    def __init__(self, customer, sales, postdate=None, duedate=None,
                 ReceivableAC=Account("Assets:Accounts Receivable"),
                 description=None):
        assert isinstance(customer, Customer)
        assert isinstance(sales, SalesList)
        if postdate and not isinstance(postdate, datetime.date):
            raise ValueError("postdate should be a datetime.date value")
        if duedate and not isinstance(duedate, datetime.date):
            raise ValueError("duedate should be a datetime.date value")
        assert customer == sales.customer
        assert isinstance(ReceivableAC, Account)
        if description:
            assert isinstance(description, str)

        self.customer = customer
        self.sales = sales
        self.postdate = postdate
        self.duedate = duedate
        self.ReceivableAC = ReceivableAC
        self.description = description

    def get_sales(self):
        return self.sales

    def get_entries(self):
        return self.sales

    def get_postdate(self):
        return self.postdate

    def get_duedate(self):
        return self.duedate

    def get_description(self):
        return self.description

    def get_ReceivableAC(self):
        return self.ReceivableAC

class Payment:

    def __init__(Customer, PaymentAmount, Refund=0, Memo="Payment Received",
                 PaymentDate=datetime.date.today(),
                 PostedAccount=Account("Assets:Accounts Receivable"),
                 TransferAccount=Account("Assets:Current Assets:Petty Cash")):
        self.Customer = Customer
        self.PaymentAmount = PaymentAmount
        self.Refund = Refund
        self.Memo = Memo
        self.PaymentDate = PaymentDate
        self.PostedAccount = PostedAccount
        self.TransferAccount = TransferAccount

        self.Num = ""
        self.GList = None
        self.AutoPay = True
        self.Transaction = None

    def get_payment_amount(self):
        return gnucash_laska.gnc_numeric_from_decimal(self.PaymentAmount)

    def get_refund_amount(self):
        return gnucash_laska.gnc_numeric_from_decimal(self.Refund)
