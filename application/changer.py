from application.reader import Reader
import pandas as pd


class Changer:

    def __init__(self, obj: Reader) -> None:
        self.obj = obj

    def change_losses(self):
        df = self.obj.df_losses

        try:
            df_l = df.loc[df['Unnamed: 0'] == 'Итого потери']
        except KeyError:
            df_l = pd.DataFrame()
        try:
            df_s = df.loc[df['Unnamed: 0'] == 'Брак']
        except KeyError:
            df_s = pd.DataFrame()
        try:
            df_un = df.loc[df['Unnamed: 0'] == 'Неучтённые потери']
        except KeyError:
            df_un = pd.DataFrame()
        try:
            df_p = df.loc[df['Unnamed: 0'] == 'Списания']
        except KeyError:
            df_p = pd.DataFrame()

        try:
            losses = round(df_l.iloc[0]['% от выручки'], 2)
        except IndexError:
            losses = 0

        try:
            scrap = round(df_s.iloc[0]['% от выручки'], 2)
        except IndexError:
            scrap = 0
        try:
            uncancel = round(df_un.iloc[0]['% от выручки'], 2)
        except IndexError:
            uncancel = 0
        try:
            prep = round(df_p.iloc[0]['% от выручки'], 2)
        except IndexError:
            prep = 0

        return losses, scrap, uncancel, prep

    def change_orders(self, name: str):
        df_st = self.obj.df_st
        df_prod = self.obj.df_prod
        df_avg_prod = self.obj.df_avg_prod

        pizza_st = df_st.loc[df_st['Store \n/ \nПиццерия'] == name]
        pizza_prod = df_prod.loc[df_prod['Store / Пиццерия'] == name]
        pizza_avg_prod = df_avg_prod.loc[df_prod['Store / Пиццерия'] == name]
        avg_res_st = pizza_st.iloc[0][
            'Average score of 6 checkups \n/ \nСредний рейтинг за последние \n6 результатов\n']
        avg_res_prod = pizza_avg_prod.iloc[0]['Average for 12 results / Среднее за 12 проверок']
        df_res_st = pizza_st.iloc[:, -1:].reset_index()
        df_res_prod = pizza_prod.iloc[:, -1:].reset_index()
        try:
            res_st = df_res_st.iat[0, 1]
        except IndexError:
            res_st = 0
        try:
            res_prod = df_res_prod.iat[0, 1]
        except IndexError:
            res_prod = 0
        try:
            res_prod = res_prod.replace(',', '.')
        except AttributeError:
            res_prod = 0
        try:
            avg_res_prod = avg_res_prod.replace(',', '.')
        except AttributeError:
            res_prod = 0
        try:
            res_st = res_st.replace(',', '.')
        except AttributeError:
            res_prod = 0
        try:
            avg_res_st = avg_res_st.replace(',', '.')
        except AttributeError:
            res_prod = 0
        try:
            return int(float(res_prod)), float(avg_res_prod), int(float(res_st)), float(avg_res_st)
        except ValueError:
            return 0, 0, 0, 0

