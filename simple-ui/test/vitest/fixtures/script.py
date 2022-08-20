import rain as sr


def create_dataset(i, o, nums, p1, p2=True, p3='bb', p4=100):
    import pandas as pd

    def char_range(c1, c2):
        for c in range(ord(c1), ord(c2) + 1):
            yield chr(c)
    arr_number = [i for i in range(nums)]
    arr_letter = [c for c in char_range('A', 'Z')]
    index = pd.MultiIndex.from_product([arr_number, arr_letter], names=['nums', 'letters'])
    df = pd.DataFrame(index=index).reset_index()
    o['dataset'] = df

def dataset_length(i, o):
    df = i['dataset']
    o['length'] = len(df)

def sum(i, o):
    o['sum'] = i['num1'] + i['num2']

def check_equal(i, o):
    print(i['i1'] == i['i2'])


df = sr.DataFlow("dataflow1")


DatasetCreator1 = sr.CustomNode(
    node_id="DatasetCreator1",
    use_function=create_dataset,
    nums=100,
    p1="ciao",
)

TrainTestDatasetSplit1 = sr.TrainTestDatasetSplit(
    node_id="TrainTestDatasetSplit1",
    shuffle=False,
)

DataFrameLengthCalculator3 = sr.CustomNode(
    node_id="DataFrameLengthCalculator3",
    use_function=dataset_length,
)

DataFrameLengthCalculator1 = sr.CustomNode(
    node_id="DataFrameLengthCalculator1",
    use_function=dataset_length,
)

DataFrameLengthCalculator2 = sr.CustomNode(
    node_id="DataFrameLengthCalculator2",
    use_function=dataset_length,
)

SumOfNumbers1 = sr.CustomNode(
    node_id="SumOfNumbers1",
    use_function=sum,
)

EqualChecker1 = sr.CustomNode(
    node_id="EqualChecker1",
    use_function=check_equal,
)


df.add_edges([
    DatasetCreator1 @ 'dataset' > TrainTestDatasetSplit1 @ 'dataset',
    DatasetCreator1 @ 'dataset' > DataFrameLengthCalculator3 @ 'dataset',
    TrainTestDatasetSplit1 @ 'train_dataset' > DataFrameLengthCalculator1 @ 'dataset',
    TrainTestDatasetSplit1 @ 'test_dataset' > DataFrameLengthCalculator2 @ 'dataset',
    DataFrameLengthCalculator3 @ 'length' > EqualChecker1 @ 'i2',
    DataFrameLengthCalculator1 @ 'length' > SumOfNumbers1 @ 'num1',
    DataFrameLengthCalculator2 @ 'length' > SumOfNumbers1 @ 'num2',
    SumOfNumbers1 @ 'sum' > EqualChecker1 @ 'i1',
])

df.execute()