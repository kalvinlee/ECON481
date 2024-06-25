import pandas as pd
#pip install pandas

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
output_path = 'customer_on_time_percentages_output.xlsx'
result.to_excel(output_path, index=False)