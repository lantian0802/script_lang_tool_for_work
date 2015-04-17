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

def generateDataGenCommand(execParam):
    paramJson = json.loads(execParam)
    sparkSubmitCommand = "spark-submit --master "+paramJson["master"]+ \
                                       " --executor-memory "+paramJson["executor-memory"]+ \
                                       " --total-executor-cores "+paramJson["total-executor-cores"]+ \
                                       " --class "+paramJson["dataGen"]
    return sparkSubmitCommand

def single_submit_spark_job(execParam):

    genDataCommand = generateDataGenCommand(execParam)
    submitCommand = generateSparkSubmitCommand(execParam)
    ## 删除已经生成的数据
    removeDataCommand = "hadoop fs -rmr "+json.loads(execParam)["removePath"]
    ## 生成测试数据
    removeStatus = os.system(removeDataCommand)
    print(json.loads(execParam)["name"]+" 生成测试数据...")
    genStatus = os.system(genDataCommand)
    print("genStatus="+str(genStatus))
    ## 具体的任务执行
    print("#######################"+json.loads(execParam)["name"]+" start ...#############################")
    start = time.time()
    print(submitCommand)
    status = os.system(submitCommand)
    print(str(status)+" ")
    end = time.time()
    print "[SPARK_ON_ECS_BAT_TEST] JobName:"+json.loads(execParam)["name"]+" cost="+str(end-start)+"s  start time="+\
          time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start))+"  end time="+\
          time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end))
    print("##########################"+json.loads(execParam)["name"]+" end ...#############################")
    removeStatus = os.system(removeDataCommand)
    print(json.loads(execParam)["name"]+" 删除测试数据... exec status="+str(removeStatus))


def batch_submit_spark_job(execPlanPath):
    file = open(execPlanPath)
    while 1:
        line = file.readline()
        if not line:
            break
        single_submit_spark_job(line)

def startTsar(ipPath,homedir):
    print("pssh -h "+ipPath+" \"tsar --io --traffic --cpu --mem > "+homedir+"/tsar.log \" ")
    os.system("pssh -h "+ipPath+" \"tsar --io --traffic --cpu --mem > "+homedir+"/tsar.log \" ")

def collectTsar(userName,ipPath,srcFile,targetDir):
    file = open(ipPath)
    while 1:
        line = file.readline()
        if not line:
            break
        print("scp "+userName+"@"+line.strip('\n')+":"+srcFile+" "+targetDir+"/"+line.strip('\n')+"_tsar.log")
        os.system("scp "+userName+"@"+line.strip('\n')+":"+srcFile+" "+targetDir+"/"+line.strip('\n')+"_tsar.log")

##  scp jianying.wcj@10.207.24.6:/home/jianying.wcj/tsar.log ./tsarstat/
if __name__ == "__main__":
    ## 默认参数
    userName = "jianying.wcj"
    ipPath = "./ip.txt"
    homeDir = "/home/"+userName
    srcFile = homeDir+"/tsar.log"
    targetDir = "./tsarstat/"

    if len(sys.argv) < 2:
        print("plan file path parameter expected,please rerun the job with the parameter.")
    else :
        startTsar(ipPath,homeDir)
        execPlanPath = sys.argv[1]
        batch_submit_spark_job(execPlanPath)
        collectTsar(userName,ipPath,srcFile,targetDir)