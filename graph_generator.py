import random
from settings import get_setting as S

class Graph:
    def __init__(self):
        self.nodes = set()
        self.graph_options = {}
        self.node_options = {}

    def graphviz(self):
        content = '\n'.join(node.graphviz() for node in self.nodes)

        graph_option_tuples = [(k, v) for k, v in self.graph_options.items()]
        graph_option_strs = ['{0}={1}'.format(k, v) for k, v in graph_option_tuples]

        node_option_tuples = [(k, v) for k, v in self.node_options.items()]
        node_option_strs = ['node[{0}={1}]'.format(k, v) for k, v in node_option_tuples]

        return 'graph G {\n' + \
            '\n'.join(graph_option_strs) + '\n' + \
            '\n'.join(node_option_strs) + '\n' + \
            content + '\n' + \
        '}'

class Node:
    def __init__(self, name):
        self.name = name
        self.links = set()

    def __str__(self):
        return '{0} ({1})'.format(self.name, len(self.links))

    def __hash__(self):
        return hash(self.name)

    def link(self, node):
        self.links.add(node)

    def graphviz(self):
        def links_generator():
            yield '{0} [label=""]'.format(self.name)
            for linked_node in self.links:
                yield '{0} -- {1}'.format(self.name, linked_node.name)

        return '\n'.join(list(links_generator()))

if __name__ == '__main__':

    def random_different_element(seq, not_this):
        assert len(seq) > 1
        while True:
            trial = random.choice(seq)
            if trial != not_this:
                return trial

    groups = []
    for g in range(S('graph.number_of_groups')):
        nodes = []
        for n in range(S('group.number_of_nodes')):
            name = 'n{0}x{1}'.format(g, n)
            nodes.append(Node(name))

        groups.append(nodes),

    # Ligações intra-grupos
    for group in groups:
        for node in group:
            number_of_links = S('group.intralinks_per_node')
            for i in range(number_of_links):
                linked_node = random_different_element(group, node)
                node.link(linked_node)

    for group in groups:
        for i in range(S('group.nodes_with_extralinks')):
            node = random.choice(group)
            number_of_links = S('group.extralinks_per_node')
            for i in range(number_of_links):
                other_group = random_different_element(groups, group)
                linked_node = random.choice(other_group)
                node.link(linked_node)

    graph = Graph()
    graph.graph_options['overlap'] = 'false'
    graph.graph_options['outputorder'] = 'edgesfirst'
    graph.node_options['style'] = 'filled'
    graph.node_options['regular'] = 'true'

    for group in groups:
        for node in group:
            graph.nodes.add(node)

    print(graph.graphviz())
