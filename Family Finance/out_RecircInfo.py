# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:39:05 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG

class PrepRecirc:
    
    def insertRecircPRInfo(sqlInsertPRTuple):

#sqlInsertPRTuple
# [0] = prtransID, [1] = trans date, [2] = trans amount, [3] = trans source, 
# [4] = payer [5] = reimburser [6] date reimbursed [7] amt reimbursed [8] now()

#  0                1                 3                   5                         
# [0] = prtransID, [1] = trans date, [2] = trans source, [3] = reimburser 
#  6                   7 
# [4] date reimbursed [5] amt reimbursed 
        
        
        recircInfoDictList = []
        
        keyAmount = sqlInsertPRTuple[2]
        keyAmount = float(keyAmount)

        rPR_key = str(sqlInsertPRTuple[1]) + "*" + str(keyAmount) + "*" + sqlInsertPRTuple[4]
        #sql_outPRID, transDestination, reimburser, date reimbursed, amount reimbursed    
        recircInfoDictList = [str(sqlInsertPRTuple[0]),\
            str(sqlInsertPRTuple[3]),str(sqlInsertPRTuple[5]),\
            str(sqlInsertPRTuple[6]),str(sqlInsertPRTuple[7])]        
        
        varG.recircInfoDict[rPR_key] = recircInfoDictList
               
    
    def updateRecircPRInfo(prKey,prDate,prAmount):
        
        varG.recircInfoDict[prKey][3] = prDate                                            
        varG.recircInfoDict[prKey][4] = prAmount
        
        
    def updateEOJRecircPRInfo(sql_outPRID):
        
        varG.recircInfoDict[varG.prRIKey][0] = sql_outPRID        

    
    def updateEOJRecircTInfo(sql_outTransID):
        
        varG.recircInfoDict[varG.tRIKey][0] = sql_outTransID 
        varG.recircInfoDict[varG.tRIKey][1] = varG.tRILastRunLine

        if varG.headerList[3] == 'Master Card':
            varG.recircInfoDict[varG.tRIKey][1] = varG.tRILastRunLine
        elif varG.headerList[3] == 'Visa Card':
            varG.recircInfoDict[varG.tRIKey][2] = varG.tRILastRunLine
        elif varG.headerList[2] == 'Debit':
            varG.recircInfoDict[varG.tRIKey][1] = varG.tRILastRunLine                              
        
    

class WriteRI:

    def write_recircInfo(recircOutInfo):
        
        riKey = ""
        riKeyList = []
        outRecircInfo = ""
        
        for riKey in varG.recircInfoDict:
            riKeyList = varG.recircInfoDict[riKey]
            #if len(riKeyList) == 6:
            #print("\t","riKey=",riKey," riKeyList=",riKeyList)
                #      " riKeyList[1]=",riKeyList[1]," riKeyList[2]=",\
                #      riKeyList[2]," riKeyList[3]=",riKeyList[3],\
                #      " riKeyList[4]=",riKeyList[4]," riKeyList[5]=",\
                #      riKeyList[5])            
            outRecircInfo = outRecircInfo + riKey + ":"
            
            for x, y in enumerate(riKeyList):
                
                outRecircInfo = outRecircInfo + str(y) + ","
                
            outRecircInfo = outRecircInfo.rstrip(",")
            outRecircInfo = outRecircInfo + ":"

        
        outRecircInfo = outRecircInfo.rstrip(":")       
        recircOutInfo.write(outRecircInfo)
        
        recircOutInfo.close()
        
        varG.studyOutList.append("\n" + "Write: recircOutInfo=" + outRecircInfo)
        
        varG.studyOutList.append('\n' + 'recircOutInfo closed')       

