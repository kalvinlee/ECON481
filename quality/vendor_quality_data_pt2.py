import pandas as pd

# For the second part follow the steps 11-14 Vendor Quality Data (based on qty), with the dates as the
# entire timespan wanted. MAKE SURE Prcpart IS A COLUMN THAT IS VISIBLE! Import the excel file and under the 
# line file = , replace the name of the new excel file with the old excel file, then run the chunk by 
# hitting the play on top, and it'll create a new excel file named vendor_quality_data_qty.xlsx which 
# holds the information for this part of the metric
def vendor_qual_data_pt2(excel_file):
    df2 = pd.read_excel(excel_file)
    df2['Entered On'] = pd.to_datetime(df2['Entered On'], format = '%Y/%m/%d')
    df2['Year-Quarter'] = df2['Entered On'].dt.to_period('Q')

    filtered_df = df2[df2['NCR Type'].str.contains('Manufacturing Defect', case=False, na=False)].copy()

    filtered_df['Prcpart_prefix'] = filtered_df['Prcpart'].str[:3]

    result = filtered_df.groupby(['Year-Quarter', 'Prcpart_prefix']).agg({
        'Quantity': 'sum'
    }).reset_index()

    return result

file2 = "107545-otd_ncrs.xlsx"
result = vendor_qual_data_pt2(file2)
output_path = 'vendor_quality_data2.xlsx'
result.to_excel(output_path, index = False)