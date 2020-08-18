from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn
import pandas as pd
import matplotlib.pyplot as plt

class LR():
    X_train = None
    X_test = None
    y_train = None
    y_test = None
    
    def train(self, X, y, max_iter, test_size, param_grid=[{}]):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=42, test_size=test_size)
        pipe = Pipeline(
                [('select', SelectFromModel(LogisticRegression(class_weight='balanced',
                                                          penalty="l2", C=0.01, max_iter=max_iter ))),
                ('model', LogisticRegression(class_weight='balanced',penalty='l2', max_iter=max_iter ))])

        param_grid = param_grid # Optionally add parameters here
        grid_search = GridSearchCV(pipe, 
                           param_grid,
                           cv=StratifiedKFold(n_splits=5, 
                                              random_state=42).split(self.X_train, self.y_train), 
                           verbose=2,
                           n_jobs=-1
                          )
        model = grid_search.fit(self.X_train, self.y_train)
        return model
    
    def predict(self,model, X_test=None):
        if not X_test:
            X_test = self.X_test
        y_pred = model.predict(X_test)
        return y_pred
    
    def gen_report(self, y_test = None, y_pred = None):
        if not y_test:
            y_test = self.y_test
        return classification_report(y_test, y_pred)
    
    def gen_confusion_matrix(self, y_test = None, y_pred = None):
        if not y_test:
            y_test = self.y_test
        confusion_mat = confusion_matrix(y_test, y_pred)
        matrix_proportions = np.zeros((3,3))
        for i in range(0,3):
            matrix_proportions[i,:] = confusion_mat[i,:]/float(confusion_mat[i,:].sum())
        names=['Hate','Offensive','Neither']
        confusion_df = pd.DataFrame(matrix_proportions, index=names,columns=names)
        plt.figure(figsize=(5,5))
        seaborn.heatmap(confusion_df,annot=True,annot_kws={"size": 12},cmap='gist_gray_r',cbar=False, square=True,fmt='.2f')
        plt.ylabel(r'True categories',fontsize=14)
        plt.xlabel(r'Predicted categories',fontsize=14)
        plt.tick_params(labelsize=12)