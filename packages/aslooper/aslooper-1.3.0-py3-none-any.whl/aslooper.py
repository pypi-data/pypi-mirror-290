"""
looper-佛跳墙活套
"""

__all__ = ["looper"]


import asyncio
import functools
import inspect
from signal import SIGINT, SIGTERM
from typing import Callable, Awaitable, Coroutine
from typing import TypeVar, ParamSpec
from typing import Optional
# from types import FunctionType


# def __cancel_all_tasks():
#     """取消所有任务
#
#     :return:
#     """
#     for task in asyncio.all_tasks():
#         if task is not asyncio.current_task():
#             print(f"Cancel Task {task}")
#             task.cancel()
#
#
# def __signal_cancel_run(call: Union[Callable, Awaitable] = None):
#     """取消所有任务，并执行自定义任务
#
#     :return:
#     """
#     loop = asyncio.get_running_loop()
#     for task in asyncio.all_tasks():
#         if task is not asyncio.current_task():
#             print(f"[Cancel Task] {task}")
#             task.cancel()
#     if call:
#         if asyncio.iscoroutinefunction(call):
#             loop.run_until_complete(call())
#         elif asyncio.iscoroutine(call):
#             loop.run_until_complete(call)
#         # elif isinstance(call, FunctionType):
#         #     call()
#         elif callable(call):
#             call()
#         else:
#             print(f"[Error Call] {call}")
#
#
# def looper(func, call: Union[Callable, Awaitable] = None):
#     """异步函数装饰器:
#     用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务，退出运行不报错。
#     """
#     if not asyncio.iscoroutinefunction(func):
#         raise TypeError(f"{func} is not coroutinefunction.")
#
#     @functools.wraps(func)
#     async def loop_signal_handler(*args, **kwargs):
#         loop = asyncio.get_running_loop()
#         # Add signal
#         for signal in (SIGINT, SIGTERM):
#             try:
#                 loop.add_signal_handler(
#                     signal,
#                     # lambda: asyncio.create_task(__cancel_all_tasks(), name="signal_handler_call")
#                     # __cancel_all_tasks
#                     __signal_cancel_run,
#                     call
#                 )
#             except NotImplementedError:
#                 # logger.warning(
#                 #     "crawler tried to use loop.add_signal_handler "
#                 #     "but it is not implemented on this platform."
#                 # )
#                 pass
#         try:
#             return await func(*args, **kwargs)
#         except asyncio.CancelledError:
#             print("Exit!")
#
#     return loop_signal_handler


FuncReturnType = TypeVar('FuncReturnType')
FuncParamType = ParamSpec('FuncParamType')


class Looper:
    """装饰器对象，用来装饰异步函数，用于取消异步任务。

    注意：只在主线程中运行。

    :param call: 自定义任务，可以是同步函数、异步函数、协程对象、可调用对象。
    :param debug: 是否打印调试信息。
    """

    def __init__(self, call: Callable = None, *,
                 debug: bool = True):
        """（call 暂时只能支持同步函数，异步函数没研究出来 - -！）"""
        self.call = call
        self.debug = debug
        self.func: Optional[Callable[FuncParamType, FuncReturnType]] = None  # 存放装饰的异步函数
        self.func_coroutine: Optional[Coroutine] = None  # 存放装饰的异步函数协程对象

    def print(self, *args):
        if self.debug:
            print(*args)

    def __signal_cancel_run(self, loop: asyncio.AbstractEventLoop):
        """取消所有任务，并执行自定义任务"""
        if not self.call:
            pass
        elif asyncio.iscoroutinefunction(self.call):
            loop.run_until_complete(self.call())
        elif inspect.isawaitable(self.call):
            loop.run_until_complete(self.call)
        elif inspect.iscoroutine(self.call):
            loop.run_until_complete(self.call)
        elif callable(self.call):
            self.call()
        else:
            self.print(f"[Error] Call {self.call}")
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                self.print(f"[Cancel] {task}")
                task.cancel(msg=f"looper cancel task {task}")

    async def run_func(self) -> FuncReturnType:
        """用于__await__执行"""
        try:
            return await self.func_coroutine
        except asyncio.CancelledError:
            self.print("Exit!")

    def __await__(self):
        """
        必须定义这个方法才能直接 await 这个类的对象
        并且，返回值必须是一个 iterator，这里直接
        使用 async 函数的内置方法 __await__()
        """
        return self.run_func().__await__()

    def __call__(self,
                 func: Callable[FuncParamType, FuncReturnType]
                 ) -> Callable[..., Awaitable[FuncReturnType]]:
        """异步函数装饰器:
        用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务，退出运行不报错。
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f"{func} is not coroutine function.")
        self.func = func

        @functools.wraps(func)
        async def loop_signal_handler(*args: FuncParamType.args, **kwargs: FuncParamType.kwargs):
            loop = asyncio.get_running_loop()
            # Add signal
            for signal in (SIGINT, SIGTERM):
                try:
                    loop.add_signal_handler(
                        signal,
                        functools.partial(self.__signal_cancel_run, loop),
                    )
                except NotImplementedError:
                    # logger.warning(
                    #     "crawler tried to use loop.add_signal_handler "
                    #     "but it is not implemented on this platform."
                    # )
                    pass
            self.func_coroutine = self.func(*args, **kwargs)
            await self
        return loop_signal_handler


looper = Looper
