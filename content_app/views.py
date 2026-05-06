from django.shortcuts import render

def contentAdmin(request):
    return render(request, 'contentAdmin.html')
def CRMAdmin(request):
    return render(request, 'CRMAdmin.html')

# Create your views here.
