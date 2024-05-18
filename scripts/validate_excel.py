import pandas as pd
import os
import re

def get_election_df(election_type, state = 'CH'):
    if state == 'CH' and election_type == 'AE': 
        election_df = pd.read_csv('data/CH_2023_namemapping.csv')
    # if state == 'MH' and election_type == 'GA':
    #     election_df = pd.read_csv('data/Maharashtra_GA.csv')
    return election_df



def get_parties(year,AC):
    # top_3 = [1,2,3]
    # # Define conditions
    # condition_general = (
    #     (election_df['Year'] == year) &
    #     (election_df['Constituency_No'] == AC) &
    #     (~election_df['Candidate'].isin(['None of the Above', 'NOTA']))
    # )

    # condition_inc = (
    #     (election_df['Party'] == 'INC')
    # )

    # # Use bitwise OR to combine conditions
    # filtered_election_df = election_df[
    #     (condition_general & election_df['Position'].isin(top_3)) |
    #     (condition_inc & condition_general)
    # ]

    # return filtered_election_df.sort_values(by='Position', ascending=True)['Party'].tolist()
    party = election_df[(election_df['Year'] == year) & (election_df['Constituency_No'] == AC)]['Party'].tolist()
    
    # return filtered_election_df.sort_values(by='Position', ascending=True)['Party'].tolist()
    return party

def evaluate_results(state,folder_path,output_dir,year:int,election_type, constituencies_count):
    # Create a DataFrame to store the summary for each file
    constituencies_df = election_df
    summary = []
    
    for i in range(1, constituencies_count+1):
        file_path = os.path.join(folder_path, f'{i}.xlsx')
        
        # check if the certain file exists in the folder 
        if os.path.exists(file_path):
            # Read the Excel file
            df = pd.read_excel(file_path)
            if df.empty:
                    summary.append({
                        'state':state,
                        'year': year,
                        'type': election_type,
                        'constituency': i,
                        'rows_less_than_50_excel' : True,
                        'files_found' : True
                    })
                    continue  

            # Compute required information
            max_SN = df.iloc[:, 0].max()  # Assuming SN is in the first column
            count_record = df.size 
            row = df.shape[0]
            column = len(df.columns)
            null_records = df.isnull().sum().sum()  # Total number of null data in the DataFrame
            total_votes_sum = df['Total'].sum()
            constituency_no =  df['Constituency'][0]
            matched_votes = constituencies_df[constituencies_df['Constituency_No'] == constituency_no]
            year_filtered = matched_votes[matched_votes['Year'] == year]
            # total_votes_sum_gt = year_filtered['Votes'].sum()
            # candidates_count_gt = year_filtered['Candidate'].nunique() - 1
            parties_ordered = get_parties(year, constituency_no)
            candidates_count_excel = [col for col in df.columns if col in parties_ordered or col.startswith('col') ]
            
            # Check the number of rows in excel 
            if row < 50:
                rows_less_than_50_excel = True 
            else : 
                rows_less_than_50_excel = False
                
            # Check if the columns listed in the parties_ordered are present in the excel file
            if set(parties_ordered).issubset(df.columns):
                party_mapped_correctly = True
            else : 
                party_mapped_correctly = False

            # Append the information to the summary DataFrame
            summary.append({
                'state':state,
                'year': year,
                'type': election_type,
                'constituency': i,
                'max_SN_excel': max_SN,
                'count_records_excel': count_record,
                'row_excel': row,
                'column_excel': column,
                'null_records_excel': null_records,
                'sum(Total)_excel':total_votes_sum,
                # 'consituency_wise_total_votes_rayan':total_votes_sum_gt,
                'count_of_candidates_excel':len(candidates_count_excel),
                # 'count_of_candidates(rayan_csv)':candidates_count_gt,
                'files_found' : True,
                'rows_less_than_50_excel': rows_less_than_50_excel,
                'party_mapped_correctly' : party_mapped_correctly       
            })
        else: 
            summary.append({
                        'state':state,
                        'year': year,
                        'type': election_type,
                        'constituency': i,
                        'files_found' : False,
                        'rows_less_than_50_excel' : True,
                    })
        
    # Save the summary DataFrame to a CSV file
    summary_df = pd.DataFrame(summary)
    output_file_path = os.path.join(output_dir, f'{state}_{election_type}_{year}.xlsx')
    summary_df.to_excel(output_file_path, index=False)    
