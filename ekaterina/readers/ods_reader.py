#!/usr/bin/env python3

# Wait... ODSReader is just CSVReader Wrapper?
# ............................always has been.

from subprocess import run
from tempfile import TemporaryDirectory

from ekaterina.utils.fsutils import *
from ekaterina.readers import csv_reader

class CSVConversionError(Exception):
    pass

def generate_csv_from_ods_using_libreoffice(odsfile, outdir=os.getcwd()):
    """
    Given an Open Document Spreadsheet (.ods) file, generates
    a Comma Separated Value (.csv) file by calling LibreOffice.
    $ libreoffice --convert-to csv --outdir outdir odsfile

    Returns the absolute path of the generated csv file.
    """
    assert isinstance(odsfile, str), "can not accept non-string arguments"

    outdir = standardize_path(outdir)
    odsfile = standardize_path(odsfile)
    assert isdirectory(outdir), ("Invalid Output Directory: '{}'"
                                 .format(outdir))
    if not isfile(odsfile):
        raise CSVConversionError(("Specified .ods file '{}' not found"
                                  .format(odsfile)))

    try:
        run(["libreoffice", "--version"], capture_output=True)
    except FileNotFoundError:
        raise CSVConversionError("LibreOffice not found.")

    conversion = run(["libreoffice",
                      "--convert-to", "csv",
                      "--infilter=CSV:44,34,76,1", # Use UTF-8 encoding
                      "--outdir", outdir,
                      odsfile],
                     capture_output=True)

    # Add check here to assert that no error occured.
    # Turns out, LibreOffice isn't guarenteed to return a non-zero
    # exit status on error (at least not when the file does not exist)
    # Hence the len(conversion.stderr) check.
    if conversion.returncode != 0 or len(conversion.stderr) != 0:
        err_msg = conversion.stderr.decode("utf-8").strip()
        raise CSVConversionError(err_msg)

    return destination_path(outdir, odsfile, new_extension=".csv")

def Read(odsfile):
    tempdir = TemporaryDirectory()
    csvfile = generate_csv_from_ods_using_libreoffice(
        standardize_path(odsfile),
        outdir=tempdir.name)
    return csv_reader.Read(csvfile)
