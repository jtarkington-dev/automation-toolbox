# System Info Reporter

## Overview

The **System Info Reporter** is a lightweight Python script that collects and displays detailed environment information for Windows-based systems. It captures vital system data such as OS version, hardware specs, memory usage, disk usage, environment variables, and more. This is especially useful for debugging, reporting issues to support teams, or verifying setup consistency across machines.

---

## Features

- Displays hostname, OS version, architecture, and CPU info
- Reports Python version
- Captures detailed memory usage statistics (requires `psutil`)
- Lists available disk space for all drives
- Optionally reports GPU information (requires `GPUtil`)
- Dumps all environment variables
- Saves report to timestamped `.txt` file in the current directory

---

## Dependencies

Install the following packages before running:

```bash
pip install psutil GPUtil
```

**Important Notes:**

- If using **Python 3.12 or later**, you must also install `setuptools` to avoid import errors with `GPUtil`, as it relies on the deprecated `distutils` module:

```bash
pip install setuptools
```

- If GPU info is not required, `GPUtil` is optional.

---

## Usage

1. Clone or download the repo.
2. Run the script:

```bash
python system_info_reporter.py
```

3. A report file named like `system_info_2025-06-04_16-08-06.txt` will be generated in the same directory.

---

## Sample Output

A generated report will contain sections like:

- `=== System Information Report ===`
- `=== Memory Information ===`
- `=== Disk Usage ===`
- `=== Environment Variables ===`

Example snippet:

```
=== Memory Information ===
Total: 15.72 GB
Available: 1.24 GB
Used: 14.48 GB (92.1%)
```

---

## Notes

- This script is intended for **Windows systems**.
- If `GPUtil` is not installed, the script will skip GPU details and show a warning.
- `GPUtil` only supports NVIDIA GPUs. AMD and Intel integrated graphics are not reported.
- If you're running Python 3.12+, and see an error about `distutils`, be sure `setuptools` is installed.
- You can modify the script to include more info such as network adapters or installed software if needed.

---

## Author

Jeremy Tarkington
GitHub: [jtarkington-dev](https://github.com/jtarkington-dev)

---

## License

This script is open source and free to use or modify as part of the Automation Toolbox.
