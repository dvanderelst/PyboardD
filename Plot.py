import textgraph
import array
import math


def plot(buffer, x_points=40,height=10):
    factor = math.ceil(len(buffer) / x_points)

    start = 0
    means = []
    while start < len(buffer):
        mean = buffer[start:start+factor]
        mean = sum(mean) / factor
        start = start + factor
        means.append(mean)
    means.pop(-1)
    graph = textgraph.vertical(means, height=10, character='*')
    min_value = min(buffer)
    max_value = max(buffer)
    return graph, min_value, max_value
