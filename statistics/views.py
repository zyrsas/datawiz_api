from django.contrib import auth
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from dwapi import datawiz, datawiz_auth



@csrf_exempt
def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            dw = datawiz.DW(username, password)
            dw_info = dw.get_client_info()
            request.session['username'] = username
            request.session['password'] = password
            request.session.save()
            return HttpResponseRedirect('/stat/')
        except ValueError:
            return render_to_response("main.html", {'error': True})
    return render_to_response("main.html", {'error': True})


def stat(request):
    return render_to_response("stat.html", {'user': request.session['username'],
                                            'password': request.session['password']})
