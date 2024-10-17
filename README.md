# Leveraging LASSO-Based Methodologies for Enhanced SNP Analysis in Plant Genomes
## Project Overview

This project consists of two main parts:  
1. **SNP Analysis using Biglasso**  
2. **SNP Analysis using Autalasso**  

## Project Directory Structure

The project directory contains the following structure:

```markdown
/LASSO-SNP
    ├── AtPolyDB
    │   ├── genotype.ped
    │   ├── phenotypes.pheno
    │   ├── p1.raw
    │   ├── re_p1_[phenotype].raw
    │   ├── out_[phenotype].txt
    │   ├── out_[phenotype]_snp_rankings.xlsx
    │   └── [phenotype].csv
    ├── Biglasso
    │   ├── get_input_with_[phenotype].py
    │   ├── biglasso.R
    │   └── get_snp_rank.py
    └── Autalasso
        ├── raw_to_csv.py
        ├── AUTALASSO_[phenotype].ipynb
        ├── extract_snps.py
        ├── compare_snp_rankings.py    
        ├── outbeta_[phenotype].txt
        ├── outlambda_[phenotype].txt
        ├── outMSE_[phenotype].txt
        ├── outACC_[phenotype].txt
        ├── output_[phenotype]_MaxMin3.xlsx
        └── output_[phenotype]_snp_rankings.xlsx
```
This structure encompasses all the source code and result files for the project. However, due to size limitations, certain data files and intermediate process files could not be uploaded. Users are encouraged to generate these files independently.

## Biglasso SNP Analysis

### Step 1: Convert Genotype Data Using PLINK
To generate a raw genotype file for Biglasso from the `.ped` format, please use the following command:
```bash
plink --file genotype --recodeA --out p1
```
​This command will create a file named `p1.raw`, which contains the genotype data necessary for further analysis using Lasso model.​ Ensure that you have PLINK installed and properly set up in your environment to execute this command successfully.

### Step 2: Integrate Phenotype Data
Integrate the phenotype data with the raw genotype file to create an input format compatible with Biglasso:
```bash
python get_input_with_[phenotype].py
```
This command generates the file `re_p1_[phenotype].raw`.

### Step 3: Identify Top 20 SNPs with Biglasso
To identify the top 20 SNPs, please execute the following command to run the Biglasso.R script:
```R
Rscript Biglasso.R
```
Upon running this script, an output file named `out_[phenotype].txt` will be generated.

Please note that to obtain approximately 20 SNPs, different phenotypes require varying regularization parameters (lambda). We should adjust the lambda values accordingly to achieve the desired number of SNPs for each specific phenotype analysis.

### Step 4: Compare SNP Rankings from Biglasso with GWAS Top 20 Results
To compare the SNPs obtained from Biglasso with those from GWAS (including PLINK, TASSEL, GAPIT, and GCTA), please execute the following command:
```bash
python get_snp_rank.py
```
This will generate a file named `out_[phenotype]_snp_rankings.xlsx`, which includes the SNPs identified by Biglasso along with their rankings in each of the GWAS results.

---

## Autalasso SNP Analysis

### Step 1: Convert Biglasso Raw Data to Autalasso Format
Run the `raw_to_csv.py` script to convert the `p1.raw` file generated in Biglasso Step 1 into a CSV format compatible with Autalasso:
```bash
python raw_to_csv.py
```
This will generate `[Phenotype].csv` as the input file for Autalasso.

### Step 2: Execute Autalasso Analysis in Jupyter Notebook
Open the Jupyter notebook `AUTALASSO_[phenotype].ipynb` and run the cells to perform the SNP analysis.

Since AUTALASSO is based on the Alternating Direction Method of Multipliers (ADMM) optimization algorithm and uses golden section search for automatic tuning of the learning rate and regularization parameters, we can adjust the ratio of training and testing data for different phenotypes to achieve the desired number of SNP results.

The results will be automatically saved in the `/Autalasso` directory and will include four output files:
- `outbeta_[phenotype].txt`: Contains the regression coefficients.
- `outlambda_[phenotype].txt`: Contains the lambda values.
- `outMSE_[phenotype].txt`: Contains the mean squared error (MSE).
- `outACC_[phenotype].txt`: Contains the accuracy (ACC) values.

### Step 3: Process Autalasso Results to Identify Top SNPs
Run the extract_snps.py script to process the result file `outbeta_[phenotype].txt` generated in Step 2. This script will produce an output file named `output_[phenotype]_MaxMin3.xlsx`, containing the top 18 SNPs selected by the top 3 highest and lowest values from the three regression coefficient columns.

```bash
python extract_snps.py
```

### Step 4: Compare Autalasso SNPs with GWAS
Use the `compare_snp_ranking.py` script to compare the Autalasso SNPs with GWAS results and generate a ranking based on GWAS:
```bash
python compare_snp_ranking.py
```

## Version Information
Below are the software versions used in this project:
- R version: 4.4.0 (2024-04-24)  
- Python: 3.7.6  
- Jupyter Core: 4.6.3  
- Jupyter Notebook: 6.0.3  
- Julia: 1.10.4  
- PLINK: v1.90b7.2 64-bit (11 Dec 2023)  


