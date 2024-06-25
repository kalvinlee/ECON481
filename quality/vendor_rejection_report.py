# pip install pandas

import pandas as pd

def vendor_rejection_report(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df1['Date'] = pd.to_datetime(df1['Date'], format = '%Y/%m/%d')
    df1['Year-Month'] = df1['Date'].dt.to_period('M')
    df2['Received On'] = pd.to_datetime(df2['Received On'], format = '%Y/%m/%d')
    df2['Year-Month'] = df2['Received On'].dt.to_period('M')

    reason_code_counts = df1.pivot_table(
        index='Year-Month', 
        columns='NCR Type', 
        aggfunc='size', 
        fill_value=0
    ).reset_index()

    total_ncr_count = df1.groupby('Year-Month')['ID'].count().reset_index()

    manufacturing_defects = df1[df1['NCR Type'] == 'Manufacturing Defect']
    
    # Then, group by 'Year-Month' and sum the 'Qty' column
    defect_totals = manufacturing_defects.groupby('Year-Month')['Qty'].sum().reset_index()

    total_parts = df2.groupby('Year-Month')['Qty'].sum().reset_index()

    report_df = total_ncr_count.merge(reason_code_counts, on='Year-Month')
    report_df = report_df.merge(defect_totals, on='Year-Month')
    report_df = report_df.merge(total_parts, on='Year-Month')
    
    # Rename columns
    reason_code_columns = list(reason_code_counts.columns[1:])
    report_df.columns = ['Year-Month', 'Total NCR Count'] + reason_code_columns + ['Defect Total', 'Total Parts']
    
    # Calculate the ratio
    report_df['Ratio'] = report_df['Return Total'] / report_df['Total Parts']
    
    return report_df
