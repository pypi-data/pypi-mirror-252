"""
本模块主要功能：
1. 按键状态判断
2. 虚拟按键码表
3. 日期时间格式化输出

该模块支持64位python
"""
from time import time
from time import sleep
from functools import wraps
import sys
from warnings import warn
from . import datetime_utils


try:
    import keyboard
except:
    # 大部分功能只有windows才可以用!
    pass


class VK:
    Time = 0.1
    Constant = 8000  # 内部标记

    ms_l = mouse_left = vk_lbutton = VK_LBUTTON = 1
    ms_r = mouse_right = vk_rbutton = VK_RBUTTON = 2
    cancel = VK_CANCEL = 3
    ms_m = mouse_middle = vk_mbutton = VK_MBUTTON = 4

    vk_xbutton1 = VK_XBUTTON1 = 5
    vk_xbutton2 = VK_XBUTTON2 = 6

    backspace = 8
    tab = 9
    clear = 12
    # enter = 13
    # shift = 16
    # ctrl = 17
    # alt = 18
    pause = 19
    caps_lock = 20
    esc = 27
    spacebar = 32
    page_up = 33
    page_down = 34
    end = 35
    home = 36
    left_arrow = 37
    up_arrow = 38
    right_arrow = 39
    down_arrow = 40
    select = 41
    print = 42
    execute = 43
    print_screen = 44
    insert = 45
    delete = 46
    help = 47
    num_0 = 48  # 大键盘数字编码
    num_1 = 49
    num_2 = 50
    num_3 = 51
    num_4 = 52
    num_5 = 53
    num_6 = 54
    num_7 = 55
    num_8 = 56
    num_9 = 57
    a = 65
    b = 66
    c = 67
    d = 68
    e = 69
    f = 70
    g = 71
    h = 72
    i = 73
    j = 74
    k = 75
    l = 76
    m = 77
    n = 78
    o = 79
    p = 80
    q = 81
    r = 82
    s = 83
    t = 84
    u = 85
    v = 86
    w = 87
    x = 88
    y = 89
    z = 90
    numpad_0 = 96  # 小键盘数字编码
    numpad_1 = 97
    numpad_2 = 98
    numpad_3 = 99
    numpad_4 = 100
    numpad_5 = 101
    numpad_6 = 102
    numpad_7 = 103
    numpad_8 = 104
    numpad_9 = 105
    multiply_key = 106
    add_key = 107
    separator_key = 108
    subtract_key = 109
    decimal_key = 110
    divide_key = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    num_lock = 144
    scroll_lock = 145
    left_shift = 160
    right_shift = 161
    left_control = 162
    right_control = 163
    left_menu = 164
    right_menu = 165
    browser_back = 166
    browser_forward = 167
    browser_refresh = 168
    browser_stop = 169
    browser_search = 170
    browser_favorites = 171
    browser_start_and_home = 172
    volume_mute = 173
    volume_Down = 174
    volume_up = 175
    next_track = 176
    previous_track = 177
    stop_media = 178
    play = 179
    pause_media = 179
    start_mail = 180
    select_media = 181
    start_application_1 = 182
    start_application_2 = 183
    attn_key = 246
    crsel_key = 247
    exsel_key = 248
    play_key = 250
    zoom_key = 251
    clear_key = 254

    symbol = {'+': 0xBB,
              ',': 0xBC,
              '-': 0xBD,
              '.': 0xBE,
              '/': 0xBF,
              '`': 0xC0,
              ';': 0xBA,
              '[': 0xDB,
              '\\': 0xDC,
              ']': 0xDD,
              "'": 0xDE,
              '\`': 0xC0}
    ##########
    shift = 16
    ctrl = 17
    alt = 18

    f1 = 112
    f2 = 113
    f3 = 114
    f4 = 116
    f5 = 117

    enter = 13
    space = 32
    back = 8

    # 小键盘数字
    n0, n1, n2, n3, n4, n5, n6, n7, n8, n9 = 96, 97, 98, 99, 100, 101, 102, 103, 104, 105
    left, up, right, down = 37, 38, 39, 40

    def conv_ord(self, ch):  # 转换类型, return: vitual_key_code
        # ch = 'q'
        if isinstance(ch, int):
            return ch
        if isinstance(ch, str):
            if ch.islower():
                ch = ch.upper()
            return ord(ch)

    1


vk = VK()


def run_f_with_sleep(sleep_time=1):
    def decorator_name(testf):
        @wraps(testf)
        def decorated(*args, **kwargs):
            tt.sleep(sleep_time)

            return testf(*args, **kwargs)

        return decorated

    return decorator_name


