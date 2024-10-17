import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
data = pd.read_csv("/Users/dong/GWAS/AtPolyDB/p1.raw", sep=' ', header='infer', engine='python', iterator=True)

# Read file in chunks
loop = True
chunkSize = 100
chunks = []
index = 0
while loop:
    try:
        print(f"Reading chunk {index}")
        chunk = data.get_chunk(chunkSize)
        chunks.append(chunk)
        index += 1
    except StopIteration:
        loop = False
        print("Iteration is stopped.")

print('Merging chunks')
data = pd.concat(chunks, ignore_index=True)
print('Chunks merged')

# Check data reading status
print(f"Data shape after merge: {data.shape}")
print(data.head())

# Delete the first six columns
print('Deleting the first six columns')
data = data.drop(data.columns[[0, 1, 2, 3, 4, 5]], axis=1)
print(f"Data shape after deleting columns: {data.shape}")
print(data.head())

# Display the first 3 rows and 3 columns
e = data.iloc[:3, :3]
print(e)

# Read phenotype data
print('Getting the phenotypes Emco5')
first_column = pd.read_csv('/Users/dong/GWAS/AtPolyDB/phenotypes.pheno', header='infer', usecols=['Emco5'], sep=' ')
print(first_column.head())
print(f"Data shape of Emco5: {first_column.shape}")

# Insert phenotype data into genotype data
print('Inserting the phenotypes Emco5 into genotype')
idx = 0
data.insert(loc=idx, column='Emco5', value=first_column)
print(f"Data shape after inserting Emco5: {data.shape}")
print(data.head())
f=data.iloc[:5,:5]
print(f)

# Delete rows containing NaN values
print('Deleting rows containing NaN')
data = data.dropna(subset=['Emco5'])
print(f"Data shape after dropping NaN: {data.shape}")
print(data.head())

# Write the results back to the file
print('Writing raw file')
data.to_csv('/Users/dong/GWAS/AtPolyDB/re_p1_Emco5.raw', sep=',', header=None, index=None)
print('File written')