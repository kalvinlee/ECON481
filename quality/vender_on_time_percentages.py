#pip install pandas
import pandas as pd
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
output_path = 'vender_on_time_percentages_output.xlsx'
result.to_excel(output_path, index=False)