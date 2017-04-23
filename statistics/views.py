from django.contrib import auth
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from dwapi import datawiz, datawiz_auth
import pandas as pd



@csrf_exempt
def login(request):
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
        except ValueError:
            return render_to_response("main.html", {'error': True})
    return render_to_response("main.html", {'error': True})


def stat(request):
    username = request.session['username']
    password = request.session['password']
    dw = datawiz.DW(username, password)
    dw_sales = dw.get_categories_sale(date_from="2015-10-11", date_to="2015-10-15")
    dw_info = dw.get_client_info()
    df = pd.DataFrame(dw_sales)
    df = df.to_html()
    return render_to_response("stat.html", {'user': request.session['username'],
                                            'password': request.session['password'],
                                            'dw_info': df})
