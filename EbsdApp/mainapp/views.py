from django.shortcuts import render

def start_page(request):
    return render(request, 'mainapp\start_page.html')
