import ctypes
from queue import Queue
from threading import Thread
from time import sleep

from .constants import HEX_DIRECT_KEYS, HEX_KEY_TYPES, HEX_MOUSE_KEYS, HEX_VIRTUAL_KEYS


class Keys:
    common = None
    standalone = False

    # instance of worker class
    keys_worker = None
    keys_process = None

    # key constants
    direct_keys = HEX_KEY_TYPES["direct_keys"]
    virtual_keys = HEX_KEY_TYPES["virtual_keys"]
    key_press = HEX_KEY_TYPES["key_press"]
    key_release = HEX_KEY_TYPES["key_release"]

    # mouse constants
    mouse_move = HEX_MOUSE_KEYS["mouse_move"]
    mouse_lb_press = HEX_MOUSE_KEYS["mouse_lb_press"]
    mouse_lb_release = HEX_MOUSE_KEYS["mouse_lb_release"]
    mouse_rb_press = HEX_MOUSE_KEYS["mouse_rb_press"]
    mouse_rb_release = HEX_MOUSE_KEYS["mouse_rb_release"]
    mouse_mb_press = HEX_MOUSE_KEYS["mouse_mb_press"]
    mouse_mb_release = HEX_MOUSE_KEYS["mouse_mb_release"]

    # direct keys
    dk = HEX_DIRECT_KEYS

    # virtual keys
    vk = HEX_VIRTUAL_KEYS

    # setup object
    def __init__(self, common=None):
        self.keys_worker = KeysWorker(self)
        # Thread(target=self.keys_worker.processQueue).start()
        self.common = common
        if common is None:
            self.standalone = True

    # parses keys string and adds keys to the queue
    def parseKeyString(self, string):
        # print keys
        if not self.standalone:
            self.common.info(f"Processing keys: {string}")

        key_queue = []
        errors = []

        # defaults to direct keys
        key_type = self.direct_keys

        # split by comma
        keys = string.upper().split(",")

        # translate
        for key in keys:
            # up, down or stroke?
            up = True
            down = True
            direction = key.split("_")
            subkey = direction[0]
            if len(direction) >= 2:
                if direction[1] == "UP":
                    down = False
                else:
                    up = False

            # switch to virtual keys
            if subkey == "VK":
                key_type = self.virtual_keys

            # switch to direct keys
            elif subkey == "DK":
                key_type = self.direct_keys

            # key code
            elif subkey.startswith("0x"):
                subkey = int(subkey, 16)
                if subkey > 0 and subkey < 256:
                    key_queue.append(
                        {
                            "key": int(subkey),
                            "okey": subkey,
                            "time": 0,
                            "up": up,
                            "down": down,
                            "type": key_type,
                        }
                    )
                else:
                    errors.append(key)

            # pause
            elif subkey.startswith("-"):
                time = float(subkey.replace("-", "")) / 1000
                if time > 0 and time <= 10:
                    key_queue.append(
                        {
                            "key": None,
                            "okey": "",
                            "time": time,
                            "up": False,
                            "down": False,
                            "type": None,
                        }
                    )
                else:
                    errors.append(key)

            # direct key
            elif key_type == self.direct_keys and subkey in self.dk:
                key_queue.append(
                    {
                        "key": self.dk[subkey],
                        "okey": subkey,
                        "time": 0,
                        "up": up,
                        "down": down,
                        "type": key_type,
                    }
                )

            # virtual key
            elif key_type == self.virtual_keys and subkey in self.vk:
                key_queue.append(
                    {
                        "key": self.vk[subkey],
                        "okey": subkey,
                        "time": 0,
                        "up": up,
                        "down": down,
                        "type": key_type,
                    }
                )

            # no match?
            else:
                errors.append(key)

        # if there are errors, do not process keys
        if len(errors):
            return errors

        # create new thread if there is no active one
        if self.keys_process is None or not self.keys_process.isAlive():
            self.keys_process = Thread(target=self.keys_worker.processQueue)
            self.keys_process.start()

        # add keys to queue
        for i in key_queue:
            self.keys_worker.key_queue.put(i)
        self.keys_worker.key_queue.put(None)

        return True

    # direct key press
    def directKey(self, key, direction=None, type=None):
        if type is None:
            type = self.direct_keys
        if direction is None:
            direction = self.key_press
        if key.startswith("0x"):
            key = int(key, 16)
        else:
            key = key.upper()
            lookup_table = self.dk if type == self.direct_keys else self.vk
            key = lookup_table[key] if key in lookup_table else 0x0000

        self.keys_worker.sendKey(key, direction | type)

    # direct mouse move or button press
    def directMouse(self, dx=0, dy=0, buttons=0):
        self.keys_worker.sendMouse(dx, dy, buttons)


