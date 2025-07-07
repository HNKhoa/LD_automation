import subprocess
import cv2
import numpy as np
import time

def capture_screen(device_name: str, save_path: str = "screen.png") -> bool:
    result = subprocess.run(
        ["adb", "-s", device_name, "exec-out", "screencap", "-p"],
        capture_output=True
    )
    if result.returncode == 0:
        with open(save_path, "wb") as f:
            f.write(result.stdout)
        return True
    return False

def click_device(device_name: str, x: int, y: int):
    subprocess.run(["adb", "-s", device_name, "shell", "input", "tap", str(x), str(y)])

def detect_image_on_screen(
    device_name: str,
    template_path: str,
    threshold: float = 0.85,
    retry: int = 1,
    click: bool = True,
    screenshot_path: str = "screen.png"
):
    for attempt in range(retry):
        if not capture_screen(device_name, screenshot_path):
            print(f"[{device_name}] ❌ Lỗi chụp màn hình.")
            return False

        screen = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)

        if screen is None or template is None:
            print(f"[{device_name}] ❌ Không đọc được ảnh.")
            return False

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"[{device_name}] 🔍 Lần {attempt+1}/{retry} - Độ khớp: {max_val:.3f}")
        if max_val >= threshold:
            h, w = template.shape[:2]
            x = max_loc[0] + w // 2
            y = max_loc[1] + h // 2
            if click:
                click_device(device_name, x, y)
                print(f"[{device_name}] ✅ Click tại ({x}, {y})")
            else:
                print(f"[{device_name}] 🎯 Tìm thấy tại ({x}, {y}) (không click)")
            return (x, y)

        time.sleep(1)  # Chờ 1 giây trước khi thử lại

    print(f"[{device_name}] ❌ Không tìm thấy hình sau {retry} lần.")
    return False
def click_at(device_name: str, x: int, y: int, hold=False):
    """
    Click vào tọa độ (x, y) trên thiết bị ADB.

    Args:
        device_name (str): Tên thiết bị ADB, ví dụ 'emulator-5554'
        x (int): Tọa độ X
        y (int): Tọa độ Y
        hold (bool|float): 
            - False hoặc 0 → chỉ click nhanh
            - float (số giây) → giữ tại tọa độ đó
    """
    if not hold:
        # Click nhanh
        subprocess.run(["adb", "-s", device_name, "shell", "input", "tap", str(x), str(y)])
        print(f"[{device_name}] ✅ Click tại ({x}, {y})")
    else:
        # Click & giữ (giả lập bằng swipe cùng điểm)
        hold_time = float(hold)
        ms = int(hold_time * 1000)
        subprocess.run([
            "adb", "-s", device_name, "shell", "input", "swipe",
            str(x), str(y), str(x), str(y), str(ms)
        ])
        print(f"[{device_name}] ✅ Click & giữ tại ({x}, {y}) trong {hold_time:.2f} giây")


def swipe_from_to(device_name: str, x: int, y: int, x1: int, y1: int, duration: float = 0.5):
    """
    Vuốt từ (x, y) đến (x1, y1) trên thiết bị ADB.

    Args:
        device_name (str): Tên thiết bị ADB, ví dụ 'emulator-5554'
        x, y (int): Tọa độ điểm bắt đầu
        x1, y1 (int): Tọa độ điểm kết thúc
        duration (float): Thời gian vuốt (giây). Mặc định = 0.5s
    """
    ms = int(duration * 1000)
    subprocess.run([
        "adb", "-s", device_name, "shell", "input", "swipe",
        str(x), str(y), str(x1), str(y1), str(ms)
    ])
    print(f"[{device_name}] ✅ Vuốt từ ({x}, {y}) đến ({x1}, {y1}) trong {duration:.2f} giây")










if __name__ == "__main__":
    device = "emulator-5554"

    # # Chạy và lấy kết quả
    # coords = detect_image_on_screen(
    #     device_name=device,
    #     template_path="img/gio_hang_ok.png",
    #     threshold=0.95,
    #     retry=5,
    #     click=True  # ❌ Không click, chỉ tìm
    # )

    # if coords:
    #     print("🎯 Toạ độ:", coords)
    # else:
    #     print("❌ Không tìm thấy.")



# click_at(device, 500, 1207, hold=False)


# click_at(device, 368, 1082, hold=False)

swipe_from_to(device, 375, 1112, 356, 826, duration=0.9)