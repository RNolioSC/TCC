from numpy import genfromtxt
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import one_hot

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
    model.add(Dense(12, input_dim=3, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X, Y, epochs=30, batch_size=10)
    _, accuracy = model.evaluate(X, Y)
    print('Accuracy: %.2f' % (accuracy * 100))
    #tst = [[0.3333333333, 43745, 1], [0.0, 43745, 3], [0.2, 43745, 50], [0.8, 43745, 9]]
    predictions = model.predict_classes(X)
    # summarize some cases
    for i in range(60):
        #print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], Y[i]))
        print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], Y[i]))

