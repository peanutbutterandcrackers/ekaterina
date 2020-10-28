import pytest

from context import ods2csv

class TestGenerateCSVFromODSUsingLibreOffice:

    @pytest.fixture
    def nonexistent_ods_filepath(self, tmp_path):
        """Return a non-existent .ods file path"""
        nonexistent_ods = tmp_path/"nonexistent.ods"
        assert not nonexistent_ods.exists()
        return str(nonexistent_ods)

    @pytest.fixture
    def empty_ods_filepath(self, tmpdir):
        """Return an empty .ods file path"""
        empty_ods = tmpdir.join("empty.ods")
        empty_ods.write("")
        assert empty_ods.exists()
        return str(empty_ods)
    
    @pytest.mark.parametrize("invalid_input", [1234, True])
    def test_invalid_input(self, invalid_input):
        """Assert AssertionError is raised when passed non-string arguments"""
        with pytest.raises(AssertionError):
            ods2csv.generate_csv_from_ods_using_libreoffice(invalid_input)
            
    def test_libreoffice_not_found(self, monkeypatch, empty_ods_filepath):
        """Assert LibreOffice is found in $PATH"""
        monkeypatch.setenv("PATH", "")
        with pytest.raises(ods2csv.CSVConversionError, match="LibreOffice"):
            ods2csv.generate_csv_from_ods_using_libreoffice(empty_ods_filepath)

    def test_non_existant_file_input(self, nonexistent_ods_filepath):
        """Assert CSVConversionError is raised when passed non-existent file"""
        with pytest.raises(ods2csv.CSVConversionError,
                           match=r"(?i)specified .ods file .* not found"):
            ods2csv.generate_csv_from_ods_using_libreoffice(nonexistent_ods_filepath)

    def test_invalid_output_directory(self, empty_ods_filepath, tmp_path):
        """Assert error when the given outdir is not a directory"""
        invalid_out_dir = tmp_path/"invalid_out_dir"
        assert not invalid_out_dir.exists()
        with pytest.raises(AssertionError, match="Invalid Output Directory"):
            ods2csv.generate_csv_from_ods_using_libreoffice(empty_ods_filepath,
                                                            invalid_out_dir)
