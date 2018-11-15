import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import os
from keras.models import Sequential
from keras.layers import Dense
import numpy

root_dir = "/home/acevikel/localizenet/src/"
train_X_dir = root_dir+"train/scan/"
train_Y_dir = root_dir+"train/label/"
test_X_dir = root_dir+"test/scan/"
test_Y_dir = root_dir+"test/label/"
train_X_list = []
train_Y_list = []
test_X_list = []
test_Y_list = []


for filename in os.listdir(train_X_dir):
    train_X_list.append(np.load(os.path.join(train_X_dir,filename)))
    train_Y_list.append(np.load(os.path.join(train_Y_dir,filename)))

for filename in os.listdir(test_X_dir):
    test_X_list.append(np.load(os.path.join(test_X_dir,filename)))
    test_Y_list.append(np.load(os.path.join(test_Y_dir,filename)))


train_X = np.column_stack(train_X_list).T
test_X = np.column_stack(test_X_list).T
train_labels = np.column_stack(test_Y_list+train_Y_list).T
train_Y_raw = np.column_stack(train_Y_list).T
test_Y_raw = np.column_stack(test_Y_list).T

mlb = MultiLabelBinarizer()
mlb.fit(train_labels)
train_Y= mlb.transform(train_Y_raw)
test_Y= mlb.transform(test_Y_raw)

model = Sequential()
model.add(Dense(1024, input_dim=360, kernel_initializer='uniform', activation='relu'))
model.add(Dense(512, kernel_initializer='uniform', activation='relu'))
model.add(Dense(103, kernel_initializer='uniform', activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_X, train_Y, epochs=5, batch_size=32,  verbose=2)

score, acc = model.evaluate(test_X,test_Y,batch_size=32)

print "Training finished with accuracy {0}".format(acc)



