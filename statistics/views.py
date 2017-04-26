#-coding:utf-8
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from dwapi import datawiz, datawiz_auth
import datetime
import pandas as pd
from dw_func import client_info, categories_sales, client_shops
import ast


# global DataWiz
dw = datawiz.DW()
# date
date_from = "2015-11-17"
date_to = "2015-11-18"


@csrf_exempt
def login(request):
    error = False
    global dw
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            dw = datawiz.DW(username, password)
            request.session['username'] = username
            request.session['password'] = password
            request.session.set_expiry(0)
            request.session.save()
            return HttpResponseRedirect('/stat/')
        except:
            error = True
            return render_to_response("main.html", {'error': error})
    return render_to_response("main.html", {'error': error})


@csrf_exempt
def stat(request):
    global dw
    if request.method == "POST":
        try:
            del request.session['username']
            del request.session['password']
        except KeyError:
            pass
        return HttpResponseRedirect("/")
    try:
        username = request.session['username']
        password = request.session['password']
        context = {
                   'user': username,
                   'password': password,
                   'dw_info': client_info(dw),
                   'dw_shops': client_shops(dw),
                  }
        return render_to_response("stat.html", context)
    except KeyError:
        return render_to_response("permission.html")


@csrf_exempt
def get_product(request):
    if request.POST:
        index = request.POST['id_products']
        prd = dw.get_product(products=int(index))
        prd = pd.DataFrame(prd, index=[0])
    return render_to_response("get_product.html", {'products': prd.to_html()})


def sale_stat(request):
    turnover = pd.DataFrame(dw.get_products_sale(
                                                by='turnover',
                                                date_from=date_from,
                                                date_to=date_to
                                                ))
    qty = pd.DataFrame(dw.get_products_sale(
                                            by='qty',
                                            date_from=date_from,
                                            date_to=date_to
                                            ))
    receipts_qty = pd.DataFrame(dw.get_products_sale(
                                                    by='receipts_qty',
                                                    date_from=date_from,
                                                    date_to=date_to
                                                    ))
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
    contex['Різниця'] = contex[date_to] - contex[date_from]

    return render_to_response("sale_stat.html", {"sale_stat": contex.to_html()})


def grow_sales(request):
    turnover = pd.DataFrame(dw.get_products_sale(
                                                by='turnover',
                                                date_from=date_from,
                                                date_to=date_to,
                                                view_type="represent"
                                                ))

    diferent = pd.Series(turnover.loc[date_to] - turnover.loc[date_from])

    positiv = diferent[(diferent > 0)].tolist()

    index = pd.Series(diferent[(diferent > 0)].index).values

    new_index = []
    for i in list(index):
        new_index.append(dw.get_product(products=int(i)))

    name_product = pd.DataFrame(new_index)
    #name_product = name_product['product_name'].str.encode("utf-8")

    tmp = pd.DataFrame(name_product['product_name'])
    tmp['Different'] = positiv

    tmp = tmp.sort_values(by=['Different'], axis=0, ascending=False)

    """ diff = pd.DataFrame(data=[
                            positiv
                             ],
                        index=[
                            "Зміна обороту"
                        ],
                        columns=name_product)

    diff = diff.head().sort(name_product, axis=0, ascending=False)"""

    return render_to_response("grow_sales.html", {'turnover': turnover.to_html(),
                                                  'different': tmp.to_html()})
