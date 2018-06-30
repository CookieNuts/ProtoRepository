#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import platform
import argparse
import shutil
import time

currentPath = os.path.abspath(__file__)
rootPath = os.path.abspath(os.path.dirname(currentPath) + os.path.sep + ".")
protoPath = os.path.join(rootPath, "protos")
targetPath = os.path.join(rootPath, "generate")
allPrefix = {"java": " --java_out=", "cshap": " --csharp_out=", "python": " --python_out="}

def generateCmd(rootPath):
	sysstr = platform.system()
	if (sysstr == "Windows"):
		return os.path.join(rootPath, "protoc_tools_win", "bin", "protoc")
	elif (sysstr == "Linux"):
		return os.path.join(rootPath, "protoc_tools_linux", "bin", "protoc")
	else:
		return os.path.join(rootPath, "protoc_tools_linux", "bin", "protoc")

def execCmd(basePath, targetPath):
	for root, dirs, files in os.walk(basePath):
		for fileName in files:
			if fileName.endswith(".proto"):
				cmdCode = cmd + " -I=" + protoPath + targetPath + " "+ os.path.join(root, fileName)
				print(cmdCode)
				result = os.popen(cmdCode)
				print(result.read())
		for name in dirs:
			execCmd(os.path.join(root, name), targetPath)

def execInit(targetPath):
	if os.path.exists(targetPath):
		shutil.rmtree(targetPath)
		#sleep for delete finish!
		time.sleep(1)
	os.mkdir(targetPath)
	for key in allPrefix.keys():
		os.mkdir(os.path.join(targetPath, key))
	allFilePath = {"java": os.path.join(rootPath, "generate", "java"),
				   "cshap": os.path.join(rootPath, "generate", "cshap"),
				   "python": os.path.join(rootPath, "generate", "python")}
	return allFilePath

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description='Welcome To Proto Generator!')
	parser.add_argument('-l', action="store", dest="languate", help=" Select Generate Languate: [java, cshap, python]")
	results = parser.parse_args()
	languate  = results.languate
	print("Exec Generate %s File!" % languate)
	if languate in allPrefix.keys():
		allFilePath = execInit(targetPath)
		cmd = generateCmd(rootPath)
		execCmd(protoPath, allPrefix[languate]+allFilePath[languate])
	else:
		print("Languate Select Error!")


