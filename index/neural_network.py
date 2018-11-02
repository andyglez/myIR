from numpy import dot
from math import exp
from utils import build_inputs, build_targets, normal_denominator


def train(neural_network, tf, idf):
    inputs = build_inputs(len(tf))
    targets = build_targets(tf, idf)

    for i in range(10):
        for input_vector, target_vector in zip(inputs, targets):
            backpropagate(neural_network, input_vector, target_vector)
    return neural_network


def backpropagate(neural_network, input_vector, targets):
    output = feed_forward(neural_network, input_vector)
    output_deltas = [output * (1 - output) * (output - target)
                     for output, target in zip(output[-1], targets)]
    i = len(neural_network) - 1
    while i > 0:
        adjust_weights(neural_network[i], output[i - 1], output_deltas)
        output_deltas = get_deltas(neural_network[i], output[i - 1], output_deltas)
        i -= 1
    adjust_weights(neural_network[0], input_vector, output_deltas)


def adjust_weights(layer, outputs, deltas):
    for i, output_neuron in enumerate(layer):
        for j, prev_neuron in enumerate(outputs):
            output_neuron[j] -= deltas[i] * prev_neuron


def get_deltas(layer, outputs, deltas):
    return [output * (1 - output) *
            dot(deltas, [n[i] for n in layer])
            for i, output in enumerate(outputs)]


def feed_forward(neural_network, input_vector):
    outputs = []
    for layer in neural_network:
        output = [neuron_output(neuron, input_vector)
                  for neuron in layer]
        outputs.append(output)
        input_vector = output
    return outputs


def neuron_output(weights, inputs):
    return sigmoid(dot(weights, inputs))


def sigmoid(t):
    return 1 / (1 + exp(-t))


