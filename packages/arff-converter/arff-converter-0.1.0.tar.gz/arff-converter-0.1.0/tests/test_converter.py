import pytest
import os
from arff.converter import parse_arff, write_xlsx
import pandas as pd


class TestParseArff:
    @pytest.fixture
    def sample_arff_file(self, tmp_path):
        def _sample_arff_file(content):
            file = tmp_path / "sample.arff"
            file.write_text(content)
            return str(file)
        return _sample_arff_file

    def test_parse_arff_valid_file(self, sample_arff_file):
        content = """
@relation weather
@attribute outlook {sunny, overcast, rainy}
@attribute temperature numeric
@data
sunny,85
overcast,83
rainy,70
"""
        arff_path = sample_arff_file(content)
        headers, data = parse_arff(arff_path)
        assert headers == ['outlook', 'temperature']
        assert data == [['sunny', '85'], ['overcast', '83'], ['rainy', '70']]

    def test_parse_arff_empty_file(self, sample_arff_file):
        content = ""
        arff_path = sample_arff_file(content)
        with pytest.raises(ValueError) as excinfo:
            headers, data = parse_arff(arff_path)
        assert "ARFF file is empty or invalid." in str(excinfo.value)

    def test_parse_arff_missing_data_section(self, sample_arff_file):
        content = """
@relation weather
@attribute outlook {sunny, overcast, rainy}
@attribute temperature numeric
"""
        arff_path = sample_arff_file(content)
        headers, data = parse_arff(arff_path)
        assert headers == ['outlook', 'temperature']
        assert data == []

    def test_parse_arff_invalid_format(self, sample_arff_file):
        content = """
Invalid content
Data without proper headers
"""
        arff_path = sample_arff_file(content)
        with pytest.raises(Exception):
            parse_arff(arff_path)


class TestWriteXlsx:
    @pytest.fixture
    def sample_data(self):
        return {
            "headers": ['outlook', 'temperature'],
            "data": [['sunny', '85'], ['overcast', '83'], ['rainy', '70']]
        }

    def test_write_xlsx_valid_data(self, tmp_path, sample_data):
        output_path = str(tmp_path / "output.xlsx")
        write_xlsx(sample_data['headers'], sample_data['data'], output_path)
        assert os.path.exists(output_path)

        df = pd.read_excel(output_path, dtype=str)  # Force all data to be read as strings
        assert list(df.columns) == sample_data['headers']
        assert df.values.tolist() == sample_data['data']

    def test_write_xlsx_empty_data(self, tmp_path, sample_data):
        output_path = str(tmp_path / "empty_output.xlsx")
        empty_data = []
        write_xlsx(sample_data['headers'], empty_data, output_path)
        assert os.path.exists(output_path)

        df = pd.read_excel(output_path)
        assert df.empty

    def test_write_xlsx_invalid_data_type(self, tmp_path, sample_data):
        output_path = str(tmp_path / "invalid_data_output.xlsx")
        invalid_data = "invalid data"
        
        with pytest.raises(Exception):
            write_xlsx(sample_data['headers'], invalid_data, output_path)

        assert not os.path.exists(output_path)