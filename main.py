#!/usr/bin/env python3.6

import json, logging, os, re
from configparser import ConfigParser as cfgparser

configFile = 'settings.ini'

config = cfgparser()
config.read(configFile)

rootdir = config['codebase']['path']
luadefsPath = config['codebase']['luadefsPath']

searchableTypes = config['codebase']['searchableTypes'].split('|')

def findVariables(subroutineName):
    print('Searching')

def findSubroutineList(fileToSearch):
    print('Searching')

def generateFileList():
    fileList = {}
    for searchableType in searchableTypes:
        for root, dirs, files in os.walk(f"{rootdir}{searchableType}{luadefsPath}"):
            for cFile in files:
                if cFile.endswith('.cpp'):
                    fileList[cFile] = []
                    fullFilePath = f"{rootdir}{searchableType}{luadefsPath}{cFile}"
                    searchString = 'std::map<const char*, lua_CFunction> functions{'
                    nextString = '^    };$'
                    searchStringLine = 0
                    nextStringLine = 0
                    openedFile = open(fullFilePath).readlines()
                    for num, line in enumerate(openedFile):
                        if searchString in line:
                            searchStringLine = num
                    for num, line in enumerate(openedFile, searchStringLine):
                        if re.match(nextString, line):
                            nextStringLine = num - searchStringLine
                            break
                    if searchStringLine > 0:
                        for lineNumber in range(searchStringLine+1, nextStringLine):
                            lineData = openedFile[lineNumber]
                            if not re.match('\s+\/\/', lineData) and not re.match('^\s?$', lineData):
                                splitLine = lineData.split('"')
                                luaFunctionName = splitLine[1],
                                cppFunctionName = splitLine[2][2:-3]
                                fileList[cFile].append({
                                    'luaFunctionName': luaFunctionName,
                                    'cppFunctionName': cppFunctionName
                                })
                                subroutineStart = f"\w+ \w+::{cppFunctionName}\("
                                subroutineEnd = "^}$"
                                subroutineStartLine = 0
                                subroutineEndLine = 0
                                for num, line in enumerate(openedFile):
                                    if re.match(subroutineStart, line):
                                        subroutineStartLine = num
                                for num, line in enumerate(openedFile, subroutineStartLine):
                                    if re.match(subroutineEnd, line):
                                        if cppFunctionName == 'xmlLoadFile':
                                            print(num)
                                        subroutineEndLine = num
                                        break
                                if cppFunctionName == 'xmlLoadFile' and subroutineStartLine > 0:
                                    print(f"{subroutineStartLine} {subroutineEndLine}")
                                    for line in openedFile[subroutineStartLine:subroutineEndLine]:
                                        print(line)
generateFileList()
