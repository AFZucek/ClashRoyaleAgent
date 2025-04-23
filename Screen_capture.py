from PIL import ImageGrab
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import os
import subprocess


def focus_bluestacks():
    """
    Bring blue stacks emulator to the front
    """
    subprocess.run([
        "osascript", "-e", 'tell application "BlueStacks" to activate'
    ])

def find_bluestacks_window():
    """
    Find bounding box for bluestacks_window
    """
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    for window in window_list:
        owner_name = window.get('kCGWindowOwnerName', '')
        window_name = window.get('kCGWindowName', '')
        if 'BlueStacks' in owner_name or 'BlueStacks' in window_name:
            bounds = window['kCGWindowBounds']
            x = int(bounds['X'])
            y = int(bounds['Y'])
            w = int(bounds['Width'])
            h = int(bounds['Height'])
            return (x, y, x + w, y + h)
    return None


def main():
    """
    Main function, currently testing capture for one image
    """

    focus_bluestacks()

    bbox = find_bluestacks_window()

    test_file_path = os.path.join('data', 'TestCaptures', 'testscreen.png')

    if not bbox:
        raise Exception("BlueStacks window not found.")

    # Capture and savecle
    img = ImageGrab.grab(bbox)
    img.save(test_file_path)

if __name__ == "__main__":
    main()