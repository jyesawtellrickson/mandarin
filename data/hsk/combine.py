import pandas as pd

tmp = pd.DataFrame()

for i in range(1, 7):
    tmp2 = pd.read_csv('L'+str(i)+'.txt', sep='\t', header=None)
    tmp2['hsk_level'] = i
    print(tmp2.shape)
    tmp = tmp.append(tmp2)

tmp.columns = ['simplified', 'traditional', 'pinyin_1', 'pinyin_2', 'english',
               'hsk_level']
tmp.to_csv('all.csv', index=False)
