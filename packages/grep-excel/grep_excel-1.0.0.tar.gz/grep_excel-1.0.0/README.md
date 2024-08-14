# Grep Excel

[![PyPI](https://img.shields.io/pypi/v/grep-excel)](https://pypi.org/project/grep-excel/)

ExcelGrep is an utility for searching through Excel files in a directory (including nested directories) to find cells that match a specified pattern.

## Features

- **Search Pattern:** Find cells containing a specified string pattern.
- **Exclude Pattern:** Optionally exclude matches that contain a specified string pattern.
- **Print Row Data:** Optionally print the entire row data of matching cells.
- **Progress Tracking:** Displays progress information for scanning files and cells.
- **Performance Metrics:** Shows elapsed time for scanning and overall progress.


## Installation

You can install the package using pip:

```sh
pip install grep_excel
```

## Usage

To use the grep_excel, run the following command:

```sh
grep-excel ./your_directory "pattern_to_search" --exclude "pattern_to_exclude" --print-row

```

## Arguments


## Contributing
Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes.
- Write tests for your changes.
- Ensure all tests pass.
- Submit a pull request.

### Development
To set up a development environment:

#### Clone the repository:

```sh
git clone https://github.com/stenzr/grep_excel
cd grep_excel
```

#### Create a virtual environment and activate it:

```sh
Copy code
python3 -m venv venv
source venv/bin/activate
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


