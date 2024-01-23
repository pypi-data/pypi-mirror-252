import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from numpy import inf


def collect_ids(s0):
    '''
    s0 is is a sentence from the doc parsed using md_benepar
    '''
    ids = {}

    def col_children(span):
        lst = list(span._.children)  # freeze ids
        ids[id(span)] = {'span': span, 'children': lst}
        [col_children(c) for c in lst]
    col_children(s0)
    return ids


def children_bfs(G, ids_to_spans, s0_id):
    for n in G.nodes:
        G.nodes[n]['color'] = 'WHITE'
        G.nodes[n]['d'] = inf
        G.nodes[n]['pred'] = None
    G.nodes[s0_id]['color'] = 'GRAY'
    G.nodes[s0_id]['d'] = 0
    G.nodes[s0_id]['pred'] = None
    q = []
    q.append(s0_id)  # enqueue
    while len(q) > 0:
        u = q.pop(0)  # dequeue
        children = ids_to_spans[u]['children']
        for child_span in children:  # search the neighbors of u
            v = id(child_span)
            # print(v, child_span)
            if G.nodes[v]['color'] == 'WHITE':
                G.nodes[v]['color'] = 'GRAY'
                G.nodes[v]['d'] = G.nodes[u]['d'] + 1

                # G.nodes[v]['pred'] = u
                l = child_span._.labels
                if len(l) >= 1:
                    G.add_edge(u, v, label=l[0])
                else:
                    if len(child_span) == 1:
                        # use POS if single token
                        G.add_edge(
                            u, v, label=child_span[0].tag_, color='green', fontcolor='green')
                    else:
                        # just edge
                        G.add_edge(u, v, label='')

                q.append(v)
        G.nodes[u]['color'] = 'BLACK'


def create_constituency_parse_graph(s0):
    ids_to_spans = collect_ids(s0)
    G = nx.DiGraph()
    [G.add_node(k, label=f"{k} {str(v['span'])}", span=v['span'])
     for k, v in ids_to_spans.items()]
    children_bfs(G, ids_to_spans, id(s0))
    return G