class KeysWorker:
    # keys object
    keys = None

    # queue of keys
    key_queue = Queue()

    # init
    def __init__(self, keys):
        self.keys = keys

    # main function, process key's queue in loop
    def processQueue(self):
        # endless loop
        while True:
            # get one key
            key = self.key_queue.get()

            # terminate process if queue is empty
            if key is None:
                self.key_queue.task_done()
                if self.key_queue.empty():
                    return
                continue
            # print key
            elif not self.keys.standalone:
                self.keys.common.info(
                    "Key: \033[1;35m%s/%s\033[0;37m, duration: \033[1;35m%f\033[0;37m, direction: \033[1;35m%s\033[0;37m, type: \033[1;35m%s"
                    % (
                        key["okey"] if key["okey"] else "None",
                        key["key"],
                        key["time"],
                        "UP"
                        if key["up"] and not key["down"]
                        else "DOWN"
                        if not key["up"] and key["down"]
                        else "BOTH"
                        if key["up"] and key["down"]
                        else "NONE",
                        "None"
                        if key["type"] is None
                        else "DK"
                        if key["type"] == self.keys.direct_keys
                        else "VK",
                    ),
                    "\033[0;35mKEY:    \033[0;37m",
                )

            # if it's a key
            if key["key"]:
                # press
                if key["down"]:
                    self.sendKey(key["key"], self.keys.key_press | key["type"])

                # wait
                sleep(key["time"])

                # and release
                if key["up"]:
                    self.sendKey(key["key"], self.keys.key_release | key["type"])

            # not an actual key, just pause
            else:
                sleep(key["time"])

            # mark as done (decrement internal queue counter)
            self.key_queue.task_done()

    # send key
    def sendKey(self, key, type):
        self.SendInput(self.Keyboard(key, type))

    # send mouse
    def sendMouse(self, dx, dy, buttons):
        if dx != 0 or dy != 0:
            buttons |= self.keys.mouse_move
        self.SendInput(self.Mouse(buttons, dx, dy))

    # send input
    def SendInput(self, *inputs):
        nInputs = len(inputs)
        LPINPUT = INPUT * nInputs
        pInputs = LPINPUT(*inputs)
        cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
        return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

    # get input object
    def Input(self, structure):
        if isinstance(structure, MOUSEINPUT):
            return INPUT(0, _INPUTunion(mi=structure))
        if isinstance(structure, KEYBDINPUT):
            return INPUT(1, _INPUTunion(ki=structure))
        if isinstance(structure, HARDWAREINPUT):
            return INPUT(2, _INPUTunion(hi=structure))
        raise TypeError("Cannot create INPUT structure!")

    # mouse input
    def MouseInput(self, flags, x, y, data):
        return MOUSEINPUT(x, y, data, flags, 0, None)

    # keyboard input
    def KeybdInput(self, code, flags):
        return KEYBDINPUT(code, code, flags, 0, None)

    # hardware input
    def HardwareInput(self, message, parameter):
        return HARDWAREINPUT(
            message & 0xFFFFFFFF, parameter & 0xFFFF, parameter >> 16 & 0xFFFF
        )

    # mouse object
    def Mouse(self, flags, x=0, y=0, data=0):
        return self.Input(self.MouseInput(flags, x, y, data))

    # keyboard object
    def Keyboard(self, code, flags=0):
        return self.Input(self.KeybdInput(code, flags))

    # hardware object
    def Hardware(self, message, parameter=0):
        return self.Input(self.HardwareInput(message, parameter))


# types
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    )


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR),
    )


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", DWORD), ("wParamL", WORD), ("wParamH", WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (("type", DWORD), ("union", _INPUTunion))


if __name__ == "__main__":
    sleep(3)
    keys = Keys()

    # # mouse movement
    # for i in range(100):
    #     keys.directMouse(-1 * i, 0)
    #     sleep(0.004)

    # mouse keys
    # keys.directMouse(buttons=keys.mouse_rb_press)
    # sleep(0.5)
    # keys.directMouse(buttons=keys.mouse_lb_press)
    # sleep(2)
    # keys.directMouse(buttons=keys.mouse_lb_release)
    # sleep(0.5)
    # keys.directMouse(buttons=keys.mouse_rb_release)

    # or
    # keys.directMouse(buttons=keys.mouse_lb_press | keys.mouse_rb_press)
    # sleep(2)
    # keys.directMouse(buttons=keys.mouse_lb_release | keys.mouse_rb_release)

    # keyboard (direct keys)
    keys.directKey("a")
    sleep(1)
    keys.directKey("a", keys.key_release)
    # keyboard (virtual keys)
    # keys.directKey("d", type=keys.virtual_keys)
    # sleep(1)
    # keys.directKey("d", keys.key_release, keys.virtual_keys)

    # queue of keys (direct keys, threaded, only for keybord input)
    # keys.parseKeyString("d_down,-4,d_up,0x01")  # -4 - pause for 4 ms, 0x00 - hex code of Esc

    # queue of keys (virtual keys, threaded, only for keybord input)
    # keys.parseKeyString("vk,a_down,-4,a_up")  # -4 - pause for 4 ms
