from django.shortcuts import render
from .forms import UploaderForm
from .excel_utils import *
from .database_utils import *

# Create your views here.
def report_importer(request):
    form = UploaderForm()
    error_message = None

    if request.method == "POST":
        if "sla_top_20" in request.POST:
            file = UploaderForm(request.POST, request.FILES)
            file_name = request.FILES.get('file')
            if file.is_valid():
                read_file = request.FILES['file']
                valid_report, data = extract_waybills_to_ship_file(read_file)
                if valid_report:
                    sla_top_20_save(data)
                else:
                    error_message = (f"{file_name} - Wrong Report. Please ensure this is either "
                                     f"Waybills to Ship or Bot Report")



            else:
                "File extension “png” is not allowed. Allowed extensions are: xlsx."
                if "".join(file.errors['file'].as_data()[0]) == "The submitted file is empty.":
                    error_message = (f'{file_name} - File extension "{file_name.name.split(".")[-1]}" is not allowed. '
                                     f'Allowed extensions are: xlsx."')
                else:
                    error_message = f"{file_name} - {''.join(([error for error in file.errors['file'].as_data()][0]))}"
    else:
        form = UploaderForm()

    context = {"form": form, "error_message": error_message}

    return render(request, 'report_importer.html', context)