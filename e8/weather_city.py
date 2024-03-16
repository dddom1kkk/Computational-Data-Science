import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import sys

label = pd.read_csv(sys.argv[1])
unlabel = pd.read_csv(sys.argv[2])

X_label = label.drop(['city', 'year'], axis=1)
y_label = label['city']

X_train, X_valid, y_train, y_valid = train_test_split(X_label, y_label);

scale = StandardScaler()
X_sctrain = scale.fit_transform(X_train)
X_scvalid = scale.transform(X_valid)
scunlabel = scale.transform(unlabel.drop(['city', 'year'], axis=1))

model = RandomForestClassifier(n_estimators=200, max_depth=10)
model.fit(X_sctrain, y_train)
print('Score: ', model.score(X_scvalid, y_valid))

predictions = model.predict(scunlabel)
pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)