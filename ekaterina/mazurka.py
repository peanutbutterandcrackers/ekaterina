"""
Mazurka (n): A Polish folk dance; featured in 'Anna Karenina' by Leo Tolstoy.
Kitty's heart breaks over Count Vronsky, who dances the Mazurka with Anna.

We take the date structures (objects) from ekaterina.classes, and turn them
into actual GNUCash objects in order to write to the .gnucash file. This
process will be called, the Mazurka, as if it were a dance.

Naming Scheme:
For ekat.X -> gnucash.X: ekat_to_gnc_X()
For ekat.X -> gnucash.Y: ekatX_to_gncY()
"""
import gnucash

from ekaterina import classes

def ekat_to_gnc_Account(GNCBook, EkatAccount):
    """
    Turn ekaterina.Account into gnucash.Account.

    More specifically, turn ekaterina.classes.Account into
    gnucash.gnucash_core.Account.
    """
    RootAccount = GNCBook.get_root_account()
    return RootAccount.lookup_by_full_name(
        EkatAccount.get_account_identifier().replace(":", "."))

def ekat_to_gnc_Currency(GNCBook, EkatCurrency):
    """
    Turn ekaterina.Currency into gnucash.Currency

    More specifically, turn ekaterina.classes.Currency into
    gnucash.gnucash_core.GncCommodity of the namespace "Currency".
    """
    CommodityTable = GNCBook.get_table()
    return CommodityTable.lookup("CURRENCY", str(EkatCurrency))

def ekat_to_gnc_Customer(GNCBook, EkatCustomer):
    """
    Turn ekaterina.Customer into gnucash.Customer

    More specifically, turn ekaterina.classes.Customer into
    gnucash.gnucash_business.Customer.
    """
    return GNCBook.CustomerLookupByID(EkatCustomer.getID())

def ekat_to_gnc_Invoice(GNCBook, EkatInvoice):
    """
    Turn ekaterina.Invoice into gnucash.Invoice.

    More specifically, turn ekaterina.classes.Invoice into
    gnucash.gnucash_business.Invoice.
    """
    # Consult: gnucash_api_docs/html/group__Invoice.html
    # `make gnucash_api_docs` in the project root first.
    Customer   = ekat_to_gnc_Customer(GNCBook, EkatInvoice.get_customer())
    Currency   = ekat_to_gnc_Currency(GNCBook, EkatInvoice.get_currency())
    GNCInvoice = gnucash.gnucash_business.Invoice(
        GNCBook,
        GNCBook.InvoiceNextID(Customer),
        Currency,
        Customer)

    for sale_entry in EkatInvoice.get_entries():
        ekatSale_to_gncInvoiceEntry(GNCBook, GNCInvoice, sale_entry)

    return GNCInvoice

def ekatSale_to_gncInvoiceEntry(GNCBook, GNCInvoice, EkatSale):
    """
    Turn ekaterina.Sale into gnucash.InvoiceEntry.

    More specifically, turn ekaterina.classes.Sale into
    gnucash.gnucash_business.Entry.
    """
    Date = EkatSale.get_date()
    Notes = EkatSale.get_notes()
    Description = EkatSale.get_description()
    Quantity = EkatSale.get_quantity()
    UnitPrice = EkatSale.get_unitprice()
    IncomeAccount = ekat_to_gnc_Account(GNCBook, EkatSale.get_incomeaccount())
    InvoiceEntry = gnucash.gnucash_business.Entry(GNCBook, GNCInvoice, Date)
    InvoiceEntry.SetDescription(Description)
    InvoiceEntry.SetNotes(Notes)
    InvoiceEntry.SetQuantity(Quantity)
    InvoiceEntry.SetInvPrice(UnitPrice)
    InvoiceEntry.SetInvAccount(IncomeAccount)
    return InvoiceEntry

def add_ekatInvoice_to_GNCBook(GNCBook, EkatInvoice):
    """
    Add ekaterina.Invoice to GNCBook.
    """
    # Consult: gnucash_api_docs/html/group__Invoice.html
    # gncInvoicePostToAccount()
    # `make gnucash_api_docs` in the project root first.
    # These seem like sane defaults:
    AccumulateSplits = True
    Autopay = True
    DueDate  = EkatInvoice.get_duedate()
    PostDate = EkatInvoice.get_postdate()
    Description = EkatInvoice.get_description()
    if not Description:
        Description = "; ".join(
            [sale.get_description() for sale in EkatInvoice.get_sales()])
        ReceivableAC = ekat_to_gnc_Account(GNCBook, EkatInvoice.get_ReceivableAC())
        Invoice = ekat_to_gnc_Invoice(GNCBook, EkatInvoice)
        Invoice.PostToAccount(ReceivableAC, PostDate, DueDate, Description,
                              AccumulateSplits, Autopay)

def add_ekatPayment_to_GNCBook(GNCBook, EkatPayment):
    """
    Add ekaterina.Payment to GNCBook.
    """
    Customer = ekat_to_gnc_Customer(GNCBook, EkatPayment.Customer)
    PaymentAmount = EkatPayment.get_payment_amount()
    RefundAmount = EkatPayment.get_refund_amount()
    PostedAccount = ekat_to_gnc_Account(GNCBook, EkatPayment.PostedAccount)
    TransferAccount = ekat_to_gnc_Account(GNCBook, EkatPayment.TransferAccount)

    # Consult gnucash api docs:
    # gnucash_api_docs/html/group__Owner.html#ga66a4b67de8ecc7798bd62e34370698fc
    # Run `make gnucash_api_docs` in project root.
    Customer.ApplyPayment(EkatPayment.Transaction,
                          EkatPayment.GList,
                          PostedAccount,
                          TransferAccount,
                          EkatPayment.get_payment_amount(),
                          EkatPayment.get_refund_amount(),
                          EkatPayment.PaymentDate,
                          EkatPayment.Memo,
                          EkatPayment.Num,
                          EkatPayment.AutoPay)

def danse_mazurka(GNCBook, TransactionList):
    """
    (Dance Mazurka): The final call

    Add all the Payments and Invoices in the TransactionList to GNCBook.
    """
    for Transaction in TransactionList:
        assert (isinstance(Transaction, classes.Invoice)
                or isinstance(Transaction, classes.Payment))

    for Transaction in TransactionList:
        if isinstance(Transaction, classes.Invoice):
            add_ekatInvoice_to_GNCBook(GNCBook,
                                       Transaction)
        elif isinstance(Transaction, classes.Payment):
            add_ekatPayment_to_GNCBook(GNCBook,
                                       Transaction)
        else:
            pass # Won't execute
