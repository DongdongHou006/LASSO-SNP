import pandas as pd

# 1.Define phenotype variable
phenotype = "Emco5"
file_name = "out_"+phenotype

# 2.Read genotype.map
map_file_path = "/Users/dong/GWAS/AtPolyDB/genotype.map"
genotype_map = pd.read_csv(map_file_path, sep=" ", header=None)
genotype_map.columns = ['chr', 'snp_id', 'cM', 'position']

# 3.Get the SNP_ID from genotype.map
out_file = f"/Users/dong/GWAS/AtPolyDB/{file_name}.txt"
with open(out_file, 'r') as file:
    lines = file.readlines()

variable_indices = []
for line in lines:
    if line.startswith('V'):
        variable_indices.append(int(line.split('\t')[0][1:]))

snp_names = []
for index in variable_indices:
    map_row_index = index
    snp_name = genotype_map.loc[map_row_index - 1, 'snp_id']
    snp_names.append(snp_name)
    print(f"The SNP name for V{index} is: {snp_name}")

# 4.Save SNP_ID to the txt file
output_file_path = f"/Users/dong/GWAS/AtPolyDB/{file_name}_snp.txt"
with open(output_file_path, 'w') as out_file:
    for var_index, snp_name in zip(variable_indices, snp_names):
        out_file.write(f"V{var_index}\t{snp_name}\n")

print("All SNP names have been saved.")

# 5.Get the rankings of GWAS output files
files = {
    "plink": f"plink_{phenotype}_top_20_snps.txt",
    "tassel": f"tassel_{phenotype}_mlm_top_20_snps.txt",
    "gcta": f"gcta_{phenotype}_mlma_top_20_snps.txt",
    "gcta_loco": f"gcta_{phenotype}_mlma_loco_top_20_snps.txt",
    "gapit": f"gapit_{phenotype}_mlm_top_20_snps.csv"
}

out_df = pd.read_csv(output_file_path, delim_whitespace=True, header=None)
out_df.columns = ['Variable', 'SNP ID']

results = out_df.copy()

def read_and_append(file_path, snp_col, rank_col):
    df = pd.read_csv(file_path, sep=',') if file_path.endswith('.csv') else pd.read_csv(file_path, delim_whitespace=True)
    line_numbers = []
    for snp_id in out_df['SNP ID']:
        matching_row = df[df[snp_col] == snp_id]
        if not matching_row.empty:
            line_number = matching_row.index[0] + 1  # pandas索引从0开始，所以+1
            line_numbers.append(line_number)
        else:
            line_numbers.append(None)  # 如果没有匹配行，返回None
    results[rank_col] = line_numbers

read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/plink_top20-snps/{files['plink']}", 'SNP', 'PLINK Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/tassel_top20-snps/{files['tassel']}", 'Marker', 'TASSEL Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gcta_top20-snps/{files['gcta']}", 'SNP', 'GCTA Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gcta_top20-snps/{files['gcta_loco']}", 'SNP', 'GCTA_LOCO Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gapit_top20-snps/{files['gapit']}", 'SNP', 'GAPIT Rank')

# 6.Save GWAS ranking to xlsx file
output_all = f"/Users/dong/GWAS/AtPolyDB/{file_name}_snp_rankings.xlsx"
results.to_excel(output_all, index=False)

print("All rankings have been saved to the xlsx file.")
