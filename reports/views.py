from django.shortcuts import render, redirect
from .forms import UploaderForm, RemarkForm
from .excel_utils import *
from .database_utils import *
from .common_data import *
from .models import AWB


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
                    return redirect('top-20')
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


def top_20(request):
    remark_form = RemarkForm()

    calculations = {
        "total_going": AWB.objects.filter(sla_report=True, remarks__icontains="jv").count(),
        "on_hold": AWB.objects.filter(sla_report=True, remarks__icontains="hold").count(),
        "to_clear": AWB.objects.filter(sla_report=True, remarks__icontains="clear").count(),
    }

    order_filter = AWB.objects.filter(sla_report=True, destination__in=DESTINATION_FILTER_LIST).order_by(
        "-days").values()[:20]

    if request.method == "POST":
        if "edit" in request.POST:
            awb = request.POST.get('edit')
            get_awb = AWB.objects.get(awb_number=awb)
            remark_form = RemarkForm(instance=get_awb)
        elif "save" in request.POST:
            awb = request.POST.get('save')
            get_awb = AWB.objects.get(awb_number=awb)
            form = RemarkForm(request.POST, instance=get_awb)
            if form.is_valid():
                form.save()
                return redirect('top-20')

    context = {
        "remark_form": remark_form,
        "calculations": calculations,
        "order_filter": order_filter,
    }

    return render(request, 'top_20.html', context)


def sla(request):
    context = {
        "past_sla_data": get_past_sla_data(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "total_weight": get_total_weight(DESTINATION_FILTER_LIST, station="WPG", hours=0),
    }

    return render(request, 'sla_report.html', context)


def destination_breakdown(request, destination):
    breakdown = AWB.objects.filter(sla_report=True, destination__in=DESTINATION_FILTER_LIST,
                                   destination=destination, hours_remaining__lt=0).values()

    context = {
        "past_sla_data": get_past_sla_data(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "total_weight": get_total_weight(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "breakdown": breakdown,
    }

    return render(request, 'sla_report.html', context)
