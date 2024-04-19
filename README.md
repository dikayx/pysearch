# PySearch

PySearch is a simple Python script that searches for a string in a file or a directory.

## Requirements

-   Python 3.9 or higher
-   Required Python packages listed in `requirements.txt`

## Get started

1. Clone the repository

    ```bash
    git clone https://github.com/dan-koller/pysearch
    ```

2. Create a new virtual environment & activate it

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > On Windows, open a command prompt and run `.venv\Scripts\activate.bat`

3. Install the required Python packages

    ```bash
    pip3 install -r requirements.txt
    ```

4. Run the script

    ```bash
    python3 src/main.py
    ```

_\*) You might need to use python and pip instead of python3 and pip3 depending on your system._

## Usage

-   Run the app (see [above](#get-started))
-   Choose whether you want to search in a directory or manually enter a path
-   Enter the search string of leave empty to search for all files
-   Wait for the search to finish
-   Results are copied with their full path to a `results-<timestamp>.txt` file
-   If you like, you can automatically copy the results to a different location

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
