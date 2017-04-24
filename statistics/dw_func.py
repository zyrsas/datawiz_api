import pandas as pd
import datetime


date_from = "2015-11-17"
date_to = "2015-11-18"


def client_info(dw):
    dw_info = dw.get_client_info()
    dw_info = pd.DataFrame(dw_info)
    return dw_info.to_html()


def categories_sales(dw):
    dw_sales = dw.get_categories_sale(categories=['sum'], shops=int(601), by='turnover')
    dw_sales = pd.DataFrame(dw_sales)
    return dw_sales.to_html()


def client_shops(dw):
    dw_shops = dw.get_shops()
    dw_shops = pd.DataFrame(dw_shops)
    return dw_shops.to_html()

