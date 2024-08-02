import pandas as pd

# Customer rejection report needs two excel files to complete this. For file1, follow steps 1,4 and 5 and 
# make sure return qty column is shown, for the entire timespan. For file2, follow steps 6-8 for the 
# entire timespan. Import the excel files in, making sure file1 follows the first steps, and file2
# follows the 6-8 steps. Running the chunk will create a new excel file customer_rejection_report.xlsx
# which holds the information for this part of the metric
def customer_rejection_report(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df1['RMA Created'] = pd.to_datetime(df1['RMA Created'], format = '%Y/%m/%d')
    df1['Year-Month'] = df1['RMA Created'].dt.to_period('M')
    df2['Invoice Date'] = pd.to_datetime(df2['Invoice Date'], format = '%Y/%m/%d')
    df2['Year-Month'] = df2['Invoice Date'].dt.to_period('M')

    return_totals = df1.groupby('Year-Month')['Return Qty'].sum().reset_index()

    df1_unique = df1.drop_duplicates(subset='ID', keep='first')
    
    # Pivot table to get counts of each RMA Reason Code
    reason_code_counts = df1_unique.pivot_table(
        index='Year-Month', 
        columns='RMA Reason Code', 
        aggfunc='size', 
        fill_value=0
    ).reset_index()
    
    # Calculate the total RMA count for each Year-Month
    total_rma_count = df1_unique.groupby('Year-Month')['ID'].count().reset_index()
    
    # Calculate the total parts shipped
    total_parts = df2.groupby('Year-Month')['Qty'].sum().reset_index()
    
    # Merge dataframes to get the full report
    report_df = total_rma_count.merge(reason_code_counts, on='Year-Month')
    report_df = report_df.merge(return_totals, on='Year-Month')
    report_df = report_df.merge(total_parts, on='Year-Month')
    
    # Rename columns
    reason_code_columns = list(reason_code_counts.columns[1:])
    report_df.columns = ['Year-Month', 'Total RMA Count'] + reason_code_columns + ['Return Total', 'Total Parts']
    
    # Calculate the ratio
    report_df['Ratio'] = report_df['Return Total'] / report_df['Total Parts']
    
    return report_df

file1 = "104720-rma_details.xlsx"
file2 = "104722-invoices.xlsx"
result = customer_rejection_report(file1, file2)
output_path = 'customer_rejection_report.xlsx'
result.to_excel(output_path, index = False)