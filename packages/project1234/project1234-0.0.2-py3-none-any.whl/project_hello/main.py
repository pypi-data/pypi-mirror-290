def dl_index():
    print('''

  dl_p1a: matrix multiplication and finding eigen vectors
  dl_p1b: Random Matrix
  dl_p2:  Solving XOR problem using deep feed forward network
  dl_p3:  Implementing deep neural network for performing binary classification task.
  dl_p4a: Using Feed Forward Network with multiple hidden layers for performing multiclass classification and predicting the class.
  dl_p4b: Using a deep feed forward network with two hidden layers for performing classification and predicting the probability of class.
  dl_p5a: Evaluating feed forward deep network for regression using KFold cross validation.
  dl_p5b: Evaluating feed forward deep network for multiclass Classification using KFold cross-validation.
  dl_p6a: Implement 12 regularization with alpha=0.001
  dl_p6b: Evaluating feed forward deep network for multiclass Classification using KFold cross-validation.
  dl_p6c: Replace 12 regularization with l1 regularization.
  dl_p7:  Demonstrate recurrent neural network that learns to perform sequence analysis for stock price.
  dl_p8:  Performing encoding and decoding of images using deep autoencoder.
  dl_p9:  Implementation of convolutional neural network to predict numbers from number
  dl_p10: Denoising of images using autoencoder.


  ''')


def dl_p1a():
    print('''

import tensorflow as tf
print("Matrix Multiplication Demo")
x=tf.constant([1,2,3,4,5,6],shape=[2,3])
print(x)
y=tf.constant([7,8,9,10,11,12],shape=[3,2])
print(y)
z=tf.matmul(x,y)
print("Product:",z)
e_matrix_A=tf.random.uniform([2,2],minval=3,maxval=10,dtype=tf.float32,name="matrixA")
print("Matrix A:\\n{}\\n\\n".format(e_matrix_A))
eigen_values_A,eigen_vectors_A=tf.linalg.eigh(e_matrix_A)
print("Eigen Vectors:\\n{}\\n\\nEigen Values:\\n{}\\n".format(eigen_vectors_A,eigen_values_A))


''')


def dl_p1b():
    print('''

import tensorflow as tf
random_matrix = tf.random.uniform(shape=[3, 3], minval=1, maxval=10)
eigenvalues, eigenvectors = tf.linalg.eigh(random_matrix)
# Print the results
print("Random Matrix:\\n", random_matrix.numpy())
print("\\nEigenvalues:\\n", eigenvalues.numpy())
print("\\nEigenvectors:\\n", eigenvectors.numpy())



''')


def dl_p2():
    print('''

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
model=Sequential()
model.add(Dense(units=2,activation='relu',input_dim=2))
model.add(Dense(units=1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())
print(model.get_weights())
X=np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
Y=np.array([0.,1.,1.,0.])
model.fit(X,Y,epochs=1000,batch_size=4)
print(model.get_weights())
print(model.predict(X,batch_size=4))



''')


def dl_p3():
    print('''

#!pip install keras
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
names =["No. of pregnancies","Glucose level","Blood Pressure","skin thickness","Insulin","BMI","Diabetes pedigree","Age","Class"]
df=pd.read_csv("pima-indians-diabetes.data.csv",names = names)
print(df.head(3))
binaryc = Sequential()
from tensorflow.tools.docs.doc_controls import doc_in_current_and_subclasses
binaryc.add(Dense(units=10,activation='relu',input_dim=8))
binaryc.add(Dense(units=8,activation='relu'))
binaryc.add(Dense(units=1,activation='sigmoid'))
binaryc.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
X =df.iloc[:,:-1]
y = df.iloc[:,-1]
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size = 0.25, random_state=1)
xtrain.shape
ytrain.shape
binaryc.fit(xtrain,ytrain,epochs=200,batch_size=20)
predictions=binaryc.predict(xtest)
predictions.shape
class_labels=[]
for i in predictions:
    if(i>0.5):
        class_labels.append(1)
    else:
        class_labels.append(0)
class_labels
from sklearn.metrics import accuracy_score
print('Accuracy Score', accuracy_score(ytest,class_labels))



''')


def dl_p4a():
    print('''

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
df=pd.read_csv("flowers.csv")
print(df.head())
X =df.iloc[:,:-1].astype(float)
y = df.iloc[:,-1]
print(X.shape) ##print not necessary
print(y.shape) ##print not necessary
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
y = lb.fit_transform(y)
print(y)
##print not necessary
from tensorflow.keras.utils import to_categorical
encoded_Y = to_categorical(y)
print(encoded_Y) ##print not necessary
model = Sequential()
model.add(Dense(8,activation='relu',input_dim=4))
model.add(Dense(6,activation='relu'))
model.add(Dense(3,activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
odel.fit(X,encoded_Y,epochs=100,batch_size=10)
predictions = model.predict(X)
for i in range(35,130,3):
    print(predictions[i],encoded_Y[i])
import numpy as np
a =[]
for i in range(0,150):
    a.append(np.argmax(predictions[i]))
newdf = pd.DataFrame(list(zip(a,y)),columns = ['Predicted','True Label'])
print(newdf)


''')


