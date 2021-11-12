import textgraph
import array
import math



def plot(buffer, x_points=50, size=30, threshold=0):
    factor = math.ceil(len(buffer) / x_points)
    start = 0
    means = []
    while start < len(buffer):
        mean = buffer[start:start+factor]
        mean = int((sum(mean) / factor) - threshold)
        if mean < 0: mean = 0
        start = start + factor
        means.append(mean)
    means.pop(-1)
    #graph = textgraph.vertical(means, height=size, character='#')
    try:
        graph = textgraph.horizontal(means, width=size, character='=')
    except Exception as e:
        graph = str(e)
    min_value = min(buffer)
    max_value = max(buffer)
    graph = graph.replace('\n','<br>')
    return graph, min_value, max_value