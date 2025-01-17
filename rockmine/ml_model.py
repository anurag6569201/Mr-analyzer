# importing dependies
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# createing dataframe from data
sonar_df=pd.read_csv('rockmine/sonar_data.csv',header=None)

# dividing dataframe into features and targets
features=sonar_df.drop(columns=60,axis=1)
targets=sonar_df[60]

# train test split
x_train,x_test,y_train,y_test=train_test_split(features,targets,stratify=targets,test_size=0.2,random_state=3)

model=LogisticRegression()
model.fit(x_train,y_train)

def training_accuracy_score():
    x_train_prediction=model.predict(x_train)
    training_data_accuracy=accuracy_score(x_train_prediction,y_train)
    training_data_accuracy=round(training_data_accuracy*100,2)
    return training_data_accuracy

def testing_accuracy_score():
    x_test_prediction=model.predict(x_test)
    testing_data_accuracy=accuracy_score(x_test_prediction,y_test)
    testing_data_accuracy=round(testing_data_accuracy*100,2)
    return testing_data_accuracy

def testing_data_result():
    y_test_np=np.asarray(y_test)
    return y_test_np.tolist()

def testing_data():
    x_test_np=np.asarray(x_test)
    return x_test_np.tolist()

def predicting_model(values):
    input_data = np.asarray(values)
    input_data_as_np=np.asarray(input_data)

    input_data_reshaped=input_data_as_np.reshape(1,-1)

    prediction = model.predict(input_data_reshaped)

    if(prediction[0]=='R'):
        print("Its rock")
        return 1
    else:
        print("Its mine")
        return 0