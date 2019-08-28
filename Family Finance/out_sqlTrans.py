# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:01:22 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from out_RecircInfo import PrepRecirc as riPrep


sql_outTransID = 0
prev_prDateKey = ""
sqlInsert_outTransALL = ""
sqlUpdateOTList = []

sqlInsert_oTCnt = 0
sqlUpdate_oTCnt = 0
creditPRKeyDict = {}

class TransSQL:
    
    def setOTGlobals(tranID):
        
        global sql_outTransID
        
        sql_outTransID = tranID
        
        print('last run sql_outTransID=',sql_outTransID)
        
    
    def sqlInsert_OutTransTuples(yesPayer,yesReimburser,payer,reimburser,\
        transDate,transAmount,transAction,transSource,transDestination,\
        transDescription,transCategory,transLocation):
        
        global sql_outTransID
        global sqlInsert_outTransALL
        global sqlInsert_oTCnt
        
        sqlInsert_TransTuple = "" 
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        sql_outTransID = sql_outTransID + 1
        

        sqlInsert_TransTuple = (sql_outTransID,str(transDate),transAmount,\
            str(transAction),str(transSource),str(transDestination),\
            str(transDescription),str(transCategory),str(varG.headerList[0]),\
            str(transLocation),str(varG.headerList[3]),0,'now()')
        
        sqlInsert_outTransALL = sqlInsert_outTransALL + "," + \
            str(sqlInsert_TransTuple)
            
        sqlInsert_oTCnt = sqlInsert_oTCnt + 1    
		
        
        return sqlInsert_TransTuple

    def sqlUpdate_TransPayReimbID(sql_outTID,keyPayReimb):
        
        global sql_outTransTable
        global sqlUpdateOTList
        global sqlUpdate_oTCnt
        
        queryStart = "update " + varG.sql_transTableName + "  set OA_T_PayReimb_ID = " \
            + str(keyPayReimb)

        queryEnd = "  where OA_T_TransID = " + str(sql_outTID) + ";"

        queryUpdate = queryStart + queryEnd
        sqlUpdateOTList.append(queryUpdate)
        
        sqlUpdate_oTCnt = sqlUpdate_oTCnt + 1
        
        
class WriteTrans:
    
    def write_sqlI_outTrans(sql_outTrans,sqlI_tDDL_List):
        
        global sql_outTransID
        global sqlInsert_outTransALL
        global sqlInsert_oTCnt
        
        #print(sqlI_tDDL_List)
                        
        lLimit = len(sqlI_tDDL_List)-3
        for x, y in enumerate(sqlI_tDDL_List):
            if x > lLimit:
                break
            y_line = y + " \n"
            sql_outTrans.write(y_line)
               
        first_sql = "INSERT INTO " + varG.sql_transTableName + " VALUES " 
        sql_outTrans.write(first_sql)  
                  

        sqlInsert_outTransALL = sqlInsert_outTransALL.strip(",") + ";"
        sql_outTrans.write(sqlInsert_outTransALL)
        
        sql_outTrans.write(sqlI_tDDL_List[-2])
        sql_outTrans.write(sqlI_tDDL_List[-1])
        
        sql_outTrans.close()
        
        riPrep.updateEOJRecircTInfo(sql_outTransID)
        
        
        varG.studyOutList.append('\n' + 'sql_outTrans closed')             
        
        varG.studyOutList.append('tRILastRunLine=' + \
            varG.tRILastRunLine)
                                        
        varG.studyOutList.append('sql_outTransID=' + str(sql_outTransID))
        
        varG.studyOutList.append('sqlInsert_oTCnt=' + str(sqlInsert_oTCnt))
        
    
    def write_sqlU_outTrans(sql_outUpdateTrans,sqlU_tDDL_List):
        
        global sqlUpdateOTList
        global sqlUpdate_oTCnt
       
        sqlUpdate_outTransALL = ""
        

        if sqlUpdateOTList !="":

            for x,y in enumerate(sqlUpdateOTList):

                sqlUpdate_outTransALL = sqlUpdate_outTransALL + y + " "

               
            lLimit = len(sqlU_tDDL_List)-3
            for x, y in enumerate(sqlU_tDDL_List):
                if x > lLimit:
                    break
                y_line = y + " \n"
                sql_outUpdateTrans.write(y_line)
                                       
            sqlUpdate_outTransALL = sqlUpdate_outTransALL.strip(",")
            sql_outUpdateTrans.write(sqlUpdate_outTransALL)
            
            sql_outUpdateTrans.write(sqlU_tDDL_List[-2])
            sql_outUpdateTrans.write(sqlU_tDDL_List[-1])
                
        
        sql_outUpdateTrans.close()
        
        varG.studyOutList.append('\n' + 'sql_outUpdateTrans closed')
        
        varG.studyOutList.append('sqlUpdate_oTCnt=' + str(sqlUpdate_oTCnt))
