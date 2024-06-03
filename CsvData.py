import pandas as pd


class PandasData:
    @classmethod
    def writeToCsv(cls, leads, filename):
        df = pd.DataFrame(leads)
        df = cls.transformData(df)
        df.to_csv(f'./leads/{filename}.csv', index=False)

    @classmethod
    def readFromCsv(cls, filename):
        df = pd.read_csv(filename)
        df = cls.transformEmail(df)
        df = cls.transformAddress(df)
        return df

    @staticmethod
    def transformEmail(df):
        if 'email' in df.columns:
            df['email'] = df['email'].str.split(':').str[1]
        return df

    @staticmethod
    def transformAddress(df):
        if 'address' in df.columns:
            df['address'] = df['address'].str.replace('\n', ' ', regex=False)
        return df

    @staticmethod
    def transformData(df):
        # Example: Add any general transformations here
        df = PandasData.transformEmail(df)
        df = PandasData.transformAddress(df)
        return df
