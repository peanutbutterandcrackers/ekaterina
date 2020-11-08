import csv

from ekaterina.utils.fsutils import standardize_path

def Read(csvfile):
    """
    Read in a csv file and return a list of all things read.
    """
    csvfile = open(standardize_path(csvfile), newline='')
    csvdialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    CSVDictReader = csv.DictReader(csvfile, dialect=csvdialect)
    return list(CSVDictReader)
