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

def split(index, value, dataset):
    right, left = [], []
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

def get_split(dataset):
    class_values = [row[-1] for row in dataset]
    b_index, b_value, b_score, b_group = 999,999,999, None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = split(index, row[index], dataset)
            gini = gini_index(class_values, groups)
            if gini < b_score:
                b_index, b_value, b_score, b_group = index, row[index], gini,
                groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups}

if __name__ == '__main__':
    print 'Testing Gini Index'
    #Test 1: 50/50 split
    test_data = [[[1,0], [1,1]], [[0,0], [0,1]]]
    print 'Test1 passed' if gini_index([1,0], test_data) == 1.0 else 'Test 1 failed'
    #Test 2: Perfect split
    test_data = [[[1,0], [0,0]], [[1,1],[0,1]]]
    print 'Test2 passed' if gini_index([1,0], test_data) == 0.0 else 'Test 2 failed'
