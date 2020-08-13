"""
Kernal Support Vector Machine classification model to determine if someone will buy a new
SUV based on their age and salary.

Uses k-fold cross validation to find a more realistic and less optimistic accuracy
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import cross_val_score

"""
---------------Data Pre-processing---------------
"""
# Data not split into training and test set due to small amount of data being
# processed

# Importing dataset
dataset = pd.read_csv("../Data/Classification/Social_Network_Ads.csv")
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# 75% of data used for training and fixed random seed so that when re-ran same
# data in the train and test sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=0)

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""
---------------Training the Model---------------
"""
# Training kernal svm model on training set
# Uses the radial basis function as the kernal
# Parameter C=1.0 represents the inverse regularisation term.
# Smaller C means stronger regulrisation
classifier = SVC(kernel="rbf", random_state=42)
classifier.fit(X_train, y_train)

"""
---------------Predicting Single Result---------------
"""

single_prediction = classifier.predict([X_test[0, :]])
print("\nSingle Prediction")
print(f"Single prediction is {single_prediction}")
print(f"Actual answer is {y_test[0]}")

"""
---------------Predicting Test Set Result---------------
"""
y_pred = classifier.predict(X_test)
# Convert vectors from horizontal to vertical and display side by side to compare
# print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), axis=1))

"""
--------------Making the Confusion Matrix and Evaluating the Model---------------
"""

# Gives confusion matrix C such that Cij is equal to the number of observations known to be in group i and predicted to be in group j.
cm = confusion_matrix(y_test, y_pred)
true_positive = cm[1][1]
true_negative = cm[0][0]
false_positive = cm[0][1]
false_negative = cm[1][0]

print("\nModel Evaluation")
print(f"Accuracy is {accuracy_score(y_test, y_pred)}")
print(f"Precision is {true_positive / (true_positive + false_positive)}")
print(f"Recall is {true_positive / (true_positive + false_negative)}")
print(f"F1 score is {f1_score(y_test, y_pred, average='binary')}")

"""
---------------Applying K-Fold Cross Validation---------------
"""
# Using 10 folds
accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=10)
print(f"Accuracy: {accuracies.mean()*100}")
print(f"Standard Deviation: {accuracies.std()*100}")