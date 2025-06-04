# Clean Old Files Script

This script allows users to clean up old files from a specified directory by either deleting or archiving them. It is interactive, user-friendly, and includes logging for every operation performed.

---

## Features

- Prompts the user to:

  - Select a folder to clean
  - Choose an optional archive destination
  - Set the age threshold (in days) for what counts as "old"

- Scans all files in the selected directory and its subdirectories
- Offers a preview of what files will be deleted or archived
- Asks for confirmation before making any changes
- Logs all actions (deletions, archives, and errors) to `logs/clean_old_files.log`
- Displays color-coded console output for better visibility

---

## How to Use

1. Open a terminal and navigate to the `scripts/` directory in this project.
2. Run the script:

   ```bash
   python clean_old_files.py
   ```

3. Follow the prompts:

   - Enter the full path of the folder to clean.
   - (Optional) Enter the path of a folder where old files should be moved instead of deleted.
   - Set the number of days to determine file age.

4. Review the list of files that will be affected.
5. Confirm to proceed or cancel the operation.

---

## Example

```bash
=== Old File Cleaner ===
Enter the full path of the folder to clean: /Users/jeremy/Downloads
Enter the full path of the archive folder (optional, leave blank to skip archiving): /Users/jeremy/Downloads/old_files
Delete or archive files older than how many days? 30

Found 7 file(s) to archive:
  - /Users/jeremy/Downloads/test1.zip
  - /Users/jeremy/Downloads/old_log.txt
  ...

Proceed with cleanup? (y/n): y
[ARCHIVED] /Users/jeremy/Downloads/test1.zip
[ARCHIVED] /Users/jeremy/Downloads/old_log.txt
[COMPLETE] Cleanup finished at 2025-06-04 18:32:10
```

---

## Log Output Example

```
2025-06-04 18:32:10 - Archived: /Users/jeremy/Downloads/test1.zip -> /Users/jeremy/Downloads/old_files/test1.zip
2025-06-04 18:32:10 - Archived: /Users/jeremy/Downloads/old_log.txt -> /Users/jeremy/Downloads/old_files/old_log.txt
```

---

## Notes

- Archived files retain their original filenames.
- Logs are saved to the `logs/` folder in the project root.
- If the archive directory is left blank, files will be permanently deleted after confirmation.

---

## Requirements

- Python 3.x
- No external dependencies

---

## License

This script is open source and free to use or modify as part of the Automation Toolbox.
