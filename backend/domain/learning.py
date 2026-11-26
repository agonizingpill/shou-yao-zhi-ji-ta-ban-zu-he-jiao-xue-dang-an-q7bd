import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def vectors(rows):
    return [[r['right_rate'],r['left_rate'],r['pause']] for r in rows]

def calculate(data):
    candidates=data['archive']
    x_train,x_hold=train_test_split(candidates,test_size=1/3,random_state=24,
                                  stratify=[r['pattern'] for r in candidates])
    scaler=StandardScaler().fit(vectors(x_train))
    model=LinearDiscriminantAnalysis(n_components=2)
    model.fit(scaler.transform(vectors(x_train)),[r['pattern'] for r in x_train])
    query=scaler.transform(vectors([data['target']]))
    scores=model.predict_proba(query)[0]
    return {'label':str(model.classes_[np.argmax(scores)]),'confidence':round(float(max(scores)),4),
            'coordinates':model.transform(query)[0].round(4).tolist(),
            'holdout_accuracy':round(float(model.score(scaler.transform(vectors(x_hold)),
                                          [r['pattern'] for r in x_hold])),4),'held_out':len(x_hold),
            'held_out_segments':[{'code': r['code'], 'pattern': r['pattern']} for r in x_hold]}
