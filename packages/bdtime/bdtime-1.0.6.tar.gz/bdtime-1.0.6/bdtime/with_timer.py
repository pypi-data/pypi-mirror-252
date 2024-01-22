import time


class WithTimer:
    """
    # 使用示例
    with WithTimer("test_func"):
        # 在这里放置要测量执行时间的代码
        for _ in range(1000):
            pass
    """
    mute_all = False
    mute_enter = False
    mute_exit = False

    def __init__(self, name, tt=None, debug=None):
        self.name = name

        if tt is not None:
            assert hasattr(tt, 'now'), 'tt必须实现方法`now`, 以获取当前总花费时间!'
        self.tt = tt

        if debug is None:
            debug = not WithTimer.mute_all
        self.debug = debug

    def __enter__(self):
        if self.debug and not WithTimer.mute_enter:
            msg = f"====== enter WithTimer[{self.name}]"
            if self.tt:
                msg += f", now: {self.tt.now()}"

            print()
            print(msg)
        self.last_show_time = self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        if self.debug and not WithTimer.mute_exit:
            msg = f"====== exit WithTimer[{self.name}] cost seconds: {elapsed_time:.3f}"
            if self.tt:
                msg += f', now: {self.tt.now()}'
            print(msg)

    def show(self, desc="", show_cost=True, show_now=True, reset_cost=False):
        """
        show desc
        :param desc: 描述文本
        :param show_cost: show cost time
        :param show_now: show current time
        :param reset_cost: reset cost time when it was call by another code
        """
        self.end_time = time.time()
        # elapsed_time = self.end_time - self.start_time
        elapsed_time = self.end_time - self.last_show_time
        if reset_cost:
            self.last_show_time = self.end_time

        msg = f""

        if desc:
            msg += f' {desc}'
        if show_cost:
            msg += f' --- cost: {elapsed_time: .3f}'
        if self.tt and show_now:
            msg += f" --- now: {self.tt.now()}"
        print(msg)


with_timer = WithTimer

if __name__ == '__main__':
    from bdtime import tt

    # with_timer.mute_all = True
    with_timer.mute_enter = True
    tt.sleep(2)
    with with_timer('测试', tt) as wt:
        for i in range(10):
            tt.sleep(0.3)
            if i % 5 == 0:
                wt.show(f"第{i}次的loss: {i * 2 / 5}")
