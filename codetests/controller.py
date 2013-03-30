#!/usr/bin/env python
#import sys
import os
import tarfile
import datetime
import shutil
from codetests.models import Test

TEST_PATH = "tests/"
SOURCE_PATH = "submissions/"

#problem_id = sys.argv[1]
#sourcefile = sys.argv[2]

def verify_single(expected, actual):
    exp_file = open(expected, 'r')
    act_file = open(actual, 'r')

    for exp_line in exp_file.readlines():
        act_line = act_file.readline()
        if (exp_line.strip() != act_line.strip()):
            return 1
    return 0

def verify(problem_id, sourcefile):
    input_path = TEST_PATH + problem_id + "/inputs/"
    solution_path = TEST_PATH + problem_id + "/solutions/"

    basename = sourcefile.split('.')[0]
    #os.system("tar -xvzf " + SOURCE_PATH + sourcefile)
    
    try:
        archive = tarfile.open(SOURCE_PATH + sourcefile)
        archive.extractall(path=SOURCE_PATH)
        os.system("chmod 777 " + SOURCE_PATH + basename)
        os.system("chmod 777 " + SOURCE_PATH + basename + "/run.sh")
    except Exception:
        return [-1, 0]

    result = 0
    allfiles = len(os.listdir(input_path))
    
    for filename in os.listdir(input_path):
        failed = 0
        try:
            output_name = "output_%s_%s" % (sourcefile, filename)
            limit = Test.objects.get(problem_title=problem_id, test_input=filename).max_duration
            start = datetime.datetime.now() 
            os.system("./%s%s/run.sh %s%s > %s" % (SOURCE_PATH, basename, input_path, filename, output_name))
            end = datetime.datetime.now()
            delta = end - start
            if delta.microseconds/1000 > limit:
                failed = 1
            else:
                failed = verify_single(solution_path + filename, output_name)
        except Exception:
            if (failed == 0):
                failed = 1
        
        result = result + failed
        if os.path.exists(output_name):
            os.remove(output_name)
    
    if os.path.exists(SOURCE_PATH + sourcefile):
        os.remove(SOURCE_PATH + sourcefile)
    if os.path.exists(SOURCE_PATH + basename):
        shutil.rmtree(SOURCE_PATH + basename)

    return [result, allfiles]
