from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from dwapi import datawiz, datawiz_auth
import datetime
import pandas as pd
from dw_func import client_info, categories_sales, client_shops


# global DataWiz
dw = datawiz.DW()


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

        turnover = pd.DataFrame(dw.get_products_sale(by='turnover', date_from="2015-11-17",
                                        date_to="2015-11-18"))

        turn_over = []
        for turn_val in turnover.values:
            turn_over.append(turn_val.sum())

        #qty
        """qty = pd.DataFrame(dw.get_products_sale(by='qty', date_from="2015-11-17",
                                        date_to="2015-11-18"))

        qty_list = []
        for qty_val in qty.values:
            qty_list.append(qty_val.sum())"""

        receipts_qty = pd.DataFrame(dw.get_products_sale(by='receipts_qty', date_from="2015-11-17",
                                        date_to="2015-11-18"))

        receipt_qty_list = []
        for rc_qty_val in receipts_qty.values:
            receipt_qty_list.append(rc_qty_val.sum())


        average_qty = []
        for turn_val, rc_qty_val in turn_over, receipt_qty_list:
            average_qty.append(turn_val / rc_qty_val)


        context = {'user': username,
                   'password': password,
                   'dw_info': client_info(dw),
                   #'dw_sales': categories_sales(dw),
                   'dw_shops': client_shops(dw),
                   'product': average_qty,
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