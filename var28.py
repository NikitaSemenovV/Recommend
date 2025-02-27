import pandas as pd
import numpy as np
import json

def grade(user, client):
    res = []
    for i in range(1, len(user)):
        if user[i] > -1 and client[i] > -1:
            res.append(i)
    fst = np.array([user[i] for i in res])
    scd = np.array([client[i] for i in res])
    return sum(fst * scd) / (np.sqrt(sum(fst ** 2)) * np.sqrt(sum(scd ** 2)))


def kNN(i):
    df = knn.head(4)
    chisl = 0
    zn = 0
    for row in df.itertuples(index=False, name=None):
        if row[i] != -1:
            chisl += row[-2] * (row[i] - row[-1])
            zn += abs(row[-2])
    return data.iloc[27][-1] + chisl / zn


###
# Первая часть
###
data = pd.read_csv('data.csv')
data.head()
keys = data.keys()
print(data[data['Unnamed: 0'] == 'User 28'].head())
tmp_grade = []
for i in range(data.shape[0]):
    if i == 27:
        tmp_grade.append(0)
    else:
        tmp_grade.append(grade(data.iloc[i], data.iloc[27]))
data['grade'] = tmp_grade
m = []
for i in range(data.shape[0]):
    m.append(np.mean(list(filter(lambda x: x > -1, data.iloc[i][1:-1]))))
data['mean'] = m
data = data.round({'grade': 3, 'mean': 3})
knn = data.sort_values(by=['grade'], ascending=False)
knn.head(4)
res = {"user": 28, 1: {}}
for i in range(1, data.shape[1] - 2):
    if data.iloc[27][i] == -1:
        res[1][keys[i]] = kNN(i)

###
# Вторая часть
###
days = pd.read_csv("context_day.csv")
places = pd.read_csv("context_place.csv")
dfilms = []
for el in range(1, len(days.iloc[27])):
    if days.iloc[27][el].strip() == 'Sat' or days.iloc[27][el].strip() == 'Sun':
        dfilms.append(el)
pfilms = []
for el in range(1, len(days.iloc[27])):
    if places.iloc[27][el].strip() == 'h' and el in dfilms:
        pfilms.append(el)
rating = []
if len(pfilms) > 0:
    for el in pfilms:
        rating.append(data.iloc[27][el])
else:
    for el in dfilms:
        rating.append(data.iloc[27][el])
dot = np.mean(rating)
dots = []
for d in res[1].values():
    dots.append(abs(d - dot))
dot = dots.index(min(dots))
res[2] = {list(res[1].keys())[dot]: list(res[1].values())[dot]}

with open('res.json', 'w') as fl:
    fl.write(str(json.dumps(res)))
