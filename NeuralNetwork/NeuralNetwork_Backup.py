import numpy as np
from read_write import ReadWrite
from timeit import default_timer as timer

np.random.seed(1)
class HiddenLayer:
    def __init__(self, n_inputs, n_neurons):
        self.neurons = n_neurons
        self.weights = np.random.randn(n_inputs, self.neurons)
        self.biases = np.zeros((1, n_neurons))

    def sigmoid(self):
        return 1 / (1 + np.exp(-self.signals))

    def sigmoid_derivative(self):
        derivative = self.outputs * (1 - self.outputs)
        return derivative

    def forward(self, inputs):
        self.inputs = np.array(inputs)
        self.signals = np.dot(inputs, self.weights) + self.biases
        self.signals = np.clip(self.signals, -100, 100)
        self.outputs = self.sigmoid()
    
    def calculate_delta(self, weights, deltas):
        partial = np.dot(weights, deltas)
        derivative = self.sigmoid_derivative()
        self.deltas = partial * derivative.T
    
    def backward(self, learning_rate = 0.1):
        self.inputsT = self.inputs
        self.inputsT = self.inputs.T
        self.weights = self.weights - learning_rate * np.dot(self.inputsT, self.deltas.T)
        self.biases  = self.biases - learning_rate * self.deltas.T



class FinalLayer:
    def __init__(self, n_inputs, n_neurons):
        self.neurons = n_neurons
        self.weights = np.random.randn(n_inputs, self.neurons)
        self.biases = np.zeros((1, n_neurons))
    
    
    def softmax(self):
        exp_values = np.exp(self.signals - np.max(self.signals))
        # exp_values = np.exp(self.signal)
        probabilities = exp_values / exp_values.sum()
        return probabilities
    
    def forward(self, inputs):
        self.inputs = np.array(inputs)
        self.signals = np.dot(self.inputs, self.weights) + self.biases
        # self.signals = np.clip(self.signals, -100, 100)
        self.outputs = self.softmax()

    def calculate_delta(self, output_true):
        self.deltas = self.outputs - output_true
        return self.deltas
    
    def backward(self, learning_rate = 0.1):
        self.inputsT = self.inputs
        self.inputsT = self.inputs.T
        # self.inputsT = self.inputsT.reshape(len(self.inputsT),1)
        self.weights = self.weights - learning_rate * np.dot(self.inputsT, self.deltas)
        self.biases  = self.biases - learning_rate * self.deltas

if __name__ == "__main__":

    # start = timer()

    rw = ReadWrite("train_image.csv", "train_label.csv", "test_predictions.csv")
    X, Y = rw.readInputFromFile()
    X_train, Y_train, X_Test = X[:50000], Y[:50000]
    X_test, Y_test = X[50000:], Y[50000:]

    # model
    # layer = HiddenLayer(784,100)
    # layer2 = HiddenLayer(100,65)
    # layer3 = HiddenLayer(65,35)
    # final  = FinalLayer(35,10)
    layer = HiddenLayer(784,25)
    final  = FinalLayer(25,10)
    epochs = 100
    for epoch in range(epochs):
        # train the model using SGD
        sample_train = len(X_train)
        for i in range(sample_train):
            x_train, y_train = X_train[i], Y_train[i]
            x_train = x_train.reshape((1,len(x_train)))

            # forward pass
            # layer1.forward(x_train)
            # layer2.forward(layer1.outputs)
            # layer3.forward(layer2.outputs)
            # final.forward(layer3.outputs)
            layer.forward(x_train)
            final.forward(layer.outputs)

            # deltas pass
            # final.calculate_delta(y_train)
            # layer3.calculate_delta(final.weights, final.deltas.T)
            # layer2.calculate_delta(layer3.weights, layer3.deltas)
            # layer1.calculate_delta(layer2.weights, layer2.deltas)
            final.calculate_delta(y_train)
            layer.calculate_delta(final.weights, final.deltas.T)

            # backward pass
            # final.backward()
            # layer3.backward()
            # layer2.backward()
            # layer1.backward()
            final.backward()
            layer.backward()

        # epoch wise accuracy calculation
        acc = 0
        sample_test = len(X_test)
        for i in range(sample_test):
            x_test, y_test = X_test[i], Y_test[i]
            x_test = x_test.reshape((1,len(x_test)))
            # layer1.forward(x_test)
            # layer2.forward(layer1.outputs)
            # layer3.forward(layer2.outputs)
            # final.forward(layer3.outputs)
            layer.forward(x_test)
            final.forward(layer.outputs)
            prediction = np.argmax(final.outputs)
            actual = np.argmax(y_test)
            if actual == prediction:
                acc += 1
        print("Epoch: ", epoch, "sample_test", sample_test, " accurate:", acc, "Accuracy: ", acc/sample_test)