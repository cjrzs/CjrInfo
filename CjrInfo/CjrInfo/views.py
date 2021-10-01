from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


def test_view(request):
    return HttpResponse('于宏成大傻逼，没有小GG')
