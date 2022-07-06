import psycopg2
from config.conf import Config
from datetime import timedelta, date


class Database:
    @property
    def connection(self):
        cfg = Config()
        return psycopg2.connect(
            database=cfg.dbase,
            user=cfg.user,
            password=cfg.password,
            host=cfg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_data(self, name: str):
        sql = '''
            SELECT restId, uuId, restLogin, 
                    restPassword, countryCode 
            FROM settings 
            WHERE restName=%s;
        '''
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self, group: str):
        sql = '''
            SELECT restName, restId , uuId
            FROM settings 
            WHERE restGroup=%s 
            ORDER BY restId;
        '''
        parameters = (group,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_line(self, dt: str, rest_name: str):
        sql = '''
            SELECT restName 
            FROM week 
            WHERE ordersDay=%s and restName=%s;
        '''
        parameters = dt, rest_name
        return self.execute(sql, parameters=parameters, fetchall=True)

    def update_week2_metrics(self, dt: date, rest_name: str, loss: float, scr: float, unc: float, prep: float,
                             rp: int, arp: float, st: int, ast: float):
        sql = '''
            UPDATE week 
            SET losses=%s, scrap=%s, unlosses=%s, cancel=%s,
                ratingProduct=%s, avgRatingProduct=%s, ratingStandard=%s, 
                avgRatingStandard=%s WHERE ordersDay=%s AND restName=%s
        '''
        parameters = (loss, scr, unc, prep, rp, arp, st, ast, dt, rest_name)
        self.execute(sql, parameters=parameters, commit=True)

    def add_week2_metrics(self, dt: date, rest_name: str, rest_id: int, loss: float, scr: float, unc: float, prep: float,
                          rp: int, arp: float, st: int, ast: float):
        sql = '''
            INSERT INTO week
                (ordersDay, restName, restId, losses, scrap, unlosses, cancel,
                 ratingProduct, avgRatingProduct, ratingStandard, avgRatingStandard)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        parameters = (dt, rest_name, rest_id, loss, scr, unc, prep, rp, arp, st, ast)
        self.execute(sql, parameters=parameters, commit=True)

