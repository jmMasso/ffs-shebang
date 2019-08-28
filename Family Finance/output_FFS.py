# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:34:50 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from out_sqlTrans import TransSQL as tSQL
from payReimb_Prep import PayReimb as oPR 
from out_sqlTrans import WriteTrans as wT
from out_sqlPayReimb import WritePR as wPR
from out_tranSandA import WriteSA as wSA
from out_RecircInfo import WriteRI as wRI
#from sqlPayReimb import PayReimb as sPR

class OutputPrep:
    
#    def prep_Initial():
#        global 
    
    
    def prepDriver(transDate,transAmount,\
        transLocation,transAction,transSource,\
        transDestination,transDescription,\
        transCategory,sql_outTransID):

        #print('FFS-1: varG.recircInfoDict=',varG.recircInfoDict)
#   -->1) Check if transaction attributes require corresponding
#         payReimbursement record keeping via mySQL
        
        yesPayer, yesReimburser, payer, reimburser, transDescription \
            = oPR.determinePayReimb(transSource,transCategory,\
            transDescription,transDate)
            

#   sql insert outTrans files:

#   -->2) Create tuple for mySQL  insert out Trans file         
        #print('FFS-2: varG.recircInfoDict=',varG.recircInfoDict)       
        sqlInsert_TransTuple \
            = tSQL.sqlInsert_OutTransTuples(yesPayer,\
            yesReimburser,payer,reimburser,\
            transDate,transAmount,transAction,transSource,transDestination,\
            transDescription,transCategory,transLocation)
                   

#   sql insert/update Pay Reimburse out files and update out Trans file
        
#   -->2) yesPayer indicates attributes matched stored attributes indicating 
#           transOwner made payment for another person requiring reimbursement 
#         yesReimburser indicates that a reimbursement payment was made and an
#           sql update Pay Reimburse statement creation is required     

        #print('FFS-3: varG.recircInfoDict=',varG.recircInfoDict)
        if yesPayer == True or yesReimburser == True: 

#   -->3) sql_outPayReimb method will create sqlInsert PR tuples, sqlUpdate Out Trans
#         strings and varG.recircInfoDict key/value inserts and updates - global
#         variables are used to store PR variables                     

            oPR.sql_outPayReimb(yesPayer,yesReimburser,payer,reimburser,\
                sqlInsert_TransTuple)
                
        #print('FFS-4: varG.recircInfoDict=',varG.recircInfoDict)    

    
    def postTransaction():
        
        if varG.headerList[2] == "Credit":
            oPR.creditPRPostTransaction()
                                          
    
class OutputWrite:
    
    def writeOutFiles(sql_outTrans,sqlI_tDDL_List,
            sql_outPayReimb,sqlI_prDDL_List,
            sql_outUpdateTrans,sqlU_tDDL_List,
            sql_outUpdatePayReimb,sqlU_prDDL_List,
            recircOutInfo,transStudy,transAnalysis):
       
        wT.write_sqlI_outTrans(sql_outTrans,sqlI_tDDL_List)
        wT.write_sqlU_outTrans(sql_outUpdateTrans,sqlU_tDDL_List)
        
        wPR.write_sqlI_outPayReimb(sql_outPayReimb,sqlI_prDDL_List)        
        wPR.write_sqlU_outPayReimb(sql_outUpdatePayReimb,sqlU_prDDL_List)
        
        wRI.write_recircInfo(recircOutInfo)
        
        wSA.write_TransAnalysis(transAnalysis)
        wSA.write_TransStudy(transStudy)       
              
                                                      
#class OutputEnd:
         
        