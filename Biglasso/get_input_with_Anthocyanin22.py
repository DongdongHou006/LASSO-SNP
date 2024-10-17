import pandas as pd

data = pd.read_csv("/Users/dong/GWAS/AtPolyDB/p1.raw", sep=' ', header='infer', engine = 'python',iterator=True)

loop = True
chunkSize = 100
chunks = []
index=0
while loop:
    try:
        print(index)
        chunk = data.get_chunk(chunkSize)
        chunks.append(chunk)
        index+=1
    except StopIteration:
        loop = False
        print("Iteration is stopped.")
print('Merge Chunks')
data = pd.concat(chunks, ignore_index= True)
print('Merge Chunks End')
print('Delete the first six columns ')
data = data.drop(data.columns[[0, 1, 2, 3, 4, 5]], axis=1)
e=data.iloc[:3,:3]
print(e)

print('Get the  phenotypes Anthocyanin_22')
first_column = pd.read_csv('/Users/dong/GWAS/AtPolyDB/phenotypes.pheno', header='infer', usecols=['Anthocyanin_22'], sep=' ')

print(first_column)

print('insert the  phenotypes Anthocyanin_22 into genotype')
idx = 0
data.insert(loc=idx,column='Anthocyanin_22',value=first_column)
f=data.iloc[:5,:5]
print(f)
print('Delete the line containing Nan ')
data = data.dropna(subset=['Anthocyanin_22'])#Delete the line containing Nan
g=data.iloc[:5,:5]
print(g)
print('Write raw file')
data.to_csv('/Users/dong/GWAS/AtPolyDB/re_p1_Anthocyanin_22.raw', sep=',', header=None, index=None)
