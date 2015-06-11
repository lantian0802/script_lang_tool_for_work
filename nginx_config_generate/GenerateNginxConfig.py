__author__ = 'jianying.wcj'
#coding=utf-8
import sys
import os

##根据模板生成对应的 upstream 和 server的配置
def doGenerateUpstreamServerConfig(sparkHostInfoPath):

    format_tab="\t"
    format_tab2 = format_tab*2
    upStreamPlaceTemplate=format_tab+"upstream server_${hostname} {"+os.linesep+ \
                          format_tab2+"server ${host}:${port};"+os.linesep+ \
                          format_tab+"}"
    serverPlaceHolderTemplate=format_tab+"server {"+os.linesep+ \
                              format_tab2+"listen 80;"+os.linesep+ \
                              format_tab2+"server_name ${hostname};"+os.linesep+ \
                              format_tab2+"location / {"+os.linesep+ \
                              format_tab2+"        proxy_pass http://server_${hostname};"+os.linesep+ \
                              format_tab2+"}"+os.linesep+ \
                              format_tab+"}"
    sparkHostInfoFile = open(sparkHostInfoPath)
    hostInfoLines = sparkHostInfoFile.readlines()

    upStreamStr = ""
    serverStreamStr = ""

    sparkMasterHostName = "spark_master"
    upStreamMasterItem = upStreamPlaceTemplate.replace("${hostname}",sparkMasterHostName)\
                                            .replace("${host}","127.0.0.1")\
                                            .replace("${port}","8080").replace("\t","",1)
    serverStreamMasterItem = serverPlaceHolderTemplate.replace("${hostname}",sparkMasterHostName).replace("\t","",1)

    upStreamStr += upStreamMasterItem+ os.linesep
    serverStreamStr += serverStreamMasterItem+os.linesep

    for hostInfo in hostInfoLines:
        hostInfoList = hostInfo.split(" ")
        print("tuple="+str(hostInfoList))
        upStreamItem = upStreamPlaceTemplate.replace("${hostname}",hostInfoList[1].strip())\
                                            .replace("${host}",hostInfoList[0].strip())\
                                            .replace("${port}","8081")
        serverStreamItem = serverPlaceHolderTemplate.replace("${hostname}",hostInfoList[1].strip())

        upStreamStr += upStreamItem.rstrip()+ os.linesep
        serverStreamStr += serverStreamItem.rstrip()+os.linesep
    return (upStreamStr,serverStreamStr)

## 替换原有nginx的配置文件
def doUpdateNginxConfigFile(resultContent,nginxConfigTagetPath):
    nginxConfigFile = file(nginxConfigTagetPath,"w")
    nginxConfigFile.write(resultContent)

## 生成配置文件的完整内容
def generateConfigFile(sparkHostInfoPath,nginxConfigTemplatePath,nginxConfigTagetPath):

     upStreamPlaceHolder="${upstream_place_holder}"
     serverPlaceHolder="${server_place_holder}"

     nginxUpstreamServerTuple = doGenerateUpstreamServerConfig(sparkHostInfoPath)

     nginxConfigTemplateFile = open(nginxConfigTemplatePath)
     nginxConfigTemplateLines = nginxConfigTemplateFile.readlines()
     resultContent = ""
     for line in nginxConfigTemplateLines:
        resultContent += line
     ##替换占位符
     resultContent = resultContent.replace(upStreamPlaceHolder,nginxUpstreamServerTuple[0]) \
                  .replace(serverPlaceHolder,nginxUpstreamServerTuple[1])
     print("resultContent="+resultContent)
     ##更新配置文件
     doUpdateNginxConfigFile(resultContent,nginxConfigTagetPath)

if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print "at least 3 parameters expected," \
              "they are [sparkHostInfoPath] [nginxConfigTemplatePath] [nginxConfigTagetPath]"
    else:
        ##spark集群的机器 hostname ip信息文件路径
        sparkHostInfoPath = sys.argv[1]
        ## nginx基础模板文件路径
        nginxConfigTemplatePath = sys.argv[2];
        ## nginx配置文件的目标路径，如果已经存在则覆盖
        nginxConfigTagetPath = sys.argv[3];

        generateConfigFile(sparkHostInfoPath,nginxConfigTemplatePath,nginxConfigTagetPath)