def dl_p4b():
    print('''

from keras.models import Sequential
from keras.layers import Dense,InputLayer
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
X, Y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
# Normalize data
scaler = MinMaxScaler()
scaler.fit(X)
X =scaler.transform(X)
# Create model
model = Sequential()
model.add(InputLayer(input_shape=(2,)))
model.add(Dense(4, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model with binary crossentropy loss
model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(X, Y, epochs=500)
Xnew, Yreal = make_blobs(n_samples=3, centers=2, n_features=2, random_state=1)
Xnew = scaler.transform(Xnew)
Ynew = model.predict(Xnew)
# Convert to class predictions
Yclass = (Ynew > 0.5).astype(int)
print(Yclass)
for i in range(len(Xnew)):
    print(f"X={Xnew[i]},Predicted_probability={Ynew[i]},Predicted_class={Yclass[i]}")



''')


def dl_p5a():
    print('''

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor
# Load the dataset correctly, skipping the first row (header)
dataframe = pd.read_csv("housing.csv", sep=',', header=0)
print("Shape of dataset:", dataframe.shape)
print("First few rows of dataset:")
print(dataframe.head())
# Extract features (X) and target variable (Y)
X =dataframe.drop(columns=['MEDV']).values
# Features (all columns except 'MEDV')
Y =dataframe['MEDV'].values
#Target variable ('MEDV')
# Check the shape of X (number of features)
print("Shape of X (features):", X.shape)
# Define the wider model function
def wider_model():
    model = Sequential()
    model.add(Dense(15,input_dim=X.shape[1], kernel_initializer='normal' , activation='relu'))
    model.add(Dense(13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model
#Create pipeline with standardization and Keras model
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp',KerasRegressor(build_fn=wider_model, epochs=10, batch_size=5)))
pipeline = Pipeline(estimators)
# Define KFold cross-validation
kfold = KFold(n_splits=10, shuffle=True, random_state=42)
try:
    # Evaluate pipeline using cross-validation
    results = cross_val_score(pipeline, X, Y, cv=kfold)
    print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))
except ValueError as e:
    print("Error during cross-validation:", e)



''')


def dl_p5b():
    print('''

from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score
# Generate a random multiclass classification dataset
X, y = make_classification(n_samples=100,
n_features=20,
n_informative=2,
n_redundant=0,
n_classes=2,
n_clusters_per_class=2,
random_state=42)
# Convert the target variable to categorical format
y = to_categorical(y)
# Define the k-fold cross-validator
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
# Define the feed-forward deep network model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Perform k-fold cross-validation
fold_accuracies = []
for train_index, val_index in kf.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))
    y_pred_prob = model.predict(X_val)
    y_pred = y_pred_prob.argmax(axis=1) # Get the predicted class index with highest probability
    accuracy = accuracy_score(y_val.argmax(axis=1), y_pred)
    fold_accuracies.append(accuracy)
# Calculate the mean accuracy across all folds
mean_accuracy = sum(fold_accuracies) / len(fold_accuracies)
print(f'Mean accuracy: {mean_accuracy:.2f}')



''')


def dl_p6a():
    print('''

from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=4000)
pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()


''')


def dl_p6b():
    print('''

from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
from keras.regularizers import l2
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l2(0.001)))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=4000)
pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()



''')


def dl_p6c():
    print('''

from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
from keras.regularizers import l1_l2
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l1_l2(l1=0.001,l2=0.001)
))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=4000)
pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()


''')


def dl_p7():
    print('''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
# Importing the training dataset
dataset_train = pd.read_csv('C:/Users/HP/Downloads/Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values
# Scaling the training set
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)
X_train = []
Y_train = []
for i in range(60, 1258):
    X_train.append(training_set_scaled[i-60:i, 0])
    Y_train.append(training_set_scaled[i, 0])
X_train, Y_train = np.array(X_train), np.array(Y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
# Building the LSTM model
regressor = Sequential()
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))
# Compiling the model
regressor.compile(optimizer='adam', loss='mean_squared_error')
# Fitting the model to the training set
regressor.fit(X_train, Y_train, epochs=100, batch_size=32)
# Predicting the stock prices
dataset_test = pd.read_csv('C:/Users/HP/Downloads/Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis=0)
inputs = dataset_total[len(dataset_total)- len(dataset_test)- 60:].values
inputs = inputs.reshape(-1, 1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
# Inverse scaling for predicted prices
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
plt.plot(real_stock_price, color='red', label='Real Google Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Price')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()



''')


