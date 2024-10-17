#install.packages("Matrix")
library(ncvreg)
library(Matrix)
library(biglasso)
library(bigmemory)
library(readr)

# Set working directory
setwd("/Users/dong/GWAS/AtPolyDB")

# Define the phenotype variable
phenotype <- "Emco5"

# Remove existing files
file.remove(paste0("re_p1_", phenotype, ".bin"))
file.remove(paste0("re_p1_", phenotype, ".desc"))

# Set up and load the big data matrix
X <- setupX(filename = paste0("re_p1_", phenotype, ".raw"), sep=',')
X <- attach.big.matrix(paste0("re_p1_", phenotype, ".desc"))

# Extract independent and dependent variables
y <- X[,1]
X <- X[,-1]
X.bm <- as.big.matrix(X)

# Check Datastructure
str(X.bm)
print(dim(X.bm))
print(X.bm[1:10, 1:10])
print(table(y))

# Run BigLasso
fit <- biglasso(X.bm, y, ncores = 4)
fit <- biglasso(X.bm, y, family = "binomial", ncores = 4)

# Emco5:      lambda = 0.06   Anthocyanin_22: lambda = 0.125
# FT10:       lambda = 0.14   Width_22:       lambda = 0.135
# Silique_16: lambda = 0.14   Silique_22:     lambda = 0.14
# Germ_22:    lambda = 0.01
coefs <- as.matrix(coef(fit, lambda = 0.06))
non_zero_coefs <- coefs[coefs != 0, ]

# Sorted none-zero coefficients
sorted_coefs <- non_zero_coefs[order(abs(non_zero_coefs), decreasing = TRUE)]
print(sorted_coefs)
print(predict(fit, lambda = 0.06, type = "nvars"))

# Write sorted none-zero coefficients
write.table(sorted_coefs, file = paste0("out_", phenotype, ".txt"), sep = "\t", col.names = NA, quote = FALSE)
