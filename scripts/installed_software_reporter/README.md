# Installed Software Reporter

## Overview

The **Installed Software Reporter** is a Python utility that scans a Windows system to gather detailed information about installed software. It retrieves data from both the Windows Registry and common installation directories (e.g., `Program Files`). The results are printed to the console with color-coded output, logged to a `.txt` file, and exported to a structured `.csv` file.

---

## Features

- Collects software name, version, publisher, and install location
- Scans multiple registry locations (including 32-bit and 64-bit paths)
- Scans the file system for additional installed applications
- Exports data in both TXT and CSV formats
- Uses `colorama` for clean and readable console output
- Automatically timestamps log and CSV output

---

## Dependencies

Install required libraries using pip:

```bash
pip install colorama
```

> `colorama` is used for colored terminal output. All other modules are part of the Python standard library.

---

## Usage

1. Clone the repo or download the script folder.
2. Run the script in a terminal or command prompt:

```bash
python installed_software_reporter.py
```

3. After execution, the following files will be created inside the `/logs` folder:

- `installed_software_<timestamp>.txt` — plain-text formatted report
- `installed_software_<timestamp>.csv` — structured spreadsheet-friendly version

---

## Sample Output (Console)

```bash
=== Installed Applications Report ===
Generated: 2025-06-04 17:12:44

Program Name                           Version              Publisher                      Install Location
===============================================================================================
7-Zip                                 22.01                Igor Pavlov                    C:\Program Files\7-Zip
...

Report saved to TXT: logs/installed_software_2025-06-04_17-12-44.txt
CSV report saved to: logs/installed_software_2025-06-04_17-12-44.csv
```

---

## Notes

- This tool is designed for **Windows environments**.
- Programs detected in file system scans will have `Version` and `Publisher` marked as `Unknown`.
- Registry data is prioritized when deduplicating entries.
- All output is logged and preserved for later review.

---

## Author

Jeremy Tarkington
GitHub: [jtarkington-dev](https://github.com/jtarkington-dev)

---

## License

This script is open source and free to use or modify as part of the Automation Toolbox project.
