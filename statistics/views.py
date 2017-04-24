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

        turnover = pd.DataFrame(dw.get_products_sale(shops=int(595), by='turnover', date_from="2015-11-17",
                                        date_to="2015-11-18", view_type="represent"))

        context = {'user': username,
                   'password': password,
                   'dw_info': client_info(dw),
                   'dw_sales': categories_sales(dw),
                   'dw_shops': client_shops(dw),
                   'product': turnover.to_html(),
                   'id2name': dw.id2name([2837457, 2837488])
                  }
        return render_to_response("stat.html", context)
    except KeyError:
        return render_to_response("permission.html")
