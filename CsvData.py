import pandas


class PandasData:
    @staticmethod
    def writeToCsv(leads, filename):
        df = pandas.DataFrame(leads)
        df.to_csv(f'./leads/{filename}.csv', index=False)


test = PandasData()
testdata = [
    {
        "a": 1,
        "b": 2,
        "c": 3
    },
    {
        "a": 4,
        "b": 5,
        "c": 6
    },
    {
        "a": 7,
        "b": 8,
        "c": 9
    },
]
test.writeToCsv(testdata, "test")
