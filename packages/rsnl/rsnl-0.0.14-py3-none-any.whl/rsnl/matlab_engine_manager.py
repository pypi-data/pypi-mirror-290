import matlab.engine
import multiprocessing as mp

engines = {}

def start_matlab_engine():
    print('debug: start_matlab_engine')
    print('debug: mp.current_process().pid =', mp.current_process().pid)
    eng = matlab.engine.start_matlab()
    eng.addpath('FUCCI')
    engines[mp.current_process().pid] = eng

def stop_matlab_engine():
    print('debug: stop_matlab_engine')
    print('debug: mp.current_process().pid =', mp.current_process().pid)
    eng = engines.pop(mp.current_process().pid, None)
    if eng:
        eng.quit()
