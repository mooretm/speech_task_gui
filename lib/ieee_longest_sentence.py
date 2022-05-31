import pandas as pd
import numpy as np

df = pd.read_csv('.\\sentences\\IEEE-DF.csv')
df2 = df['ieee_text']

word_count = []

counter = 0
for sentence in df2:
    x = ''.join(df2[counter])
    words = x.split()
    word_count.append(len(words))
    counter += 1
print(word_count)
print('\nThe longest sentence is ' + str(max(word_count)) + ' words\n')

