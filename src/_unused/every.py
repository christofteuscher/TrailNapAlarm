
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
import time, traceback

def every(delay, task, retry=False):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc() # Prints to STDerr
      if not retry:
        return
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

sample_rate = 200
begin = time.perf_counter()
begin_t = time.time()
i = 0
s = 0

def next_sample():
    global begin, begin_t, i, s
    
    
    i += 1
    if i > sample_rate:
        i = 0
        s += 1
    elapsed = time.perf_counter() - begin
    elapsed_t = time.time() - begin_t
    print("\r[Timer] Seconds: {:4}, Ticks: {:3}, Elapsed: {:4.2f}, Elapsed: {:4.2f}".format(s, i, elapsed, elapsed_t), end='')

if __name__ == "__main__":
    every(1/sample_rate, next_sample)