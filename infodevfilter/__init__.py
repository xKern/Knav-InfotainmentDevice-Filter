from datetime import datetime, timedelta
from django.db.models import Q
from django.utils.timezone import now


def get_online_status(device_model):
    InfoDevice = device_model
    time_now = now()
    devices = InfoDevice.objects.all()
    filterd_dev = []
    for dev in devices:
        frq = dev.ping_frequency
        if dev.ping_time:
            if dev.ping_time >= time_now - timedelta(seconds=2 * frq):
                filterd_dev.append(dev.id)
    devices = InfoDevice.objects.filter(id__in=filterd_dev).all()
    return devices


def filtered_devices(device_model,
                     bus_model,
                     targets):
    InfoDevice = device_model
    Bus = bus_model

    mask = targets.get("mask")
    bus_ids = targets.get("buses", [])
    device_ids = targets.get("devices", [])
    if mask == -1:
        devices = []
        busdev_id = []
        if device_ids:
            devices = [dev.id for dev in device_ids]
        if bus_ids:
            busdev_id = [bus.info_device_id for bus in bus_ids]
        devs = InfoDevice.objects.filter(
            Q(id__in=devices) | Q(id__in=busdev_id)).all()
        return devs

    elif mask == 0:
        response = InfoDevice.objects.all()
        return response

    elif mask == 1:
        response = get_online_status(device_model=device_model)
        return response
    return []
