import pandas as pd

# 1. Define phenotype variable
phenotype = "FT10"
p = phenotype.replace("_", "")
input_file = f"output_{p}_MaxMin3.xlsx"

# 2. Get the rankings of GWAS output files
files = {
    "plink": f"plink_{phenotype}_top_20_snps.txt",
    "tassel": f"tassel_{phenotype}_mlm_top_20_snps.txt",
    "gcta": f"gcta_{phenotype}_mlma_top_20_snps.txt",
    "gcta_loco": f"gcta_{phenotype}_mlma_loco_top_20_snps.txt",
    "gapit": f"gapit_{phenotype}_mlm_top_20_snps.csv"
}

# 3.Read the Autalasso SNP file
out_df = pd.read_excel(input_file)

print(out_df.head())

results = out_df[['snp_name']].copy()

def read_and_append(file_path, snp_col, rank_col):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, sep=',')
    else:
        df = pd.read_csv(file_path, delim_whitespace=True)

    line_numbers = []
    for snp_id in out_df['snp_name']:  # Ensure the correct column name is used
        matching_row = df[df[snp_col] == snp_id]
        if not matching_row.empty:
            line_number = matching_row.index[0] + 1  # pandas indexing starts from 0, so +1
            line_numbers.append(line_number)
        else:
            line_numbers.append(None)  # If no matching row, return None
    results[rank_col] = line_numbers


# Adjust paths and column names accordingly
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/plink_top20-snps/{files['plink']}", 'SNP',
                'PLINK Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/tassel_top20-snps/{files['tassel']}",
                'Marker', 'TASSEL Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gcta_top20-snps/{files['gcta']}", 'SNP',
                'GCTA Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gcta_top20-snps/{files['gcta_loco']}",
                'SNP', 'GCTA_LOCO Rank')
read_and_append(f"/Users/dong/GWAS/AtPolyDB/PLINK-TASSEL-GAPIT-GCTA-TOP-SNPs/gapit_top20-snps/{files['gapit']}", 'SNP',
                'GAPIT Rank')

# 6. Save GWAS ranking to xlsx file
output_path = f"output_{p}_snp_rankings.xlsx"
results.to_excel(output_path, index=False)

print("All rankings have been saved to the xlsx file.")