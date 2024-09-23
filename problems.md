## Issues Identified

### Filename Pattern Mismatch
- **Issue:** The pattern used to match names does not always match the names of the files created.
- **Impact:** This can cause problems in finding or processing the files correctly.

### Nested JSON Key Retrieval
- **Issue:** Sometimes, the `tables` key is nested within other keys in the JSON data, making it hard to find.
- **Proposed Solution:** Create a function to search through all levels of the JSON data to find the `tables` key no matter where it is located.

### Filename Pattern Conversion Error
- **Issue:** The system tries to convert filename patterns into numbers, but filenames can have letters as well, which causes errors.
- **Impact:** This prevents correct comparison and processing of filenames that include letters.
- **Proposed Solution:** Change the logic to handle filenames with letters without trying to convert them to numbers.

### File required in Cleanexcel and generate_intermediate script
- **Issue:** All files are specified manually. So whenever we run the script for different state we need to change the file manually in the code according to the state.
- **Impact:** This can cause get different output if we don't change the file according to the state
- **Proposed Solution:** According to the state_name passed we can use the file that it requires when we process the script by matching file name with state.

### Problem Generating Intermediate Table
- **Issue:** When generating intermediate table we are not filling field containing NAN value before adding INC status column.
- **Impact:** This is giving us warning when using idxmax(axis=1) method of pandas.
- **Proposed Solution:** We can soilve this problem either by adding default value instead of NAN value or we can ignore NAN value.

### Missing else condition in name_mapping script
- **Issue:** When defining unwanted_terms list there is condition where unwanted terms is different for state CH than other. But there else was not added which was making same unwanted terms for all states.
- **Impact:** This can cause error when processing data of state CH as unwanted_terms will be different.