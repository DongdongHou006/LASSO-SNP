import pandas as pd

# Define variables for customization
'''
Emco5:          column_index = 2 
Anthocyanin_22  column_index = 97 
FT10:           column_index = 30
Width_22:       column_index = 91
Silique_16:     column_index = 83
Silique_22:     column_index = 84
Germ_22:        column_index = 88
'''
phenotype = 'Silique_16'
column_index = 83
output_directory = '/Users/dong/GWAS/AtPolyDB/'
output_file_name = output_directory + phenotype + '.csv'

# Read the raw data file
data = pd.read_csv("/Users/dong/GWAS/AtPolyDB/p1.raw", sep=' ', header='infer', engine='python', iterator=True)

loop = True
chunkSize = 100
chunks = []
index = 0
while loop:
    try:
        print(index)
        chunk = data.get_chunk(chunkSize)
        chunks.append(chunk)
        index += 1
    except StopIteration:
        loop = False
        print("Iteration is stopped.")

print('Merge Chunks')
data = pd.concat(chunks, ignore_index=True)
print('Merge Chunks End')

print('Delete the first six columns ')
data = data.drop(data.columns[[0, 1, 2, 3, 4, 5]], axis=1)
e = data.iloc[:3, :3]
print(e)

print('Get the phenotypes')
first_column = pd.read_csv('/Users/dong/GWAS/AtPolyDB/phenotypes.pheno', header='infer', usecols=[column_index], sep=' ')

print(first_column)

print('Insert the phenotypes into genotype')
idx = 0
data.insert(loc=idx, column=phenotype, value=first_column)

f = data.iloc[:5, :5]
print(f)

print('Delete the line containing NaN ')
data = data.dropna(subset=[phenotype])

g = data.iloc[:5, :5]
print(g)

print('Write csv file')
data.to_csv(output_file_name, sep=',', header=None, index=None)
print('Write csv file End')

print(f'Number of rows: {data.shape[0]}')
print(f'Number of columns: {data.shape[1]}')