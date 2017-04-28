#-coding:utf-8
import pandas as pd


date_from = "2015-11-17"
date_to = "2015-11-18"


def client_info(dw):
    dw_info = dw.get_client_info()
    dw_info = pd.DataFrame(dw_info)
    return dw_info.to_html()


def client_shops(dw):
    dw_shops = dw.get_shops()
    dw_shops = pd.DataFrame(dw_shops)
    return dw_shops.to_html()


def sale_stat(turnover, qty, receipts_qty):
    # average bill
    average_qty_list = []
    for i, j in zip(turnover.sum(axis=1).values, receipts_qty.sum(axis=1).values):
        average_qty_list.append(i / j)

    contex = pd.DataFrame(
                        data=[
                                turnover.sum(axis=1).values,
                                qty.sum(axis=1).values,
                                receipts_qty.sum(axis=1).values,
                                average_qty_list],
                        index=[
                                "Оборот",
                                "Кількість товарів",
                                "Кількість чеків",
                                "Середній чек"],
                        columns=[
                                "2015-11-17",
                                "2015-11-18"]
                        )
    contex['Різниця в %'] = (contex[date_from] - contex[date_to]) / contex[date_from] * 100
    contex['Різниця'] = contex[date_to] - contex[date_from] # average bill
    average_qty_list = []
    for i, j in zip(turnover.sum(axis=1).values, receipts_qty.sum(axis=1).values):
        average_qty_list.append(i / j)
    contex = pd.DataFrame(
                        data=[
                                turnover.sum(axis=1).values,
                                qty.sum(axis=1).values,
                                receipts_qty.sum(axis=1).values,
                                average_qty_list],
                        index=[
                                "Оборот",
                                "Кількість товарів",
                                "Кількість чеків",
                                "Середній чек"],
                        columns=[
                                "2015-11-17",
                                "2015-11-18"]
                        )
    contex['Різниця в %'] = (contex[date_from] - contex[date_to]) / contex[date_from] * 100
    contex['Різниця'] = contex[date_to] - contex[date_from]

    return contex.to_html()


def grow_sales(dw, turnover, qty):
    diferent = pd.Series(turnover.loc[date_to] - turnover.loc[date_from])
    diferent_qty = pd.Series(qty.loc[date_to] - qty.loc[date_from])

    positiv = diferent[(diferent > 10)].tolist()
    positiv_qty = diferent_qty[(diferent > 10)].tolist()

    index = pd.Series(diferent[(diferent > 10)].index).values

    new_index = dw.id2name(list(index), typ="product")
    name_product = pd.DataFrame({"product_name": new_index}).reset_index()


    tmp = pd.DataFrame(name_product['product_name'])
    tmp['Different'] = positiv
    tmp['Different_qty'] = positiv_qty

    tmp = tmp.sort_values(by=['Different', 'Different_qty'], axis=0, ascending=[False, False])

    return tmp.to_html()


def decrease_sale(dw, turnover, qty):
    diferent = pd.Series(turnover.loc[date_to] - turnover.loc[date_from])
    diferent_qty = pd.Series(qty.loc[date_to] - qty.loc[date_from])

    negative = diferent[(diferent < -35)].tolist()
    negative_qty = diferent_qty[(diferent < -35)].tolist()

    index = pd.Series(diferent[(diferent < -35)].index).values

    new_index = dw.id2name(list(index), typ="product")
    name_product = pd.DataFrame({"product_name": new_index}).reset_index()


    tmp = pd.DataFrame(name_product['product_name'])
    tmp['Different'] = negative
    tmp['Different_qty'] = negative_qty

    tmp = tmp.sort_values(by=['Different', 'Different_qty'], axis=0, ascending=[True, True])

    return tmp.to_html()

