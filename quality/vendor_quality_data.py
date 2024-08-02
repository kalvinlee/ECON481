import pandas as pd

# Follow the first 5 steps Vendor Quality Data (based on qty), HAVING NO VENDOR SELECTED, with the dates as
# the entire timespan wanted. Import the excel file and under the line file = , replace the name of the new 
# excel file with the old excel file, then run the chunk by hitting the play on top, and it'll create a new
# excel file named vendor_quality_data_qty.xlsx which holds the information for this part of the metric
def vendor_quality_data_qty(excel_file):
    df = pd.read_excel(excel_file)
    df['Inspected On'] = pd.to_datetime(df['Inspected On'], format = '%Y/%m/%d')
    df['Year-Quarter'] = df['Inspected On'].dt.to_period('Q')

    # Group by Year-Quarter and Vendor, and sum the relevant columns
    result = df.groupby(['Year-Quarter', 'Vendor']).agg({
        'Qty Inspected': 'sum',
        'Qty Passed': 'sum',
        'Qty Failed': 'sum'
    }).reset_index()
    
    # Rename columns to match the desired output
    result.rename(columns={
        'Qty Inspected': 'Total Qty Inspected',
        'Qty Passed': 'Total Qty Passed',
        'Qty Failed': 'Total Qty Failed'
    }, inplace=True)

    return result

file = "104553-incoming_inspections.xlsx"
result = vendor_quality_data_qty(file)
output_path = 'vendor_quality_data_qty.xlsx'
result.to_excel(output_path, index = False)