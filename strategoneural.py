# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:15:12 2018

@author: ylwaller
"""

#standard imports, mute what isn't needed
from sklearn import datasets
from sklearn import preprocessing
import numpy as np
from sklearn.cross_validation import train_test_split
import random
#from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
#import datetime
#from sklearn.ensemble import RandomForestClassifier
#from sklearn import model_selection
#from sklearn.metrics import binary_accuracy

#import pandas
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout, Dense
#from keras.utils import np_utils
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import KFold
#from sklearn.preprocessing import LabelEncoder
#from sklearn.pipeline import Pipeline
import keras
from keras import backend as K
#from keras.utils.np_utils import to_categorical
from keras import regularizers

'''
#old import from flat files, but since we ported our xmlparse to python 3 when we fixed its issues, the variables are just here so use them as they are.
import csv
wing = []
with open("stratvictor.csv", 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        wing.append(row)

wing=wing[0]
wing = list(map(int, wing))

chun = []
with open("stratdata.csv", 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        chun.append(row)

for row in range(5849549):
    for row2 in range(10):
        chun[row][row2] = chun[row][row2].replace("[","")
        chun[row][row2] = chun[row][row2].replace("]","")
        chun[row][row2] = chun[row][row2].replace(" ",",")
        chun[row][row2] = chun[row][row2].replace(",,",",")

tsun = []
for row in range(5849549):
    templist = []
    for row2 in range(10):
        try:
            templist.append(numpy.asarray(chun[row][row2].split(",")).astype(int))
        except:
            templist.append(numpy.asarray(chun[row][row2].split(",")[1:]).astype(int))
    tsun.append(templist)    

ving = []
for row in range(5849549):
    ving.append(numpy.vstack(tsun[row]))
'''

#450, 300

seed = 90876
np.random.seed(seed)

randindices = np.random.choice(5849549,int(*5849549))

'''
xving = [ving[i] for i in randindices]
ywing = [wing[i] for i in randindices]
'''

#xving = [allmoves[i] for i in randindices]
#ywing = [whowon[i] for i in randindices]

xving = allmoves
ywing = whowon

counter=0
for matrix in xving:
    xving[counter] = np.interp(matrix, (-1, 31), (-1, +1))
    counter+=1

x_train, x_test, y_train, y_test = train_test_split(xving, ywing, test_size=0.2)

x_train = np.array(x_train)
y_train = np.array(y_train)

x_train = x_train.reshape(len(x_train),10,10,1)

K.clear_session()
model2 = Sequential()
model2.add(Conv2D(40, kernel_size=(3, 3), strides=(1, 1), activation='relu', input_shape=(10,10,1)))
model2.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model2.add(keras.layers.Flatten())
model2.add(BatchNormalization())
model2.add(Dense(500, activation='tanh'))
model2.add(Dropout(0.01)) #this really hurt accuracy at .5 (I wonder why :P)
model2.add(keras.layers.Dense(75, activation='tanh'))
model2.add(BatchNormalization())
model2.add(Dense(10, activation='sigmoid'))
model2.add(BatchNormalization())
model2.add(Dense(1,kernel_initializer='normal',activation='sigmoid'))
optimizerr = keras.optimizers.SGD(lr=0.5, momentum=0.01, decay=0.01, nesterov=True)
model2.compile(optimizer=optimizerr, loss='binary_crossentropy', metrics=['binary_accuracy'])

model2.fit(x_train, y_train,epochs = 40, batch_size = 128, verbose=1)



x_test = np.array(x_test)
y_test = np.array(y_test)

x_test = x_test.reshape(len(x_test),10,10,1)

#model.evaluate(x_test,y_test)
predstest=model2.predict_classes(x_test)
conf = confusion_matrix(y_test,predstest)
(conf[0,0]+conf[1,1])/len(y_test)

predstest=model2.predict_classes(x_train)
conf = confusion_matrix(y_train,predstest)
(conf[0,0]+conf[1,1])/len(y_train)


#model.save('neuralstrategoALL.h5')







