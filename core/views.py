from django.shortcuts import render
# Public Website Views
def index(request):
    return render(request, 'index.html')