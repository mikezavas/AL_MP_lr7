class AdjacencyList:

    def __init__(self):
        self.nodes = {}

    def add(self, node_id, name, parent_id=None):
        self.nodes[node_id] = {
            'id': node_id,
            'name': name,
            'parent_id': parent_id,
            'children': []
        }

        if parent_id in self.nodes:
            self.nodes[parent_id]['children'].append(node_id)

    def print_tree(self, start_id=None, indent=0):
        if start_id is None:
            for node in self.nodes.values():
                if node['parent_id'] is None:
                    self.print_tree(node['id'], 0)
            return

        node = self.nodes[start_id]
        indent_str = "  " * indent

        print(f"{indent_str}{node['name']}({node['id']}), parent_id({node['parent_id']})")

        for child_id in node['children']:
            self.print_tree(child_id, indent + 1)


al_tree = AdjacencyList()
al_tree.add(0, "Transport")
al_tree.add(1, "Boat", 0)
al_tree.add(2, "SailBoat", 1)
al_tree.add(3, "Yacht", 1)
al_tree.add(4, "AirCraft", 0)
al_tree.add(5, "Jet", 4)
al_tree.add(6, "AirBus", 4)
al_tree.add(7, "Helicopter", 4)
al_tree.add(8, "Car", 0)
al_tree.add(9, "Sedan", 8)
al_tree.add(10, "Truck", 8)

print("\nИсходное Adjacency List дерево:")
al_tree.print_tree()


class MaterializedPath:

    def __init__(self):
        self.nodes = {}

    def add(self, path_list, name):
        path_str = str(path_list)
        self.nodes[path_str] = {
            'name': name,
            'path': path_list,
            'parent_path': path_list[:-1] if path_list else None
        }

    def print_tree(self):
        sorted_items = sorted(self.nodes.items(),
                              key=lambda x: (len(x[1]['path']), x[1]['path']))

        for path_str, node in sorted_items:
            indent = "  " * len(node['path'])
            print(f"{indent}{node['name']}{node['path']}")


mp_tree = MaterializedPath()
mp_tree.add([], "Transport")
mp_tree.add([0], "Boat")
mp_tree.add([0, 0], "Yacht")
mp_tree.add([0, 1], "SailBoat")
mp_tree.add([1], "AirCraft")
mp_tree.add([1, 0], "Jet")
mp_tree.add([1, 1], "AirBus")
mp_tree.add([1, 2], "Helicopter")
mp_tree.add([2], "Car")
mp_tree.add([2, 0], "Sedan")
mp_tree.add([2, 1], "Truck")

print("\nИсходное Materialized Path дерево:")
mp_tree.print_tree()


def adjacency_to_materialized(adj_tree):
    mp = MaterializedPath()

    def build_path(node_id, current_path):
        node = adj_tree.nodes[node_id]
        new_path = current_path + [node['id']]

        mp.add(new_path, node['name'])

        for child_id in node['children']:
            build_path(child_id, new_path)

    for node in adj_tree.nodes.values():
        if node['parent_id'] is None:
            build_path(node['id'], [])

    return mp


mp_conv_tree = adjacency_to_materialized(al_tree)
print("\nКонвертированное Materialized Path дерево:")
mp_conv_tree.print_tree()


def materialized_to_adjacency(mat_tree):
    al = AdjacencyList()

    path_to_id = {}
    next_id = 1

    if "[]" in mat_tree.nodes:
        al.add(0, mat_tree.nodes["[]"]['name'])
        path_to_id["[]"] = 0

    sorted_items = sorted(mat_tree.nodes.items(),
                          key=lambda x: (len(x[1]['path']), x[1]['path']))

    for path_str, node in sorted_items:
        path = node['path']

        if path:
            parent_path = node['parent_path']
            parent_str = str(parent_path)

            if parent_str in path_to_id:
                parent_id = path_to_id[parent_str]

                node_id = next_id
                next_id += 1

                al.add(node_id, node['name'], parent_id)
                path_to_id[path_str] = node_id

    return al


al_conv_tree = materialized_to_adjacency(mp_tree)
print("\nКонвертированное Adjacency List дерево:")
al_conv_tree.print_tree()