def run_f_with_during(during_time=5, sleep_time=1, break_key='alt + s'):
    tt = Time()

    def decorator_name(testf):
        @wraps(testf)
        def decorated(*args, **kwargs):
            def circulate_f(*args, **kwargs):
                ret = None

                def setBreakFlag(tt):
                    tt.break_flag = 1
                    print(f'用户手动中断! --------------- 总运行时间: [{tt.now(2)}/{during_time}] 秒')

                keyboard.add_hotkey(break_key, lambda: setBreakFlag(tt))

                run_times = 0
                while tt.during(during_time):
                    run_times += 1
                    if tt.break_flag:
                        break

                    tt.sleep(sleep_time)

                    ret = testf(*args, **kwargs)
                    print(
                        f'第 [{run_times}] 次运行的返回值为: [{ret}]. ------------- 总运行时间 :[{tt.now(2)}/{during_time}] 秒, ')  # 0改为int类型!

                keyboard.remove_hotkey(break_key)
                return ret

            return circulate_f(*args, **kwargs)

        return decorated

    return decorator_name


class Time():
    def __init__(self):
        self.t0 = time()
        self.t1 = time()
        self.time = time
        self.sleep = sleep
        self.now()
        self.break_flag = 0

        self.common_date_time_formats = datetime_utils.common_date_time_formats
        self.datetime_utils = datetime_utils

    def set_timezone(self, my_timezone):
        self.datetime_utils.LOCAL_TIMEZONE = my_timezone

    def set_default_time_format(self, default_time_format):
        self.datetime_utils.DEFAULT_TIME_FORMAT = default_time_format

    def set_default_decimal_places(self, default_decimal_places):
        self.datetime_utils.DEFAULT_DECIMAL_PLACES = default_decimal_places

    def now(self, round_=3):  # return now time
        self.t1 = time()
        now = self.t1 - self.t0

        if round_ == 0:
            now_r = int(now)
        else:
            now_r = round(now, round_)

        return now_r

    def get_current_beijing_time_dt(self):
        """
        当前的北京时间(返回datetime格式)
        """
        return datetime_utils.get_current_beijing_time_dt()

    def get_current_beijing_time_str(self, fmt: str = None, decimal_places: (int, None) = None):
        """
       得到当前的北京时间字符串

       :param fmt: 时间格式, 如"%Y-%m-%d %H:%M:%S.%f"
       :param decimal_places: 保留几位小数
       :return: 当前的北京时间字符串
       """
        return datetime_utils.get_current_beijing_time_str(fmt, decimal_places)

    def tqdm_sleep(self, desc='正在启动程序...', T=3, times=100, fresh=0):
        from tqdm import tqdm
        # from tqdm import tqdm_gui
        if (fresh == 0):  # 刷新频率
            fresh = T / times
        else:
            times = int(T / fresh)

        t0 = self.time()
        try:
            with tqdm(range(times), desc=desc, unit=' it', ascii=True) as bar:  # , ascii=True

                # print('\r -------- 启动 ------- ', tt.now(1))
                for i in bar:
                    self.sleep(fresh)

        except KeyboardInterrupt:
            bar.close()
        bar.close()

        return

    # return: tt.now() >= T
    def exceed(self, T):
        if (self.now() >= T):
            return 1
        else:
            return 0

    # return: tt.now() <= T
    def during(self, T):
        if (self.now() <= T):
            return 1
        else:
            return 0

    def MessageBox(self, text='Text', title='Warning!', model=0, hwnd=0):
        from win32gui import MessageBox
        return MessageBox(hwnd, text, title, model)


    def get_key_state(self, virtual_key: str = vk.mouse_right):
        from win32api import GetAsyncKeyState
        _key_state = GetAsyncKeyState(virtual_key)
        key_state = 1 if _key_state & 0x8000 else 0
        return key_state

    def is_pressed(self, hotkey):
        return keyboard.is_pressed(hotkey)

    def stop(self, ch='alt + s', raise_error=True):
        break_flag = 0
        if self.is_pressed(ch):
            if raise_error:
                raise IOError("*** Stopped by user!")
            else:
                break_flag = True
        return break_flag

    def stop_alt(self, ch='s', raise_error=True):
        hotkey = 'alt + ' + ch

        break_flag = False
        if self.is_pressed(hotkey):
            if raise_error:
                raise IOError("*** Stopped by user!")
            else:
                break_flag = True
        return break_flag

    @classmethod
    def run_f_with_during(cls, *args, **kwargs):
        return run_f_with_during(*args, **kwargs)

    @classmethod
    def run_f_with_sleep(cls, *args, **kwargs):
        return run_f_with_sleep(*args, **kwargs)


tt = Time()

if __name__ == '__main__':
    # 默认保留2位小数
    ret = tt.get_current_beijing_time_str()
    print(ret)

    # 这个适合做临时文件的文件名后缀
    ret = tt.get_current_beijing_time_str(tt.common_date_time_formats.ms_int)
    print(ret)
