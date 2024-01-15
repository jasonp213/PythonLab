import logging
import logging.handlers
import multiprocessing
import time


def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def worker_process(task_queue, log_queue):
    worker_configurer(log_queue)
    logger = logging.getLogger(__name__)
    logger.info(f"Worker process {multiprocessing.current_process().name} starting.")
    while True:
        task = task_queue.get()
        if task == "STOP":
            logger.info(f"Worker process {multiprocessing.current_process().name} stopping.")
            break
        logger.info(f"Worker process {multiprocessing.current_process().name} received task: {task}")
        time.sleep(1)  # Simulate some work being done


def listener_configurer():
    root = logging.getLogger()
    h = logging.StreamHandler()
    f = logging.Formatter("%(asctime)s %(" "processName)-15s %(levelname)-8s %(message)s")
    h.setFormatter(f)
    root.addHandler(h)


def listener_process(queue):
    listener_configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys
            import traceback

            print("Whoops! Problem:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def main():
    log_queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process, args=(log_queue,))
    listener.start()

    task_queue = multiprocessing.Queue()
    workers = []
    number_of_processes = 4

    for _ in range(number_of_processes):
        worker = multiprocessing.Process(target=worker_process, args=(task_queue, log_queue))
        workers.append(worker)
        worker.start()

    for i in range(10):
        task_queue.put(f"Task {i}")

    for _ in range(number_of_processes):
        task_queue.put("STOP")

    for w in workers:
        w.join()

    log_queue.put_nowait(None)  # Tell the listener to quit
    listener.join()


if __name__ == "__main__":
    main()
