%pip install openpyxl
import openpyxl
import pandas as pd

# Follow the first 7 steps Vendor On-Time Delivery Data, HAVING NO VENDOR SELECTED, with the dates as the entire
# timespan wanted. Import the excel file and under the line file = , replace the name of the new excel file
# with the old excel file, then run the chunk by hitting the play on top, and it'll create a new excel file
# named vendor_delivery_data_output.xlsx which holds the information for this part of the metric
def vendor_delivery_data(excel_file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)
    
    # Convert the Date column to datetime format
    df['Received On'] = pd.to_datetime(df['Received On'], format = '%Y/%m/%d')
    
    # Create a Year-Quarter column from the Date column
    df['Year-Quarter'] = df['Received On'].dt.to_period('Q')
    
    # Group by Year-Quarter and Vendor
    grouped = df.groupby(['Year-Quarter', 'Vendor'])
    
    # Initialize a list to store the output rows
    output = []
    n = 10
    
    # Iterate over each group
    for (year_quarter, vendor), group in grouped:
        # Number of observations where days late >= n
        late = (group['Days Late'] >= n).sum()
        
        # Total number of observations
        total = group.shape[0]

        # assumed on-time or total - late
        on_time = total - late
        
        # Append the calculated data to the output list
        output.append({
            'year_quarter': year_quarter,
            'vendor': vendor,
            '# late': late,
            '# on-time': on_time,
            '# total': total
        })
    
    # Convert the list of output rows to a DataFrame
    output_df = pd.DataFrame(output)
    
    return output_df

file = "104537-purchase_order_receipt_vendor_performance.xlsx"
result = vendor_delivery_data(file)
output_path = 'vendor_delivery_data_output.xlsx'
result.to_excel(output_path, index = False)