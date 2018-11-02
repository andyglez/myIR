from numpy import dot
from math import sqrt
from utils import build_inputs, build_targets, normal_denominator


def train(neural_network, tf, idf):
    inputs = build_inputs(len(tf))
    targets = build_targets(tf, idf)

    for i in range(10):
        for input_vector, target_vector in zip(inputs, targets):
            backpropagate(neural_network, input_vector, target_vector)
    return neural_network


def backpropagate(neural_network, input_vector, targets):
    outputs = feed_forward(neural_network, input_vector)
    outputs.insert(0, input_vector)
    count = 1
    while len(outputs) > 1:
        output_deltas = [output * (1 - output) * (output - target)
                         for output, target in zip(outputs[-1], targets)]

        for i, output_neuron in enumerate(neural_network[-count]):
            for j, prev_output in enumerate(outputs[-1]):
                output_neuron[j] -= output_deltas[i] * prev_output

        prev_deltas = [prev_output * (1 - prev_output) *
                       dot(output_deltas, [n[i] for n in neural_network[-count]])
                       for i, prev_output in enumerate(neural_network[-(count+1)])]

        outputs.remove(outputs[-1])
        count += 1
        targets = []

        for i, prev_neuron in enumerate(outputs[-1]):
            targets.append(prev_neuron - prev_deltas * outputs[-2])


def feed_forward(neural_network, input_vector):
    outputs = []
    for layer in neural_network:
        output = [neuron_output(neuron, input_vector)
                  for neuron in layer]
        outputs.append(output)
        input_vector = output
    return outputs


def neuron_output(weights, inputs):
    return dot(weights, inputs) / (normal_denominator(weights) * normal_denominator(inputs))

