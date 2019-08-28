# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:50:39 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG

class Parameters(object):
    def __init__(self, runList):
        self.runList = runList        
        
        #runList = [runDictKey,runNumber,runParams,runYear,runRange,runType,
        #          runOwner,runAccount,runPrefix1,runPrefix2,runSuffix]
        # 'sql':('1','1') = 'sql:(A group sql files, B group sql files)
        #                 = '1' equals create-insert  sql ddl
        #                 = '2' equals insert sql ddl
        # A group sql files:  PayReimb
        # B group sql files:  owner/account Trans
        
        
        #override output 'r#" by placing specific ouput number if necessary 
        dictRunParam = {'1':
             {'insql':('1','1'),'inrecirc':'r#-1','output1':'r#',
              'output2':'r#'},            
             '2':{'insql':('2','2'),'inrecirc':'r#-1','output1':'r#',
             'output2':'r#'}, 
             '3':{'insql':('2','1'),'inrecirc':'r#-1','output1':'r#',
             'output2':'r#'}}

        runDictKey = ''
        runParams = [(0,0),0,0,0]   #[(0,0),0,0,0] = [sql,recirc,output1,output2]
        
        nameRL = ['runPath','runDictKey','runNumber','runOAnumber','runYear',
            'runRange','runType','runOwner','runAccount','runPrefix1',
            'runPrefix2','inSQLA','inSQLB','inRecirc','outSQLA','outSQLB',
            'output1','output2']
                    
        #unload runList
        runDictKey = self.runList[1]
        runNumber = self.runList[2]
        runOAnumber = self.runList[3]
        
        
        sqlTuple = dictRunParam[runDictKey]['insql']
        recirc = dictRunParam[runDictKey]['inrecirc']
        output1 = dictRunParam[runDictKey]['output1']
        output2 = dictRunParam[runDictKey]['output2']

        
        runParams[0] = sqlTuple
        if recirc == 'r#-1':
            runParams[1] = int(runNumber) - 1
        else:
            runParams[1] = recirc
        
        if output1 != 'r#':
            runNumber = output1
        if output2 != 'r#':
            runOAnumber = output2

        runParams[2] = runNumber
        runParams[3] = runOAnumber
            
            
        
        inSQLA = sqlTuple[0]
        self.runList.append(inSQLA)
        
        inSQLB = sqlTuple[1]
        self.runList.append(inSQLB)
        
        inRecirc = runParams[1]
        self.runList.append(inRecirc)
        
        outSQLA = sqlTuple[0] + '-' + str(runParams[2])
        self.runList.append(outSQLA)
        
        outSQLB = sqlTuple[1] + '-' + str(runParams[3])
        self.runList.append(outSQLB)
        
        output1 = runParams[2]
        self.runList.append(output1)
        output2 = runParams[3]
        self.runList.append(output2)
        
        
        varG.studyOutList.append('dictRunParam=' + str(dictRunParam) + '\n')

        print("\n","Parameters:","\n")
        for x, y in enumerate(self.runList):
            varG.studyOutList.append(str(nameRL[x]) + '=' + str(y) + '\n')       
            print("\t",str(nameRL[x]) + '=' + str(y) + '\n')
            
            
        
        
        
        
        






