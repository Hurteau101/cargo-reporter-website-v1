from django.shortcuts import render, redirect
from .forms import UploaderForm
from .excel_utils import *
from .database_utils import *

def handle_file_upload(request, read_excel_function, save_function):
    file = UploaderForm(request.POST, request.FILES)
    file_name = request.FILES.get('file')
    if file.is_valid():
        read_file = request.FILES['file']
        valid_report, data = read_excel_function(read_file)
        if valid_report:
            save_function(data)
            return True, None

        else:
            return False, (f"{file_name} - Wrong Report. Please ensure this is either "
                             f"Waybills to Ship or Bot Report")
    else:
        "File extension “png” is not allowed. Allowed extensions are: xlsx."
        if "".join(file.errors['file'].as_data()[0]) == "The submitted file is empty.":
            return False, (f'{file_name} - File extension "{file_name.name.split(".")[-1]}" is not allowed. '
                             f'Allowed extensions are: xlsx."')
        else:
            return False, f"{file_name} - {''.join(([error for error in file.errors['file'].as_data()][0]))}"
