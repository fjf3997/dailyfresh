from django.shortcuts import render

# Create your views here.


# index
def index(request):
    return render(request, 'index.html')

