import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

data = pd.read_csv("/Users/dong/GWAS/AtPolyDB/p1.raw", sep=' ', header='infer', engine='python', iterator=True)

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

print('Get the  phenotypes Germ_22')
first_column = pd.read_csv('/Users/dong/GWAS/AtPolyDB/phenotypes.pheno', header='infer', usecols=['Germ_22'], sep=' ')
print(first_column)

print('insert the  phenotypes Germ_22 into genotype')
idx = 0
data.insert(loc=idx,column='Germ_22',value=first_column)
f=data.iloc[:5,:5]
print(f)
print('Delete the line containing Nan ')
data = data.dropna(subset=['Germ_22'])#Delete the line containing Nan
data = data.sort_values(by=['Germ_22'])# Sort by Germ_22
g=data.iloc[:5,:5]
print(g)

# Data analysis for the Germ_22 column
value_counts = data['Germ_22'].value_counts()
print(value_counts)

description = data['Germ_22'].describe()
print(description)

plt.figure(figsize=(10, 6))
sns.histplot(data['Germ_22'], bins=30, kde=True)
plt.xlabel('Germ_22         Values')
plt.ylabel('Frequency')
plt.title('Distribution of Germ_22 Values')
plt.show()

print('set 0 and 1')
data.loc[data.Germ_22<=3,'Germ_22'] = 0 #set 0 and 1
data.loc[data.Germ_22>3,'Germ_22'] = 1
h=data.iloc[:5,:5]
print(h)
print('Write raw file')
data.to_csv('/Users/dong/GWAS/AtPolyDB/re_p1_Germ_22.raw', sep=',', header=None, index=None)
print('Write raw file end')

