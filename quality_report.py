import pandas as pd

def customer_on_time_percentages(excel_file):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file)
    
    # Organizes date columns are in datetime format to later compute
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], format= '%Y/%m/%d')
    df['Ship Target'] = pd.to_datetime(df['Ship Target'], format= '%Y/%m/%d')
    
    # Calculate the Days Late column
    df['Days Late'] = (df['Invoice Date'] - df['Ship Target']).dt.days
    
    # Extract month and year for grouping
    df['YearMonth'] = df['Invoice Date'].dt.to_period('M')
    
    # Calculate late counts and total counts per month
    n = 10.01 # varible chosen as cutoff for "on time"
    late = df[df['Days Late'] > n].groupby('YearMonth').size()
    total = df.groupby('YearMonth').size()
    
    # Calculate on-time percentage
    on_time = (1 - (late / total)) * 100
    
    # Convert the results to a DataFrame
    on_time_df = on_time.reset_index(name='On Time Percentage')
    
    return on_time_df

file = "104463-invoice_ontime_ship_report.xlsx"
result = customer_on_time_percentages(file)
print(result)

def vender_on_time_percentages(excel_file):
    # reads excel file
    df = pd.read_excel(excel_file)
    
    # organizes and groups data based on month and year
    df['Received On'] = pd.to_datetime(df['Received On'], format = '%Y/%m/%d')
    df['Year-Month'] = df['Received On'].dt.to_period('M')

    n = 10.01 # variable chosen as cutoff for late

    # calculates number of observations deemed late and total observations
    late = df[df['Days Late'] > n].groupby('Year-Month').size()
    total = df.groupby('Year-Month').size()

    # calculates and returns on-time percentages
    on_time = (1 - (late / total)) * 100
    on_time_df = on_time.reset_index(name = 'On Time Percentage')
    return on_time_df

file = "104489-purchase_order_receipt_vendor_performance.xlsx"
result = vender_on_time_percentages(file)
print(result)

def open_quote(excel_file):
    # reads excel file and organizes how data should be set-up
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
    df['Year-Month'] = df['Date'].dt.to_period('M')
    grouped = df.groupby(['Year-Month', 'Name'])
    
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
                'part': row['Prc Part'],
                'quote total': row['Quote Total']
            })
    
    # Convert the list of output rows to a DataFrame
    output_df = pd.DataFrame(output_rows)
    
    return output_df

# Vender On-Time Delivery data (OTD on lots)
def vendor_delivery_data(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)
    
    # Convert the Date column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
    
    # Create a Year-Quarter column from the Date column
    df['Year-Quarter'] = df['Date'].dt.to_period('Q')
    
    # Group by Year-Quarter and Vendor
    grouped = df.groupby(['Year-Quarter', 'Vendor'])
    
    # Initialize a list to store the output rows
    output_rows = []

    # Iterate over each group
    for (year_quarter, vendor), group in grouped:
        # Number of observations where days late > 10
        late_count = (group['Days Late'] > 10).sum()
        
        # Number of observations where days late <= 10
        on_time_count = (group['Days Late'] <= 10).sum()
        
        # Total number of observations
        total_count = group.shape[0]
        
        # Append the calculated data to the output list
        output_rows.append({
            'year_quarter': year_quarter,
            'vendor': vendor,
            '# late': late_count,
            '# on-time': on_time_count,
            '# total': total_count
        })
    
    # Convert the list of output rows to a DataFrame
    output_df = pd.DataFrame(output_rows)
    
    return output_df