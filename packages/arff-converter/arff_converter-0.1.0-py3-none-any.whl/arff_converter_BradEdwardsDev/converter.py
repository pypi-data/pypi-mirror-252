import argparse
import pandas as pd
import re


def parse_arff(arff_path):
    with open(arff_path, 'r') as file:
        content = file.read()

    if not content.strip():
        raise ValueError("ARFF file is empty or invalid.")

    lines = content.split('\n')
    headers = []
    data_start = False
    data = []

    for line in lines:
        line = line.strip()
        if line.startswith('@attribute'):
            header = re.search('@attribute\s+(\w+)', line)
            if header:
                headers.append(header.group(1))
        elif line.startswith('@data') or line.startswith('@DATA'):
            data_start = True
        elif data_start and line:
            data.append(line.split(','))

    if not headers:
        raise ValueError("No valid headers found in ARFF file.")

    if not data and data_start:
        raise ValueError("Data section is present but no data found in ARFF file.")

    return headers, data


def write_xlsx(headers, data, output_path):
    """
    Writes the data to an XLSX file.
    Args:
    headers (list): List of column headers.
    data (list): List of data rows.
    output_path (str): Path to the output XLSX file.
    """
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(description='ARFF to XLSX Converter')
    parser.add_argument('arff_path',
                        type=str,
                        help='Path to the ARFF file')
    parser.add_argument('output_path',
                        type=str,
                        help='Path to the output XLSX file')
    args = parser.parse_args()

    try:
        headers, data = parse_arff(args.arff_path)
        write_xlsx(headers, data, args.output_path)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
