"""
Parses a csv reader's output to ekaterina.classes.

We use python's csv module to read csv files.

Everything that follows expects a next(<csv.DictReader>)
--------------------------------
CSV Field Names:
### SALE:
CUSTOMER_NAME | CUSTOMER_ID -> Customer
SALE_DESCRIPTION            -> Description
QUANTITY                    -> Quantity
UNIT_PRICE                  -> Unit Price
NOTE                        -> (Sale) Note
INCOME_ACCOUNT              -> Income Account ("Income:Sales", etc.)
SALE_DATE (DATE)            -> Date of Sale
CURRENCY                    -> Currency of Sale
POST_DATE                   -> Post Date
DUE_DATE                    -> Due Date
RECEIVABLE_ACCOUNT          -> Receivable Accuont ("Assets:Accounts Receivable"

### Payment:
PAYMENT_AMOUNT              -> Payment Amount
REFUND                      -> Refund
MEMO                        -> Memo about payment
PAYMENT_DATE (DATE)         -> Payment Date
POSTED_ACCOUNT              -> Where invoice is posted (RECEIVABLE_ACCOUNT)
PAYMENT_TRANSFER_ACCOUNT    -> Payment Transfer "Assets:Current Assets:Petty Cash", etc.
"""
import datetime
from decimal import Decimal

from ekaterina import classes

class CustomerTransactionMap:
    """
    """
    pass

# What does each field name in the CSV file map to, in the program.
# So, field names 'CUSTOMER_NAME' or 'NAME' maps to the name of the
# customer. However, CUSTOMER_NAME has higher precedence. i.e. If
# we have both 'CUSTOMER_NAME' and 'NAME' in the CSV file, we go for
# 'CUSTOMER_NAME' unless it is None.

REQUIRED_DATE_FORMAT="%Y-%m-%d"

CSVFieldMappings = {
    "customer_name": ["CUSTOMER_NAME", "NAME"],
    "customer_id": ["CUSTOMER_ID"],
    "quantity": ["ITEMS_SOLD", "QUANTITY"],
    "unit_price": ["UNIT_PRICE"],
    "description": ["SALE_DESCRIPTION", "DESCRIPTION"],
    "note": ["SALE_NOTE", "NOTE"],
    "income_account": ["INCOME_ACCOUNT"],
    "sale_date": ["SALE_DATE", "DATE"],
    "currency": ["CURRENCY"],
    "post_date": ["POST_DATE"],
    "due_date": ["DUE_DATE"],
    "receivable_account": ["RECEIVABLE_ACCOUNT"],
    "payment_amount": ["PAYMENT_AMOUNT", "PAYMENT_RECEIVED"],
    "refund": ["REFUND"],
    "memo": ["PAYMENT_MEMO", "MEMO"],
    "payment_date": ["PAYMENT_DATE", "DATE"],
    "posted_account": ["POSTED_ACCOUNT", "RELATED_INVOICE_POSTAGE_AC"],
    "payment_transfer_account": ["PAYMENT_TRANSFER_ACCOUNT"]
}

_get = {
    ########################################################
    # KirkMcDonald from #python (freenode):
    # "Python's closures are late-binding, and the body
    # of a comprehension is evaluated in a single context
    # across all iterations"
    # - basically, closure sees the value from the last iteration
    #   of the comprehension
    # - "Late-binding" means the value is bound at the time the
    #   lambda is called, not at the time the lambda is defined.
    # Work around:
    # - either to use 2 lambdas
    # - or to take advantage of how default arguments work
    ##########################################################
    # Previous Version:
    # For a mapping dictionary such as:
    # {'CustomerName': 'CUSTOMER_NAME'}
    # however, we do not want to be all that rigid. For instance,
    # there could be a single 'DATE' for SALE_DATE and PAYMENT_DATE.
    # key: (lambda record, value=value: record.get(value))
    # for (key,value) in CSVFieldMappings.items()
    key: (lambda record, values=values:
          # In the following, we first record.get(value) for the value(s) in
          # CSVFieldMapping values. Then we filter out the None types, and then
          # return the list.
          list(
              filter(
                  (lambda match: match != None),
                  [record.get(value) for value in values])))
    for (key, values) in CSVFieldMappings.items()
}

def get(get_what, record):
    """
    """
    gotten =  _get[get_what](record)
    if len(gotten) > 0:
        return gotten[0]
    else:
        return None

def is_valid_Sale_record(record):
    is_valid_record = False
    if get('customer_name', record) and get('customer_id', record):
        is_valid_record = True
    if is_valid_record:
        is_valid_record = not None in [
            get('description', record),
            get('quantity', record),
            get('unit_price', record),
            get('income_account', record),
            get('date', record),
            get('currency', record)
        ]
    return is_valid_record

def is_valid_Payment_record(record):
    is_valid_record = False
    if get('customer_name', record) and get('customer_id', record):
        is_valid_record = True
    if is_valid_record:
        is_valid_record = not None in [
            get('payment_amount', record),
            get('payment_date', record),
        ]
    return is_valid_record

def is_valid_record(record):
    return is_valid_Sale_record(record) or is_valid_Payment_record(record)

