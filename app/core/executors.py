from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

THREAD_XQTR = ThreadPoolExecutor()
PROCESS_XQTR = ProcessPoolExecutor()

__all__ = ["THREAD_XQTR", "PROCESS_XQTR"]
