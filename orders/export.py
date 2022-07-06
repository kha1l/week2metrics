import requests
import fake_useragent
from datetime import date, timedelta
from postgres.psql import Database
from bs4 import BeautifulSoup


class DataExportDay:

    def __init__(self, date_end: date, name: str, tps: str):
        db = Database()
        data = db.get_data(name)
        self.name = name
        self.rest = data[0]
        self.uuid = data[1]
        self.date_end = date_end
        self.login = data[2]
        self.password = data[3]
        self.code = data[4]
        self.session = None
        self.user = None
        self.header = None
        self.tps = tps
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        log_data = {
            'CountryCode': self.code,
            'login': self.login,
            'password': self.password
        }
        self.header = {
            'user-agent': self.user
        }
        log_link = f'https://auth.dodopizza.{self.code}/Authenticate/LogOn'
        self.session.post(log_link, data=log_data, headers=self.header)

    def save(self, orders_data):
        for order in orders_data:
            response = self.session.post(orders_data[order]['link'], data=orders_data[order]['data'],
                                         headers=self.header)
            with open(f'./orders/export/{order}_{self.name}_{self.tps}.xlsx', 'wb') as file:
                file.write(response.content)
                file.close()

    def get_revision(self, dt):
        data_link = f'https://officemanager.dodopizza.ru/InventoryManager/LossesAndExcees/SelectNearestRevisions' \
                    f'?unitId={self.rest}&date={dt}'
        response_revision = self.session.get(data_link, headers=self.header)
        soup = BeautifulSoup(response_revision.text, 'html.parser')
        decoded = soup.decode()
        decoded = decoded.replace('</option>\\r\\n"}', '')
        decoded = decoded.replace('\\"\'>', ' ')
        decoded = decoded.replace('</option>\\r\\n        <', '')
        dec_list = decoded.split('option value=\'\\"')
        dec_list.pop(0)
        result_list = list()
        for i in dec_list:
            if '(День)' not in i:
                result_list.append(i)
            else:
                continue
        return result_list

    def losses(self):
        cf = list()
        cl = list()
        dt = self.date_end
        result_second = self.get_revision(dt)
        while len(cl) < 1:
            if len(result_second) != 0:
                cl.append(result_second[0])
            else:
                dt = dt - timedelta(days=1)
                result_second = self.get_revision(dt)

        dts = dt - timedelta(days=7)
        result_first = self.get_revision(dts)
        while len(cf) < 1:
            if len(result_first) == 2:
                cf.append(result_first[1])
            elif len(result_first) == 1 and result_first[0] != result_second[0]:
                cf.append(result_first[0])
            else:
                dts = dts - timedelta(days=1)
                result_first = self.get_revision(dts)

        rev_first = str((cf[0].split(' '))[0])
        rev_second = str((cl[0].split(' '))[0])
        orders_data = {
            'losses': {
                'link': f'https://officemanager.dodopizza.{self.code}/InventoryManager/LossesAndExcees/Export',
                'data': {
                    "UnitId": self.rest,
                    "SelectedMaterialCategories": [
                        "1",
                        "2",
                        "3",
                        "5"
                    ],
                    "DefaultBeginDateString": dts,
                    "DefaultEndDateString": dt,
                    "firstRevisionId": rev_first,
                    "secondRevisionId": rev_second,
                    "IsVatIncluded": [
                        "true"
                    ],
                    "sortByMaterial": "0",
                    "sortByLossesInMoney": "0",
                    "sortByTotalLossesInMoney": "1",
                    "connectionId": "57f4be7c-8e21-4b46-9096-d54896beb930",
                    "reload": "true"
                }
            }
        }
        self.save(orders_data)
