from django.shortcuts import render, redirect
from .forms import RemarkForm
from .common_data import *
from .file_utils import *
from .models import AWB

def report_importer(request):
    form = UploaderForm()
    error_message = None

    if request.method == 'POST':
        if "sla_top_20" in request.POST:
            success, error_message = handle_file_upload(request ,read_excel_function=extract_waybills_to_ship_file,
                                                        save_function=sla_top_20_save)
            if success:
                return redirect("top-20")
        elif 'priority' in request.POST:
            success, error_message = handle_file_upload(request ,read_excel_function=extract_waybills_to_ship_file,
                                                        save_function=priority_save)
            if success:
                return redirect("priority-report")

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

    return render(request, 'top_20/top_20.html', context)


def sla(request):
    context = {
        "past_sla_data": get_past_sla_data(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "total_weight": get_total_weight(DESTINATION_FILTER_LIST, station="WPG", hours=0),
    }

    return render(request, 'sla/sla_report.html', context)


def destination_breakdown(request, destination):
    breakdown = AWB.objects.filter(sla_report=True, destination__in=DESTINATION_FILTER_LIST,
                                   destination=destination, hours_remaining__lt=0).values()

    context = {
        "past_sla_data": get_past_sla_data(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "total_weight": get_total_weight(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "breakdown": breakdown,
        "destination": destination,
    }

    return render(request, 'sla/sla_report.html', context)

def combined_report(request):
    order_filter = AWB.objects.filter(sla_report=True, destination__in=DESTINATION_FILTER_LIST).order_by(
        "-days").values()[:20]

    context = {
        "past_sla_data": get_past_sla_data(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        "total_weight": get_total_weight(DESTINATION_FILTER_LIST, station="WPG", hours=0),
        'order_filter': order_filter,
    }

    return render(request, 'combined_report.html', context)


def priority_report(request):

    context = {

    }

    return render(request, "priority_report.html", context)