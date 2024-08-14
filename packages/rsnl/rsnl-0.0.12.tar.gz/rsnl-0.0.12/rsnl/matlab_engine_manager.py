import matlab.engine
import multiprocessing as mp

engines = {}

def start_matlab_engine():
    eng = matlab.engine.start_matlab()
    eng.addpath('FUCCI')
    engines[mp.current_process().pid] = eng

def stop_matlab_engine():
    eng = engines.pop(mp.current_process().pid, None)
    if eng:
        eng.quit()
