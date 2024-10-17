import pandas as pd

# 1. Read Autalasso Result file: outbeta_[phenotype].txt
phenotype = "Germ22"
file_path = f"outbeta_{phenotype}.txt"
data = pd.read_csv(file_path, header=None)

# Combine three rows to one and get the row number.
data_reshaped = data.values.reshape(-1, 3)
row_numbers = pd.Series(range(1, data_reshaped.shape[0] + 1))

df = pd.DataFrame(data_reshaped, columns=['value1', 'value2', 'value3'])
df['SNPs address'] = row_numbers

# delete the row that 3 coefficients equals zero.
df_cleaned = df[~((df['value1'] == 0) & (df['value2'] == 0) & (df['value3'] == 0))].copy()


# 2. Get the snp_name via genotype.map
genotype_map_path = "/Users/dong/GWAS/AtPolyDB/genotype.map"
genotype_map = pd.read_csv(genotype_map_path, sep=" ", header=None, names=['chr', 'snp_name', 'cM', 'position'])

genotype_map.index = genotype_map.index + 1
df_cleaned['snp_name'] = df_cleaned['SNPs address'].map(genotype_map['snp_name'])
print(df_cleaned.head())

print(f"df_cleaned : {df_cleaned.shape}")
# Check if the number of rows in df_cleaned is greater than 18
if df_cleaned.shape[0] > 18:
    # Get the rows with max & min top 3 values in value123
    value1_max_3 = df_cleaned.nlargest(3, 'value1')
    value1_min_3 = df_cleaned.nsmallest(3, 'value1')
    value2_max_3 = df_cleaned.nlargest(3, 'value2')
    value2_min_3 = df_cleaned.nsmallest(3, 'value2')
    value3_max_3 = df_cleaned.nlargest(3, 'value3')
    value3_min_3 = df_cleaned.nsmallest(3, 'value3')

    # Combine 18 rows
    result_df = pd.concat(
        [value1_max_3, value1_min_3, value2_max_3, value2_min_3, value3_max_3, value3_min_3]).drop_duplicates()
else:
    result_df = df_cleaned
# Sorted by SNPs address
result_df_sorted = result_df.sort_values(by='SNPs address')
print(f"result_df_sorted : {df_cleaned.shape}")


# Save file : output_[phenotype]_snp_MaxMin3.xls
output_path = f"output_{phenotype}_MaxMin3.xlsx"
result_df_sorted.to_excel(output_path, index=False)

print(f"Top max and min top3 snp data saved to {output_path}")
