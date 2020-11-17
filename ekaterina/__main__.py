import sys

import gnucash

from ekaterina import mazurka
from ekaterina import classes as Ekat
from ekaterina.readers import ods_reader
from ekaterina.parsers import csv_parser

if len(sys.argv) < 3:
    print("USAGE: ekaterina ODS_FILE GNUCASH_FILE")
    sys.exit(1)

odsfile = sys.argv[1]
gnucashfile = sys.argv[2]
print("*" * 80)
print(".ods file:", odsfile)
print(".gnucash file:", gnucashfile)
print("*" * 80)
input("Press Enter to continue, Ctrl+C to cancel. ")

read = ods_reader.Read(odsfile)
parsed = csv_parser.Parse(read)

total_parsed_payment_amount = sum(
    [  ekat_payment.get_payment_amount().to_double()
     - ekat_payment.get_refund_amount().to_double() for
       ekat_payment in filter(
           (lambda x: isinstance(x, Ekat.Payment)), parsed)])
print("*" * 80)
print("Total Payment Parsed = {}".format(total_parsed_payment_amount))
total_parsed_invoiced_units = sum(
    map((lambda x: sum(
        [i.get_quantity().to_double() for i in x.get_entries()])),
        filter((lambda x: isinstance(x, Ekat.Invoice)), parsed)))
print("Total Invoiced Units = {}".format(total_parsed_invoiced_units))
print("*" * 80)

input("Continue? (Ctrl+C to cancel): ")
print("*" * 80)
print("Total Payment Parsed = {}".format(total_parsed_payment_amount).upper())
print("Total Invoiced Units = {}".format(total_parsed_invoiced_units).upper())
print("*" * 80)
input("Absolutely sure? (CTRL+C TO CANCEL!): ")
input("POSITIVELY SURE? (CTRL+C TO CANCEL!!!): ")
print("\nWriting to the .gnucash file.\n")
gncsession = gnucash.Session(gnucashfile)
gncbook = gncsession.book
mazurka.danse_mazurka(gncbook, parsed)
gncsession.save()
gncsession.end()
print("Done.")