def parse_Customer(record):
    CustomerName = get('customer_name', record)
    CustomerID   = get('customer_id', record)
    return Ekat.Customer(CustomerName, CustomerID)

def parse_Currency(record):
    Currency = get('currency', record)
    return Ekat.Currency(Currency)

def parse_Sale(record):
    assert is_valid_Sale_record(record), "Invalid Sale Record"
    customer = parse_Customer(record)
    description = get('description', record)
    quantity = float(get('quantity', record))
    unit_price = Decimal(get('unit_price', record))
    notes = get('note', record) or "" # If None, ""
    income_account = Ekat.Account(get('income_account', record))
    date = datetime.datetime.strptime(get('sale_date'), REQUIRED_DATE_FORMAT)
    currency = get('currency', record)
    return Ekat.Sale(customer, description, quantity,
                     unit_price, notes, income_account,
                     date, currency)

def parse_Payment(record):
    assert is_valid_Payment_record(record), "Invalid Payment Record"
    customer = parse_Customer(record)
    payment_amount = Decimal(get('payment_amount', record))
    refund = get('refund', record) or 0
    refund = Decimal(refund)
    memo = get('memo', record) or "Payment Received"
    payment_date = datetime.datetime.strptime(get('payment_date', record), REQUIRED_DATE_FORMAT)
    posted_account = get('posted_account', record) or "Assets:Accounts Receivable"
    posted_account = Ekat.Account(posted_account)
    payment_transfer_account = (
        get('payment_transfer_account', record)
        or "Assets:Current Assets:Petty Cash")
    payment_transfer_account = Ekat.Account(
        payment_transfer_account)
    return Ekat.Payment(customer, payment_amount,
                        refund, memo, payment_date,
                        posted_account, payment_transfer_account)

def parse_Invoice(record):
    assert is_valid_Sale_record(record), "Invalid Sale Record"
    customer = parse_Customer(record)
    sales = Ekat.SalesList(parse_Sale(record))
    postdate = get('post_date', record) or datetime.date.today()
    if not isinstance(postdate, datetime.date):
        postdate = datetime.datetime.strptime(postdate, REQUIRED_DATE_FORMAT)
    # We are not quite sure when the duedate is. Postdate is today, for sure.
    duedate = get('due_date', record) or None
    if isinstance(duedate, str):
        duedate = datetime.datetime.strptime(duedate, REQUIRED_DATE_FORMAT)
    receivable_account = (
        get('receivable_account', record)
        or "Assets:Accounts Receivable")
    receivable_account = Ekat.Account(receivable_account)
    description = get('description', record)
    return Ekat.Invoice(customer, sales, postdate, duedate,
                        receivable_account, description)

def parse_record(record):
    sale = None
    payment = None
    if is_valid_record(record):
        if is_valid_Sale_record(record):
            invoice = parse_Invoice(record)
        if is_valid_Payment_record(record):
            payment = parse_Payment(record)
    return (invoice, payment)

def Parse(reader_output_list, merge_invoices_to_the_same_customer=True):
    from itertools import chain

    # Step 1: Filter out all invalid records
    valid_records = filter(is_valid_record, reader_output_list)
    parsed_transactions = list(
        # Step 3: Flatten the tuples
        chain.from_iterable(
            # Step 2: Parse records into (Invoice, payment) tuples.
            # These can be (Invoice, None), (None, Payment) or
            # (Invoice, Payment).
            map(parse_record, valid_records)))

    if not merge_invoices_to_the_same_customer:
        return parsed_transactions

    # following merges invoices to the same customer.
    invoices = filter(lambda transaction: isinstance(transaction, Ekat.Invoice),
                      parsed_transactions)
    payments = filter(lambda transaction: isinstance(transaction, Ekat.Payment),
                      parsed_transactions)

    # Create a dictionary: {Customer: [Invoice1, Invoice2]}
    customer_invoice_dictionary = {}
    for invoice in invoices:
        customer_name = invoice.get_customer().get_name()
        if customer_name in customer_invoice_dictionary:
            customer_invoice_dictionary[customer_name].append(invoice)
        else:
            customer_invoice_dictionary[customer_name] = [invoice]
    # Now, extract all the Ekat.Sale objects in each Invoice and
    # merge them into the same Ekat.SalesList and create a single
    # Invoice off of them.
    for customer, invoice_list in customer_invoice_dictionary.items():
        sales = []
        for invoice in invoice_list:
            sales.extend(invoice.get_sales().sales)
            new_sales_list = Ekat.SalesList(*sales)
            invoice_list[0].sales = new_sales_list
            # Drop all but the first invoice from the list
        customer_invoice_dictionary[customer] = [invoice_list[0]]

    new_invoices = [ customer_invoice_dictionary[customer] for
                     customer in customer_invoice_dictionary ]
    # flatten the [ [list], [of], [invoices], [in], [nested], [lists] ]
    new_invoices = list(chain.from_iterable(new_invoices))

    new_parsed_transactions = []
    new_parsed_transactions.extend(new_invoices)
    new_parsed_transactions.extend(payments)
    return new_parsed_transactions
