from datetime import datetime, timedelta


def get_online_status(device_model):
    InfoDevice = device_model
    now = datetime.now()
    devices = InfoDevice.objects.all()
    filterd_dev = []
    for dev in devices:
        if dev.ping_time:
            last_ping = dev.ping_time.strftime("%Y-%m-%d %H:%M:%S")
            last_ping = datetime.strptime(last_ping, "%Y-%m-%d %H:%M:%S")
            if last_ping >= now - timedelta(seconds=2 * dev.ping_frequency):
                filterd_dev.append(dev)
    return filterd_dev


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
        if device_ids:
            devices = list(device_ids)
        if bus_ids:
            bus_identifiers = [bus_id.id for bus_id in bus_ids]
            bus_devices = Bus.objects.filter(id__in=bus_identifiers)
            bus_devices = bus_devices.filter(info_device__isnull=False)
            bus_devices = list(
                bus_devices.values_list("info_device_id", flat=True)
                )
            bus_devices = list(
                InfoDevice.objects.filter(id__in=bus_devices).all()
                )
            devices.extend(bus_devices)
        return devices

    elif mask == 0:
        response = InfoDevice.objects.all()
        return response

    elif mask == 1:
        response = get_online_status()
        return response
