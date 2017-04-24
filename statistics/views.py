from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from dwapi import datawiz, datawiz_auth
import datetime
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


        """df = dw.get_products_sale(products=[2833024, 2286946, 'sum'], by='turnover',
                              shops=[305, 306, 318, 321],
                              date_from = datetime.date(2015, 11, 17),
                              date_to = datetime.date(2015, 12, 17),
                              interval = datawiz.WEEKS)"""

        context = {'user': username,
                   'password': password,
                   'dw_info': client_info(dw),
                   'dw_sales': categories_sales(dw),
                   'dw_shops': client_shops(dw),
                   #'dw_shops': dw_porduct,
                  }

        return render_to_response("stat.html", context)
    except KeyError:
        return render_to_response("permission.html")
