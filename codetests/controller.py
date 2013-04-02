#!/usr/bin/env python
import os
import tarfile
import datetime
import shutil
import time
from filecmp import cmp
from threading import Thread
from codetests.models import Test
from codetests.utils import InterruptableThread

TEST_PATH = "tests/"
SOURCE_PATH = "submissions/"

def verify_single(expected, actual):
    """
    Verifies output identity
    Args:
      expected (str) Path to expected output
      actual (str) Path to actual solution output
    Returns:
      1 if failed, 0 if passed (for counting failures)
    """
    failed = cmp(expected, actual)
    if (failed == True):
        result = 0
    else:
        result = 1

    return result

def run_script(basename, input_path, input_id, output_name):
    """
    Runs provided build script
    Args:
      basename (str) Path to dir containing build script
      input_path (str) Path to input dir
      input_id (str) Test input id
      output_name (str) Path to output file
    """
    os.system("./%s%s/run.sh %s%s/input > %s" % (SOURCE_PATH, 
        basename, input_path, input_id, output_name))

def timeout_kill(thread, limit, test_failed):
    """
    Kills execution thread when max execution time exceeded
    Args:
      thread (InterruptableThread) Thread to kill
      limit (float) Max execution time thread can run
      test_failed (int) 1 if thread needed to be killed
    """
    time.sleep(limit)
    if thread.isAlive():
        test_failed = 1
        thread.terminate()

def verify(problem_id, sourcefile):
    """
    Verifies that solution sourcefile of problem problem_id
    is correct
    Args:
      problem_id (str) Problem id (title)
      sourcefile (str) Path to solution
    """
    # Path to test inputs for problem problem_id
    input_path = TEST_PATH + problem_id + "/"

    # Get the name of the archived dir
    basename = sourcefile.split('.')[0]

    try:
        # Unzip and extract tarball, set permissions
        archive = tarfile.open(SOURCE_PATH + sourcefile)
        archive.extractall(path=SOURCE_PATH)
        os.system("chmod 755 " + SOURCE_PATH + basename)
        os.system("chmod 755 " + SOURCE_PATH + basename + "/run.sh")
    except Exception:
        return [-1, 0]

    result = 0
    allfiles = len(os.listdir(input_path))

    # Test all inputs
    for input_id in os.listdir(input_path):
        failed = 0
        #try:
        output_name = "output_%s_%s" % (sourcefile, input_id)

        # Read max time for execution in seconds
        limit_file = open(input_path + input_id + "/time_limit", "r")
        limit = float(limit_file.readline())/float(1000)
        limit_file.close()

        thread = InterruptableThread(target = run_script, args = (basename, input_path, input_id, output_name, ))
        thread.start()

        # This is to kill the execution thread if time-out
        killer_thread = InterruptableThread(target = timeout_kill, args = (thread, limit, failed))

        # If killer thread still alive, kill it
        if killer_thread.isAlive():
            killer_thread.terminate()

        # This is to prevent race conditions
        time.sleep(1)
        if (failed == 0): 
            failed = verify_single(input_path + input_id + "/output", 
                                   output_name)
        # Catch exception in case something went wrong for some test
        #except Exception:
        #    if (failed == 0):
        #        failed = 1

        result = result + failed

        # Clean up
        if os.path.exists(output_name):
            os.remove(output_name)

    # Clean up
    if os.path.exists(SOURCE_PATH + sourcefile):
        os.remove(SOURCE_PATH + sourcefile)
    if os.path.exists(SOURCE_PATH + basename):
        shutil.rmtree(SOURCE_PATH + basename)

    return [result, allfiles]
