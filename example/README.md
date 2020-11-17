This is a minor example of how this module might be used.

Take a look at the .ods file. Notice the mappings (they are defined as per the
dictionary in ekaterina/parsers/csv_parser.py). Notice the 'Total' line. It is
not a valid record, as far as ekaterina is concerned (as there isn't a name of
a customer, or their id in that row). Notice how colors have been used to make
it easier for the user to understand things in the spreadsheet end.

The only constraints on the spreadsheet end are:
1. The mappings (the names of the columns as defined in the first row)
Note that the user can add their own columns, as long as they do not come into
conflict with the ekaterina mappings. For example, there is a 'Total' column
that is completely ignored by ekaterina. A general rule of thumb is that all
entirely uppercase column names are for ekaterina. Normal column names are for
the users (ignored by ekaterina).
2. The Users and Accounts being mentioned in the spreadsheet must already exist
in the target .gnucash file.

See this in action:
* Go to project root. Then run:
```
make env # you must have GNU guix installed for this.
python3 -m ekaterina example/ekaterina_test.ods example/ekaterina.gnucash
```
If you do not have GNU guix installed, it is up to you to install python-gnucash
bindings from your package manager, yourself.