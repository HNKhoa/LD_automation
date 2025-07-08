# run_multi_ld.py
import subprocess
from concurrent.futures import ThreadPoolExecutor
from main import run_for_device


def get_connected_devices():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = []
    for line in result.stdout.strip().split('\n')[1:]:
        if 'device' in line:
            serial = line.split('\t')[0]
            devices.append(serial)
    return devices


def run_all():
    devices = get_connected_devices()
    print(f"🔍 Phát hiện {len(devices)} thiết bị: {devices}")

    if not devices:
        print("❌ Không tìm thấy thiết bị LDPlayer nào.")
        return

    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        executor.map(run_for_device, devices)


if __name__ == "__main__":
    run_all()
