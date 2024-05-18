1. Get the pdfs

2. Parse the pdfs to json

3. Convert the json to excel
   TODO:Parameterize file name input

4. Clean the excel files.

   - Validate missing data
   - Remove string values

   * Remove a row if the sum of vote counts doesnot matches the total number of vote counts.
     TODO:
     - Need to count numbr of such rows.
     - To accept state as a parameter in the function mapping.

5. Create name mapping for a state.

6. Create Intermediate files.
   TODO: Validations missing

7. Create string and swing booths.

8. Validate excel.
   TODO: Review validations.

TODO:

- One shell script for each state.
- State information is passed as parameter.

Create a github repo.
