#!/usr/bin/env python
#import sys
import os
import tarfile
import datetime
import shutil
import time
from threading import Thread
from codetests.models import Test
from codetests.utils import InterruptableThread

TEST_PATH = "tests/"
SOURCE_PATH = "submissions/"

#problem_id = sys.argv[1]
#sourcefile = sys.argv[2]

def verify_single(expected, actual):
    exp_file = open(expected, "r")
    act_file = open(actual, "r")
    
    result = 0

    for exp_line in exp_file.readlines():
        act_line = act_file.readline()
        if (exp_line.strip() != act_line.strip()):
            result = 1
            break
    
    exp_file.close()
    act_file.close()

    return result

def run_script(basename, input_path, input_id, output_name):
    os.system("./%s%s/run.sh %s%s/input > %s" % (SOURCE_PATH, 
        basename, input_path, input_id, output_name))

def timeout_kill(thread, limit, test_failed):
    time.sleep(limit)
    if thread.isAlive():
        test_failed = 1
        thread.terminate()        

def verify(problem_id, sourcefile):
    input_path = TEST_PATH + problem_id + "/"

    basename = sourcefile.split('.')[0]
    #os.system("tar -xvzf " + SOURCE_PATH + sourcefile)
    
    try:
        archive = tarfile.open(SOURCE_PATH + sourcefile)
        archive.extractall(path=SOURCE_PATH)
        os.system("chmod 755 " + SOURCE_PATH + basename)
        os.system("chmod 755 " + SOURCE_PATH + basename + "/run.sh")
    except Exception:
        return [-1, 0]

    result = 0
    allfiles = len(os.listdir(input_path))
    
    for input_id in os.listdir(input_path):
        failed = 0
        #try:
        output_name = "output_%s_%s" % (sourcefile, input_id)
        
        limit_file = open(input_path + input_id + "/time_limit", "r")
        limit = float(limit_file.readline())/float(1000)
        limit_file.close()
        
        thread = InterruptableThread(target = run_script, args = (basename, input_path, input_id, output_name, ))
        thread.start()

        killer_thread = InterruptableThread(target = timeout_kill, args = (thread, limit, failed))
        
        if killer_thread.isAlive():
            killer_thread.terminate()
        
        time.sleep(1)
        if (failed == 0): 
            failed = verify_single(input_path + input_id + "/output", 
                                   output_name)
        #except Exception:
        #    if (failed == 0):
        #        failed = 1
    
        result = result + failed
        if os.path.exists(output_name):
            os.remove(output_name)
    
    if os.path.exists(SOURCE_PATH + sourcefile):
        os.remove(SOURCE_PATH + sourcefile)
    if os.path.exists(SOURCE_PATH + basename):
        shutil.rmtree(SOURCE_PATH + basename)
    
    return [result, allfiles]
