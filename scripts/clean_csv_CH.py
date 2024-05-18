import pandas as pd

# Load the CSV file
df = pd.read_csv('data/new_updated_candidate_names.csv')

# Define a function to transform each row into the desired format
def transform_row(row):
    inc_candidate = {
        'constituency_no': row['constituency_no'],
        'candidate_name': row['INC_candidate_name'],
        'party': 'INC',
        'hindi_name': row['INC_hindi_name'],
        'year': 2023  # Example year (adjust as needed)
    }
    bjp_candidate = {
        'constituency_no': row['constituency_no'],
        'candidate_name': row['BJP_candidate_name'],
        'party': 'BJP',
        'hindi_name': row['BJP_Hindi_name'],
        'year': 2023  # Example year (adjust as needed)
    }
    return [inc_candidate, bjp_candidate]

# Apply the transformation to each row
transformed_data = []
for _, row in df.iterrows():
    transformed_data.extend(transform_row(row))

# Create a new DataFrame from the transformed data
new_df = pd.DataFrame(transformed_data)

# Write the new DataFrame to a new CSV file
new_df.to_csv('transformed_data.csv', index=False)
