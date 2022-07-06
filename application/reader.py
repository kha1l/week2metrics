import pandas as pd


class ReadFile:

    def __init__(self, name_rest: str, tps: str):
        self.name = name_rest
        self.tps = tps

    def open_file(self, order: str, rows: int):
        try:
            df = pd.read_excel(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', skiprows=rows)
        except ValueError:
            print(f'Неккоректный отчет в {self.name}:{order}')
            df = pd.DataFrame()
        return df


class Reader(ReadFile):
    df_losses = None
    df_st = None
    df_prod = None
    df_ass = None
    df_happy = None
    df_avg_prod = None

    def read_df(self):
        self.df_losses = self.open_file('losses', 4)
        self.df_st = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1824627247',
            on_bad_lines='skip', skiprows=2)
        self.df_prod = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1561264782',
            on_bad_lines='skip', skiprows=1)
        self.df_ass = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1374138695',
            on_bad_lines='skip', skiprows=1)
        self.df_happy = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1919028745',
            on_bad_lines='skip')
        self.df_avg_prod = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1561264782',
            on_bad_lines='skip', skiprows=2)
