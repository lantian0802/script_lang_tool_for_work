#coding=utf-8
import os

##将Spark机器名映射信息从本机拷贝到其他机器
def copyHostInfoFile(opts,hostInfoFilePath,ip,dst):
    try:
        print "sshpass -p "+str(opts.pwd)+" scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+hostInfoFilePath+ " "+opts.user+"@"+ip+":"+dst
        os.system("sshpass -p "+str(opts.pwd)+" scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+hostInfoFilePath+" "+opts.user+"@"+ip+":"+dst)
    except Exception as e:
        print(e.message)
        raise e

## 执行远程命令
def executeRemoteCommand(opts,ip,command):
    print "sshpass -p "+str(opts.pwd)+" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+opts.user+"@"+ip+" "+command
    os.system("sshpass -p "+str(opts.pwd)+" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+opts.user+"@"+ip+" "+command)

## 拷贝文件=》生成nginx配置 =》启动nginx
def configFileAndStartNginx(opts,hostInfoFilePath,ip,dst):
    ##将Spark配置文件拷贝到Master机器
    copyHostInfoFile(opts,hostInfoFilePath,ip,dst)
    generateConfigFileCommand = "python ./GenerateNginxConfig.py"
    startNginxCommand = "bash /opt/nginx-1.9.1/sbin/nginx"
    ##拷贝远程文件
    executeRemoteCommand(opts,ip,generateConfigFileCommand)
    ##启动nginx集群
    executeRemoteCommand(opts,ip,startNginxCommand)

if __name__=="__main__":

    class Opts:
        user = ""
        pwd = ""

    opts = Opts()
    opts.user=""
    opts.pwd=""
    hostInfoFilePath="./jianying01-hosts"
    ip=""
    dst="/root/"
    configFileAndStartNginx(opts,hostInfoFilePath,ip,dst)





