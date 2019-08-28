# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:07:56 2019

@author: Jeanette
"""

from variables_Global import VarGlobals as varG
from out_RecircInfo import PrepRecirc as riPrep

sql_outPRID = 0
prev_prDateKey = ""
sqlInsert_PayReimbAll = ""
sqlUpdate_PayReimbList = []
sqlInsert_outPRCnt = 0
sqlUpdate_outPRCnt = 0


class PayReimbSQL:
    
    def setPRGlobals(keyPR):
        global sql_outPRID
        
        sql_outPRID = keyPR       
        print('setPRGlobals sql_outPRID=',sql_outPRID)
        
    
    def createDebitPROutput(payer,reimburser,transID,transDate,transAmount,\
            transDestination):                
        
        global sql_outPRID
        global sqlInsert_PayReimbAll
        
        sql_outPRID = sql_outPRID + 1
        
        sqlInsertPRTuple = (sql_outPRID,str(transDate),str(transAmount),\
            str(transDestination),\
            #str(varG.headerList[0]) + " " + str(varG.headerList[3]),\
            str(payer),str(reimburser),"",str(0.00),'now()')
        
        sqlInsert_PayReimbAll = sqlInsert_PayReimbAll + \
            str(sqlInsertPRTuple) + ","
            
        
        return sqlInsertPRTuple
       
                
        
    def createCreditPROutput(payer,reimburser,k_date,kv_amount,sql_PRID): 
        
        global sqlInsert_PayReimbAll
        global sqlInsert_outPRCnt
        global sql_outPRID
        
        sql_outPRID = sql_PRID
        
        sqlInsertPRTuple = (sql_outPRID,str(k_date),str(kv_amount), \
            str(varG.headerList[3]),str(payer),str(reimburser),"",\
            str(0.00),'now()')
        
        varG.studyOutList.append('createCreditPROutput: sqlInsertPRTuple=' + \
            str(sqlInsertPRTuple))
            
        sqlInsert_PayReimbAll = sqlInsert_PayReimbAll + \
            str(sqlInsertPRTuple) + ","
            
        sqlInsert_outPRCnt = sqlInsert_outPRCnt + 1
            
        
        return sqlInsertPRTuple,sql_outPRID

                    

    def createUpdateSQL(prDate,prAmount,prID):
        
        global sqlUpdate_PayReimbList
        global sqlUpdate_outPRCnt

  
        queryStartD = "update " + varG.sql_prTableName + \
            " set P_R_Date_Reimbursed = " \
            + "'" + prDate + "'"
        queryStartA = "update " + varG.sql_prTableName + \
            " set P_R_Amt_Reimbursed = " \
            + str(prAmount)

        queryEnd = "  where P_R_TransID = " + prID + ";"

        queryUpdateD = queryStartD + queryEnd
        queryUpdateA = queryStartA + queryEnd
        
        sqlUpdate_PayReimbList.append(queryUpdateD)
        sqlUpdate_PayReimbList.append(queryUpdateA)
        
        sqlUpdate_outPRCnt = sqlUpdate_outPRCnt + 1



class WritePR:
    
    def write_sqlI_outPayReimb(sql_outPayReimb,sqlI_prDDL_List):
    
        global sqlInsert_PayReimbAll
        global sql_outPRID
        global sqlInsert_outPRCnt
        
        lLimit = len(sqlI_prDDL_List)-3
        for x, y in enumerate(sqlI_prDDL_List):
            if x > lLimit:
                break
            y_line = y + " \n"
            sql_outPayReimb.write(y_line)
               
    
        sqlInsert_PayReimbAll = sqlInsert_PayReimbAll.strip(",") + ";"
        sql_outPayReimb.write(sqlInsert_PayReimbAll)
        
        sql_outPayReimb.write(sqlI_prDDL_List[-2])
        sql_outPayReimb.write(sqlI_prDDL_List[-1])
        
        sql_outPayReimb.close()  
        
        
        varG.studyOutList.append('\n' + 'sql_outPayReimb closed')
        
        varG.studyOutList.append('sql_outPRID=' + str(sql_outPRID))
        
        varG.studyOutList.append('sqlInsert_outPRCnt=' + \
            str(sqlInsert_outPRCnt))
        
        riPrep.updateEOJRecircPRInfo(sql_outPRID)        
        
    
    def write_sqlU_outPayReimb(sql_outUpdatePayReimb,sqlU_prDDL_List):
        
        global sqlUpdate_PayReimbList
        global sqlUpdate_outPRCnt
       
        sqlUpdate_PayReimbAll = ""
        
        
        if sqlUpdate_PayReimbList !="":

            for x,y in enumerate(sqlUpdate_PayReimbList):

                sqlUpdate_PayReimbAll = sqlUpdate_PayReimbAll + y + " "

               
            lLimit = len(sqlU_prDDL_List)
            for x, y in enumerate(sqlU_prDDL_List):
                if x > lLimit:
                    break
                y_line = y + " \n"
                sql_outUpdatePayReimb.write(y_line)
                                       
            sqlUpdate_PayReimbAll = sqlUpdate_PayReimbAll.strip(",")
            sql_outUpdatePayReimb.write(sqlUpdate_PayReimbAll)
                
        
        sql_outUpdatePayReimb.close()
        
        varG.studyOutList.append('\n' + 'sql_outUpdatePayReimb closed')