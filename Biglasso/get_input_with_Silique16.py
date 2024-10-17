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

print('Get the  phenotypes Silique_16')
first_column = pd.read_csv('/Users/dong/GWAS/AtPolyDB/phenotypes.pheno', header='infer', usecols=['Silique_16'], sep=' ')
print(first_column)

print('insert the  phenotypes Silique_16 into genotype')
idx = 0
data.insert(loc=idx,column='Silique_16',value=first_column)
f=data.iloc[:5,:5]
print(f)
print('Delete the line containing Nan ')
data = data.dropna(subset=['Silique_16'])#Delete the line containing Nan
data = data.sort_values(by=['Silique_16'])# Sort by Silique_16
g=data.iloc[:5,:5]
print(g)

# Data analysis for Silique_16
value_counts = data['Silique_16'].value_counts()
print(value_counts)

description = data['Silique_16'].describe()
print(description)

plt.figure(figsize=(10, 6))
sns.histplot(data['Silique_16'], bins=30, kde=True)
plt.xlabel('Silique_16 Values')
plt.ylabel('Frequency')
plt.title('Distribution of Silique_16 Values')
plt.show()


print('set 0 and 1')
data.loc[data.Silique_16<=1.5,'Silique_16'] = 0 #set 0 and 1
data.loc[data.Silique_16>1.5,'Silique_16'] = 1
h=data.iloc[:5,:5]
print(h)
print('Write raw file')
data.to_csv('/Users/dong/GWAS/AtPolyDB/re_p1_Silique_16.raw', sep=',', header=None, index=None)
print('Write raw file end')
