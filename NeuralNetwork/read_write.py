import numpy as np
import csv

class ReadWrite:

    def __init__(self, train_images, train_label, test_images, test_predictions):
        self.train_images = train_images
        self.train_label = train_label
        self.test_images = test_images
        self.test_predictions = test_predictions

    def readInputFromFile(self):
        X_train = []
        with open(self.train_images, 'r') as rf:
            csvreader = csv.reader(rf)
            for row in csvreader:
                data = np.array([ float(char) for char in row])
                data = data / 256
                X_train.append(data)
        X_train = np.array(X_train)
        # print(X[1])

        Y_train = []
        with open(self.train_label, 'r') as rf:
            csvreader = csv.reader(rf)
            for row in csvreader:
                data = np.zeros(10)
                digit = int(row[0])
                data[digit] = 1
                Y_train.append(data)
        Y_train = np.array(Y_train)

        X_test = []
        with open(self.test_images, 'r') as rf:
            csvreader = csv.reader(rf)
            for row in csvreader:
                data = np.array([ float(char) for char in row])
                data = data / 256
                X_test.append(data)
        X_test = np.array(X_test)

        return X_train, Y_train, X_test 

    def writeOutputToFile(self, digits):
        with open(self.test_predictions, 'w') as wf:
            length = len(digits)
            for i in range(length - 1):
                d = str(digits[i]) + '\n'
                wf.write(d)
            d = str(digits[length - 1])
            wf.write(d)

if __name__ == "__main__":
    rw = ReadWrite("train_image.csv", "train_label.csv", "test_image.csv", "test_predictions.csv")
    rw.readInputFromFile()
    digits = [1,2,5,6,7,8]
    rw.writeOutputToFile(digits)