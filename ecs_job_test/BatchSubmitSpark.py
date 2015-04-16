__author__ = 'jianying.wcj'
#coding=utf-8
import sys
try:
    import json
except ImportError:
    import simplejson as json
import os
import time

def generateSparkSubmitCommand(execParam):
    paramJson = json.loads(execParam)
    sparkSubmitCommand = "spark-submit --class "+paramJson["class"]+ \
                                        " --master "+paramJson["master"]+ \
                                        " --executor-memory "+paramJson["executor-memory"]+ \
                                        " --total-executor-cores "+paramJson["total-executor-cores"]+ \
                                        " "+paramJson["appParam"]
    return sparkSubmitCommand


def single_submit_spark_job(execParam):
    removeDataCommand = "hadoop fs -rmr "+json.loads(execParam)["removePath"]
    submitCommand = generateSparkSubmitCommand(execParam)
    start = time.time()
    print(submitCommand)
    status = os.system(submitCommand)
    print(str(status)+" ")
    end = time.time()
    print "JobName:"+json.loads(execParam)["name"]+" cost="+str(end-start)+"s  start time="+\
          time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start))+"  end time="+\
          time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end))

    removeStatus = os.system(removeDataCommand)
    print("JobName:"+json.loads(execParam)["name"]+"remove path status = "+str(removeStatus))


def batch_submit_spark_job(execPlanPath):
    file = open(execPlanPath)
    while 1:
        line = file.readline()
        if not line:
            break
        single_submit_spark_job(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("plan file path parameter expected,please rerun the job with the parameter.")
    else :
        execPlanPath = sys.argv[1]
        batch_submit_spark_job(execPlanPath)