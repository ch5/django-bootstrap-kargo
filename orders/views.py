from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect
from orders.forms import ODOrderForm
from orders.models import ODOrder

########################################################################
#                   My view code and on task                           #
########################################################################
from orders.models import Vehicle
from orders.forms import VehicleCreateForm
from django.shortcuts import get_object_or_404
from PIL import Image
from django.conf import settings


# Function Showing list of order in costumers home page
def vehicle_list(request):
    # query on all vehicle_list records
    vehicle_list = Vehicle.objects.all()

    # structured vehicle_list into simple dict,
    context = {
        'vehicle_list':vehicle_list,
    }
    return render(request, 'vehicle/vehicle_list.html', context)

# Function for Handle new customer, contain (name, driver, number, vehicle)
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.number = vehicle.number.upper()
            vehicle.save()
            # Pillow documentation (https://pillow.readthedocs.io/en/3.3.x/)
            # Request photo from models
            request.FILES.get('photo')
            thumbnail = 90, 120
            # file path to media /media/year/month/day(vehicle.photo)
            photo_media = settings.MEDIA_ROOT+"/"+vehicle.photo.name
            img = Image.open(photo_media)
            # create thumbnails with thumbnail size (90, 120)
            img.thumbnail(thumbnail)
            # saving image
            img.save(photo_media)
            messages.success(request, 'Adding data Customer')
            return redirect(reverse('order:vehicle_list'))
    else:
        form = VehicleCreateForm()

    context = {
        'form':form
    }
    return render(request, 'vehicle/vehicle_create.html', context)

# Handle edit data vehicle from menu customers
def vehicle_edit(request, number):
    vehicle = get_object_or_404(Vehicle, number=number)
    # if request POST edit vehicle
    if request.method == 'POST':
        form = VehicleCreateForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.number = vehicle.number.upper()
            vehicle.save()
            messages.success(request, 'Vehicle already updated')
            return redirect(reverse('order:vehicle_list'))
    else:
        # if request GET or something open form without edit
        form = VehicleCreateForm(instance=vehicle)

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'vehicle/vehicle_edit.html', context)

# Function for delete table on table orders_vehicle
def vehicle_delete(request, number):
    vehicle = get_object_or_404(Vehicle, number=number)
    if request.method == 'POST':
        # delete table vehicle from database
        vehicle.delete()
        messages.success(request, 'This has been deleted')
        return redirect(reverse('order:vehicle_list'))

    context = {
        'vehicle': vehicle
    }
    return render(request, 'vehicle/vehicle_delete.html', context)

########################################################################
#                         End Task                                     #
########################################################################
def index(request):
    """
    Handle index page for order
    """

    return render(request, 'order/index.html')


def management(request):
    """
    Showing list of order in management home page
    """

    # query on all order records
    orders = ODOrder.objects.all()

    # structured order into simple dict,
    # later on, in template, we can render it easily, ex: {{ orders }}
    data = {'orders': orders}

    return render(request, 'order/management.html', data)


def create_order(request):
    """
    Handle new order creation
    """

    # Initial form and data
    data = {
        'form': ODOrderForm(),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = ODOrderForm(request.POST)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        if form.is_valid():

            # wrap form result into dict ODOrder model fields structure
            order_data = {
                'name': form.cleaned_data.get('name'),
                'phone': form.cleaned_data.get('phone'),
                'price': form.cleaned_data.get('price'),
            }

            try:
                ODOrder.objects.create(**order_data)
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "A new record has been created!")

    return render(request, 'order/create_order.html', data)


def edit_order(request, uuid=None):
    """
    How to remove order
    """
    if not uuid:
        return redirect(reverse('order:management'))

    # validate given UUID match with record in database
    try:
        order = ODOrder.objects.get(uuid=uuid)
    except ODOrder.DoesNotExist:
        messages.error(request, "Record not found!")
        return redirect(reverse('order:management'))

    data = {
        'form': ODOrderForm(instance=order),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = ODOrderForm(request.POST, instance=order)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        if form.is_valid():

            try:
                form.save()
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "Record has been updated!")

    return render(request, 'order/edit_order.html', data)


def delete_order(request, uuid=None):
    """
    How to remove order
    """
    if uuid:

        # finding given UUID to match order in database
        try:
            order = ODOrder.objects.get(uuid=uuid)
        except ODOrder.DoesNotExist:
            messages.error(request, "Order not found")
        else:
            # delete order from database
            order.delete()
            messages.success(request, 'Order "{}" has been deleted'.format(order.name))

    return redirect(reverse('order:management'))
