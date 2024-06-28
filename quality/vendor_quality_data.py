import pandas as pd

def vendor_quality_data_qty(file1):
    df = pd.read_excel(file1)
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

def vendor_qual_data_pt2(file2):
    df2 = pd.read_excel(file2)
    df2['Date'] = pd.to_datetime(df2['Date'], format = '%Y/%m/%d')
    df2['Year-Quarter'] = df2['Date'].dt.to_period('Q')

    filtered_df2 = df2[df2['NCR Type'] == 'Manufacturing Defect']

    result2 = filtered_df.groupby(['Year-Quarter', 'Vendor']).agg({
        'Qty': 'sum'
    }).reset_index()

    return result2

file = "104553-incoming_inspections.xlsx"
result = vendor_quality_data_qty(file)
# print(result)
output_path = 'vendor_quality_data_qty.xlsx'
result.to_excel(output_path, index = False)
        