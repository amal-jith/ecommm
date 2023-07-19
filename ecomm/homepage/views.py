from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'homepage/home.html')

def about(request):
    return render(request, 'homepage/about.html')