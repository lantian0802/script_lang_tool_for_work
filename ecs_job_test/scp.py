__author__ = 'jianying.wcj'
import os,sys

def singleScpFile(srcDir,targetDir):
    print("scp -r "+srcDir+" "+targetDir)
    os.system("scp -r "+srcDir+" "+targetDir)

def batchScpFile(ipPath,srcDir,targetDir,userName):
    file = open(ipPath)
    while 1:
        ipAddress = file.readline()
        if not ipAddress:
            break
        fullTargetDir = userName+"@"+ipAddress.strip("\n")+":"+targetDir
        singleScpFile(srcDir,fullTargetDir)
    return


if __name__ == "__main__":

    if len(sys.argv) < 5:
       print("parameter [ipPath] [srcDir] [targetDir] [userName] is expected....")
    else:
        ipPath = sys.argv[1]
        srcDir = sys.argv[2]
        targetDir = sys.argv[3]
        userName = sys.argv[4]

        batchScpFile(ipPath,srcDir,targetDir,userName)

