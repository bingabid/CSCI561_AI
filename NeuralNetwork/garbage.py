import numpy as np
# weights = [[0.2, 0.8, -0.5, 1.0],
#           [0.5, -.91, 0.26, -0.5],
#           [-0.26, -0.27, 0.17, 0.87]]
# biases = [2, 3, 0.5]
# output = np.dot(inputs, np.array(weights).T) + biases
# print(output)

class NueralNetwork:
    def __init__(self):
        self.layers = 1

    def softmax(self, signal):
        e = np.exp(signal)
        return e/e.sum()

if __name__ == '__main__':
    data = [1, 3, 2]
    obj = NueralNetwork()
    print(obj.softmax(data))




# print(layer.weights)
# print(layer.biases)
# print(layer.signals)
# print(layer.outputs)

final = FinalLayer(3, 2)
final.forward(layer.outputs)
final.calculate_delta(y)
print(final.deltas)
# print(final.inputs)
# print(final.weights)
# w = final.weights
print("before: ", final.biases)
final.backward()
# print(final.inputsT)
# print(w - final.weights)
print("after: ", final.biases)

print("-----------")
layer.calculate_delta(final.weights, final.deltas)
w = layer.weights
# print(w)
print("layer before d: ", layer.deltas.T)
p = layer.deltas.T
print("layer before b: ", layer.biases)
q = layer.biases
print(q - 0.1 * p)
layer.backward()
# print(w - layer.weights)
print("after: ", layer.biases)

# print(layer.deltas)
# d = layer.deltas
# i = layer.inputs
# # i = i.reshape((1,len(i)))
# print(i.T)
# print(d)

# ---------------------------

X = X.reshape((1,len(X)))
# layers
layer1 = HiddenLayer(3,3)
layer2 = HiddenLayer(3,4)
layer3 = HiddenLayer(4,7)
final  = FinalLayer(7,3)

# forward pass
layer1.forward(X)
layer2.forward(layer1.outputs)
layer3.forward(layer2.outputs)
final.forward(layer3.outputs)

# deltas pass
final.calculate_delta(y)
layer3.calculate_delta(final.weights, final.deltas.T)
layer2.calculate_delta(layer3.weights, layer3.deltas)
layer1.calculate_delta(layer2.weights, layer2.deltas)

# backward pass
final.backward()
layer3.backward()
layer2.backward()
layer1.backward()

