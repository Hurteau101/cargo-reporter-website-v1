from django.shortcuts import render

# Create your views here.
def report_importer(request):
    return render(request, 'report_importer.html')