import pandas as pd
import requests


def get_ym_warehouses(ym_api_token: str):
    """
    Возвращает список складов Маркета (FBY) с их идентификаторами.
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/warehouses/getFulfillmentWarehouses

    :param ym_api_token:
    :return:
    """
    url = 'https://api.partner.market.yandex.ru/warehouses?'
    headers = headers = {'Accept': 'application/json', 'Authorization': f'Bearer {ym_api_token}'}
    response = requests.get(url=url, headers=headers, params={})
    # display(f'{response = }')
    lst = response.json()['result']['warehouses']
    df = pd.DataFrame.from_dict(lst)
    return df
