# importing dependies
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

# createing dataframe from data
diabetes_data=pd.read_csv('diabetes/diabetes.csv')

# seprating the features and targets
features=diabetes_data.drop(columns='Outcome',axis=1)
target=diabetes_data['Outcome']

# standardizing the data
scaler=StandardScaler()
scaler.fit(features)
standardized_data=scaler.transform(features)

X=standardized_data
Y=diabetes_data['Outcome']

# train and test
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

# Traning the classifier using the train data
classifier=svm.SVC(kernel='linear')
classifier.fit(x_train,y_train)

# accuracy on training moodel
def training_accuracy_score():
    x_train_prediction=classifier.predict(x_train)
    training_data_accuracy=accuracy_score(y_train,x_train_prediction)
    training_data_accuracy=round(training_data_accuracy*100,2)
    return training_data_accuracy

# accuracy on testing moodel
def testing_accuracy_score():
    x_test_prediction=classifier.predict(x_test)
    testing_data_accuracy=accuracy_score(y_test,x_test_prediction)
    testing_data_accuracy=round(testing_data_accuracy*100,2)
    return testing_data_accuracy

def testing_data_result():
    y_test_np=np.asarray(y_test)
    return y_test_np.tolist()

def testing_data():
    x_test_np=np.asarray(x_test)
    return x_test_np.tolist()

def predicting_model(values):
    print(values)
    input_data=(values)

    # change the input data to numpy array
    input_data_as_numpy=np.asarray(input_data)

    # reshaping the numpy data
    input_data_reshaped=input_data_as_numpy.reshape(1,-1)

    # standardizing the data
    std_data=scaler.transform(input_data_reshaped)
    print(std_data)

    prediction=classifier.predict(std_data)
    print(prediction)

    if(prediction[0]==0):
        print("Person is diabetics")
        return 0
    else:
        print("Person is not diabetic")
        return 1
