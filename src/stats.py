import platform
from datetime import datetime
import distro
import psutil
import config

def get_stats():
    sys_name=platform.system()

    if sys_name == "Windows":
        os = f"Windows {platform.release()}"
    elif sys_name == "Linux":
        os = distro.name(pretty=True)
    elif sys_name == "Darwin":
        os = f"macOS {platform.mac_ver()[0]}"
    else:
        os = sys_name

    cpu_load = psutil.cpu_percent(interval=1)
    ram_load = psutil.virtual_memory().percent

    upload = round(psutil.net_io_counters().bytes_sent / (1024 * 1024), 2)
    download = round(psutil.net_io_counters().bytes_recv / (1024 * 1024), 2)
    
    battery_info = psutil.sensors_battery()
    battery = battery_info.percent if battery_info else "N/A"

    try:
        temps = psutil.sensors_temperatures()
        temperature = round(next(iter(temps.values()))[0].current, 1)
    except (AttributeError, KeyError, IndexError, StopIteration):
        temperature = "N/A"

    uptime_delta = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    uptime = str(uptime_delta).split(".")[0]

    return config.TEMPLATES['stats_report'].format(
            os=os,
            cpu_load=cpu_load,
            ram_load=ram_load,
            upload=upload,
            download=download,
            battery=battery,
            temperature=temperature,
            uptime=uptime
        )