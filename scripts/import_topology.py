import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")
from general_node.models import general_node
from topology.models import topology
from graph.models import graph
from Phage_api import settings_local as local_settings
from ast import literal_eval
import pandas as pd

django.setup()

def _corr(species, uid, topology_id):
    with open(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/corr.csv', 'r') as f:
        csv_lines = f.readlines()
    for line in csv_lines[1:]:
        l = line.strip().split(",")
        general_node.objects.create(
            topology_id = topology_id,
            node_name = l[0],
            x = float(l[1]),
            y = float(l[2]),
            z = float(l[3]),
        )

# def _graph_old(species, uid, topology_id, graph_type, pkl_list):
#     graph_info = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_type + '/graph.csv').to_numpy()
#     edge_info = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_type + '/edge.csv', index_col=0).to_numpy().tolist()

#     obj = graph.objects.create(
#         topology_id = topology_id,
#         type = graph_type,
#         edges = edge_info,
#         average_branching_factor = graph_info[0][1],
#         modularity = graph_info[1][1],
#         span = graph_info[2][1],
#         assortativity = graph_info[3][1],
#         degree_centrality = graph_info[4][1],
#         closeness_centrality = graph_info[5][1],
#         betweenness_centrality = graph_info[6][1],
#         graph_pkl_list = pkl_list,
#     )
#     return obj.id

# def _node_old(species, uid, graph_id, graph_type):
#     node_info = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_type + '/node.csv').to_numpy()
#     for _ in node_info:
#         graph_node.objects.create(
#             graph_id = graph_id,
#             node_name = _[0],
#             degrees = _[1],
#             degree_centrality = _[2],
#             betweenness = _[3],
#             closeness_centrality = _[4],
#             page_rank_score = _[5],
#         )

def _graph(species, uid, topology_id, graph_type, pkl, graph_folder):
    graph_info = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_type + '/' + graph_folder + '/graph.csv').to_numpy()

    obj = graph.objects.create(
        topology_id = topology_id,
        type = graph_type,
        pkl = pkl,
        graph_folder = graph_folder,

        average_branching_factor = graph_info[0][1],
        modularity = graph_info[1][1],
        span = graph_info[2][1],
        assortativity = graph_info[3][1],
        degree_centrality = graph_info[4][1],
        closeness_centrality = graph_info[5][1],
        betweenness_centrality = graph_info[6][1],
    )
    return obj.id

def add_data():

    TOPOLOGY_INFO = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'main/TOPOLOGY_INFO.csv', dtype=str, index_col=0).to_numpy()
    for l in TOPOLOGY_INFO:
        species = l[0]
        uid = l[1]
        graph_type = l[2]
        pkl = l[3]
        graph_folder = l[4]
        topology_qs = topology.objects.filter(repeat_data_uid = uid)

        if len(topology_qs) != 0 and len(topology_qs) != 1:
            print('Error in import_topology.py')
            return
        if len(topology_qs) == 0:
            topology_obj = topology.objects.create(
                repeat_data_uid = uid,
                graph_list = []
            )
            _corr(species, uid, topology_obj.id)
            
        topology_qs = topology.objects.filter(repeat_data_uid = uid)
        topology_obj = topology_qs.first()
        graph_id = _graph(species, uid, topology_obj.id, graph_type, pkl, graph_folder)
        graph_list = topology_obj.graph_list
        graph_list.append(graph_id)
        topology_qs.update(graph_list = graph_list)


if __name__ == "__main__":
    add_data()
