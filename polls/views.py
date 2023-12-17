from django.shortcuts import render


def index_page(request):
    context = {}
    context['authors'] = 'Anton and Stanislav'
    context['pages'] = 2
    return render(request, 'index.html', context)

def SeaBattle_page(request):
    context = {}
    return render(request, 'SeaBattle.html', context)

def mygift_page(request):
    context = {}
    return render(request, 'MyGifts.html', context)
