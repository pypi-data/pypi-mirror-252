import numpy as np
import Xlib
import Xlib.display
from Xlib import X

class WindowCaptureSync:
    windowId = None

    def __init__(self, window_name):
        self.change_window(window_name)

    def change_window(self, window_name):
        display = Xlib.display.Display()
        try:
            root = display.screen().root
            windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

            for windowID in windowIDs:
                window = display.create_resource_object('window', windowID)
                window_title_property = window.get_full_property(display.intern_atom('_NET_WM_NAME'), 0)

                if window_title_property and window_name.lower() in window_title_property.value.decode('utf-8').lower():
                    self.windowId = windowID

            if not self.windowId:
                raise Exception('Window not found: {}'.format(window_name))
        finally:
            display.close()

    def get_screenshot(self):
        display = Xlib.display.Display()
        window = display.create_resource_object('window', self.windowId)
        
        geometry = window.get_geometry()
        width, height = geometry.width, geometry.height

        pixmap = window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
        data = pixmap.data
        image = np.frombuffer(data, dtype='uint8').reshape((height, width, 4))
        display.close()
        return image