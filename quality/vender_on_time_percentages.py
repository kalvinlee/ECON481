%pip install openpyxl
import openpyxl
import pandas as pd

# Follow the first 3 steps of Vendor On-Time Report, with the dates as the entire timespan wanted
# Import the excel file and under the line file = , replace the name of the new excel file with the 
# old excel file, then run the chunk by hitting the play on top, and it'll create a new excel file
# named vendor_on_time_percentages_output.xlsx which holds the information for this part of the metric
def vendor_on_time_percentages(excel_file):
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
result = vendor_on_time_percentages(file)
output_path = 'vendor_on_time_percentages_output.xlsx'
result.to_excel(output_path, index=False)