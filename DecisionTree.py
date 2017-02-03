# This function will return the Gini index for the split and classes provided
def gini_index(classes, groups):
    gini = 0.0
    for class_value in classes:
        for group in groups:
            size = len(group)
            if size == 0:
                continue
            proportion = [row[-1] for row in group].count(class_value) / float(size)
            gini += proportion * (1.0 - proportion)
    return gini

def create_split(index, value, dataset):
    right, left = [], []
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# This function return the class with highest frequency for the given group
def terminal_node(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key = outcomes.count)

def get_split(dataset):
    class_values = [row[-1] for row in dataset]
    b_index, b_value, b_score, b_group = 999,999,999, None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = create_split(index, row[index], dataset)
            gini = gini_index(class_values, groups)
            if gini < b_score:
                b_index, b_value, b_score, b_group = index, row[index], gini, groups
    return {'index':b_index, 'value':b_value, 'groups':b_group}

# This is a pre prune model 
def split(node, max_depth, min_nodes, depth):
    left, right = node['groups']
    del node['groups']
    print 'split called'
    if not left or not right:
        node['left'] = node ['right'] = terminal_node(left + right)
        return node 
    if depth >= max_depth:
        node['left'] = terminal_node(left)
        node['right'] = terminal_node(right)
    else:
        if len(left) <= min_nodes:
            node['left'] = terminal_node(left)
        else:
            node['left'] = get_split(left)
            node['left'] = split(node['left'], max_depth, min_nodes, depth+1)

        if len(right) <= min_nodes:
            node['right'] = get_split(right)
            node['right'] = split(node['right'], max_depth, min_nodes, depth+1)
    return node
def build_tree(dataset, max_depth, min_nodes):
    root = get_split(dataset)
    root = split(root, max_depth, min_nodes, 1)
    return root

def predict(row, node):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            predict(row, node['left'])
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            predict(row, node['right'])
        else:
            return node['right']

if __name__ == '__main__':
    print 'Testing Gini Index'
    #Test 1: 50/50 split
    test_data = [[[1,0], [1,1]], [[0,0], [0,1]]]
    print 'Test1 passed' if gini_index([1,0], test_data) == 1.0 else 'Test 1 failed'
    #Test 2: Perfect split
    test_data = [[[1,0], [0,0]], [[1,1],[0,1]]]
    print 'Test2 passed' if gini_index([1,0], test_data) == 0.0 else 'Test 2 failed'
    dataset = [[2.771244718,1.784783929,0],
            [1.728571309,1.169761413,0],
            [3.678319846,2.81281357,0],
            [3.961043357,2.61995032,0],
            [2.999208922,2.209014212,0],
            [7.497545867,3.162953546,1],
            [9.00220326,3.339047188,1],
            [7.444542326,0.476683375,1],
            [10.12493903,3.234550982,1],
            [6.642287351,3.319983761,1]]
    tree = build_tree(dataset, 1, 1)
    for row in dataset:
            prediction = predict(row, tree)
            print('Expected=%d, Got=%d' % (row[-1], prediction))
