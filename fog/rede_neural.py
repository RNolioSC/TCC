from numpy import genfromtxt
import numpy
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import one_hot
import keras
import keras.callbacks
from time import time


class TimingCallback(Callback):
  def __init__():
    self.logs=[]
  def on_epoch_begin(epoch, logs={}):
    self.starttime=time()
  def on_epoch_end(epoch, logs={}):
    self.logs.append(time()-self.starttime)

class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)


if __name__ == '__main__':

    dataset = genfromtxt(r'../simulacao/csv/cenarios_1_a_6.csv', encoding='latin-1', delimiter=',', skip_header=2,
                         usecols=(2, 3, 4, 5))
    X = dataset[:, 0:3]  # ultima linha - skip_header
    Y = dataset[:, 3]

    for i in range(0, len(X)):
        for j in range(0, len(X[0])):
            if numpy.isnan(X[i][j]):
                print(i, j)

    model = Sequential()
    model.add(Dense(12, input_dim=3, activation='sigmoid'))
    model.add(Dense(24, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

    #model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

    time_callback = TimeHistory()

    cb = TimingCallback()

    history = model.fit(X, Y, epochs=10, batch_size=10)
    #times = time_callback.times
    #print(times)
    print(cb.logs)

    _, accuracy = model.evaluate(X, Y)
    print('Accuracy: %.2f' % (accuracy * 100))
    #tst = [[0.3333333333, 43745, 1], [0.0, 43745, 3], [0.2, 43745, 50], [0.8, 43745, 9]]
    predictions = model.predict_classes(X)
    # summarize some cases
    #for i in range(60):
    #    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], Y[i]))

    # model.save('modelo.H5')

    '''
    # graficos de acuracia e validacao
    plt.plot(history.history['acc'])
    plt.ylabel('Acurácia')
    plt.xlabel('Época')
    plt.legend(['Treinamento'])
    plt.show()

    plt.plot(history.history['loss'])
    plt.ylabel('Perda')
    plt.xlabel('Época')
    plt.legend(['Treinamento'])
    plt.show()
    '''

