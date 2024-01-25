# ARFF Converter
Version: 0.1.0

## Overview

ARFF Converter is a Python package designed to convert Attribute-Relation File Format (ARFF) files into Excel (XLSX) files. It currently supports the conversion from ARFF to XLSX, with potential for future expansion to other file formats.

## Installation

To install ARFF Converter, use pip:

``` bash
pip install arff-converter
```

## Usage

The package provides a command-line interface for easy conversion of ARFF files to XLSX format.

### Command-Line Usage

To convert an ARFF file to an XLSX file, run the following command:

```bash
arff-converter <path_to_arff_file> <path_to_output_xlsx_file>
```

Replace <path_to_arff_file> with the path to your ARFF file and <path_to_output_xlsx_file> with the desired output path for the XLSX file.

### Example
```bash
arff-converter data.arff output.xlsx
```

This command will convert data.arff into an Excel file named output.xlsx.

## Features

- Converts ARFF files to XLSX format.
- Command-line interface for straightforward usage.
- Validates ARFF file structure and content.

## Requirements

- Python 3
- pandas
- openpyxl

## Development

This package is in early development and may include additional features and support for more formats in future releases.

## Contributing

Contributions to ARFF Converter are welcome. Please feel free to submit pull requests or report issues on the GitHub repository.

## License

ARFF is distributed under the MIT License. See LICENSE file for more details.
