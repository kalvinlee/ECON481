%pip install openpyxl
import openpyxl
import pandas as pd

# Follow the first 3 steps of Open Quotes, with the dates as the entire timespan wanted
# Import the excel file and under the line file = , replace the name of the new excel file with the 
# old excel file, then run the chunk by hitting the play on top, and it'll create a new excel file
# named open_quotes_output.xlsx which holds the information for this part of the metric
def open_quotes(excel_file):
    # reads excel file and organizes how data should be set-up
    df = pd.read_excel(excel_file)
    df['Created On'] = pd.to_datetime(df['Created On'].str.replace('T', ''))
    df['Year-Month'] = df['Created On'].dt.to_period('M')
    grouped = df.groupby(['Year-Month', 'Inside Sales'])
    
    output_rows = []

    # finds top n Quote Totals and stores values for output
    n = 5
    for (month, name), group in grouped:
        # Select the top 5 entries by 'Quote Total' within the current group
        top = group.nlargest(n, 'Quote Total')
        
        # Iterate over the top entries and append them to the output list
        for _, row in top.iterrows():
            # Append the relevant data to the output list
            output_rows.append({
                'month': month,
                'name': name,
                'customer': row['Customer'],
                'part': row['Prcpart'],
                'quote total': row['Quote Total']
            })
    
    # Convert the list of output rows to a DataFrame
    output_df = pd.DataFrame(output_rows)
    
    return output_df

file = "104536-quotes.xlsx"
result = open_quotes(file)
output_path = 'open_quotes_output.xlsx'
result.to_excel(output_path, index=False)