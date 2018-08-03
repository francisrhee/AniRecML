# Converts 2D array (data) with given categories into one-hot encoding of the data
def encodeOneHot(categories, data):
    dataOneHot = []
    for row in range(len(data)):
        table = dict((c, 0) for c in categories)
        for value in data[row]:
            try:
                table[value] = 1
            except:
                print("Value: " + value + " is not included in categories list")
        dataOneHot.append(list(table.values()))
    return dataOneHot