def dl_p8():
    print('''

import keras
from keras import layers
from keras.datasets import mnist
import numpy as np
encoding_dim = 32
input_img = keras.Input(shape=(784,))
#Input image
# "encoded" is the encoded representation of the input
encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = layers.Dense(784, activation='sigmoid')(encoded)
# Creating autoencoder model
autoencoder = keras.Model(input_img, decoded)
encoder = keras.Model(input_img, encoded) #Create the encoder model
encoded_input = keras.Input(shape=(encoding_dim,))
# Retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# Create the decoder model
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
# Scale and make train and test dataset
(X_train, _), (X_test, _) = mnist.load_data()
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
X_train = X_train.reshape((len(X_train), np.prod(X_train.shape[1:])))
X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))
print(X_train.shape)
print(X_test.shape)
# Train autoencoder with training dataset
autoencoder.fit(X_train, X_train,
epochs=50,
batch_size=256,
shuffle=True,
validation_data=(X_test, X_test))
encoded_imgs = encoder.predict(X_test)
decoded_imgs = decoder.predict(encoded_imgs)
import matplotlib.pyplot as plt
n =10
plt.figure(figsize=(40, 4))
for i in range(10):
# Howmanydigits we will display
    ax = plt.subplot(3, 20, i + 1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax = plt.subplot(3, 20, i + 1 + 20)
    # Display original
    # Display encoded image
    plt.imshow(encoded_imgs[i].reshape(8, 4)) # Adjust shape if necessary
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax = plt.subplot(3, 20, 2 * 20 + i + 1)
    # Display reconstruction
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()




''')


def dl_p9():
    print('''

from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten
import matplotlib.pyplot as plt
#download mnist data and split into train and test sets
(X_train,Y_train),(X_test,Y_test)=mnist.load_data()
#plot the first image in the dataset
plt.imshow(X_train[0])
plt.show()
print(X_train[0].shape)
X_train=X_train.reshape(60000,28,28,1)
X_test=X_test.reshape(10000,28,28,1)
Y_train=to_categorical(Y_train)
Y_test=to_categorical(Y_test)
Y_train[0]
print(Y_train[0])
model=Sequential()
#add model layers
#learn image features
model.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(28,28,1)))
model.add(Conv2D(32,kernel_size=3,activation='relu'))
model.add(Flatten())
model.add(Dense(10,activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
#train
model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=3)
print(model.predict(X_test[:4]))
#actual results for 1st 4 images in the test set
print(Y_test[:4])


''')


def dl_p10():
    print('''

import keras
from keras.datasets import mnist
from keras import layers
import numpy as np
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
(X_train, _), (X_test, _) = mnist.load_data()
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
X_train = np.reshape(X_train, (len(X_train), 28, 28, 1))
X_test = np.reshape(X_test, (len(X_test), 28, 28, 1))
noise_factor = 0.5
X_train_noisy = X_train + noise_factor * np.random.normal(loc=0.0, scale=1.0,
size=X_train.shape)
X_test_noisy = X_test + noise_factor * np.random.normal(loc=0.0, scale=1.0,
size=X_test.shape)
X_train_noisy = np.clip(X_train_noisy, 0., 1.)
X_test_noisy = np.clip(X_test_noisy, 0., 1.)
n =10
plt.figure(figsize=(20, 2))
for i in range(1, n + 1):
    ax = plt.subplot(1, n, i)
    plt.imshow(X_test_noisy[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
input_img = keras.Input(shape=(28, 28, 1))
x =layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x =layers.MaxPooling2D((2, 2), padding='same')(x)
x =layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2, 2), padding='same')(x)
x =layers.Conv2D(32, (3, 3), activation='relu', padding='same')(encoded)
x =layers.UpSampling2D((2, 2))(x)
x =layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x =layers.UpSampling2D((2, 2))(x)
decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(X_train_noisy, X_train,
    epochs=3,
    batch_size=128,
    shuffle=True,
    validation_data=(X_test_noisy, X_test),
    callbacks=[TensorBoard(log_dir='/tmo/tb', histogram_freq=0, write_graph=False)])
predictions = autoencoder.predict(X_test_noisy)
m=10
plt.figure(figsize=(20, 2))
for i in range(1, m + 1):
    ax = plt.subplot(1, m, i)
    plt.imshow(predictions[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

 

''')
