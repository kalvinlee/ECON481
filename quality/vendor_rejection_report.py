%pip install openpyxl
import openpyxl
import pandas as pd

# Vendor Rejection Report needs two excel files to complete this. For file1 follow steps 1 and 2, and
# for file2 follow steps 5-7, downloading the excel files and importing them in for the entire timespan
# Make sure file1 and file2 are correctly loaded in. Running the chunk creates a new file
# vendor_rejection_report.xlsx which holds information asked for this metric
# NOTE: This function doesn't take into account NCR with both Enter on Date and Due Date
def vendor_rejection_report(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df1['Entered On'] = pd.to_datetime(df1['Entered On'], format = '%Y/%m/%d')
    df1['Year-Month'] = df1['Entered On'].dt.to_period('M')
    df2['Received On'] = pd.to_datetime(df2['Received On'], format = '%Y/%m/%d')
    df2['Year-Month'] = df2['Received On'].dt.to_period('M')

    reason_code_counts = df1.pivot_table(
        index='Year-Month', 
        columns='NCR Type', 
        aggfunc='size', 
        fill_value=0
    ).reset_index()

    total_ncr_count = df1.groupby('Year-Month')['NCR'].count().reset_index()

    manufacturing_defects = df1[df1['NCR Type'].str.contains('Manufacturing Defect', case=False, na=False)]
    
    # Then, group by 'Year-Month' and sum the 'Qty' column
    defect_totals = manufacturing_defects.groupby('Year-Month')['Quantity'].sum().reset_index()

    total_parts = df2.groupby('Year-Month')['Qty'].sum().reset_index()

    report_df = total_ncr_count.merge(reason_code_counts, on='Year-Month')
    report_df = report_df.merge(defect_totals, on='Year-Month')
    report_df = report_df.merge(total_parts, on='Year-Month')
    
    # Rename columns
    reason_code_columns = list(reason_code_counts.columns[1:])
    report_df.columns = ['Year-Month', 'Total NCR Count'] + reason_code_columns + ['Defect Total', 'Total Parts']
    
    # Calculate the ratio
    report_df['Ratio'] = report_df['Defect Total'] / report_df['Total Parts']
    
    return report_df

file1 = "107545-otd_ncrs.xlsx"
file2 = "107560-purchase_order_receipts.xlsx"
result = vendor_rejection_report(file1, file2)
output_path = 'vendor_rejection_report.xlsx'
result.to_excel(output_path, index = False)