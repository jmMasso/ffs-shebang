# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:09:03 2019

@author: Jeanette
"""

from variables_Global import VarGlobals as varG
from out_sqlPayReimb import PayReimbSQL as prSQL
from out_sqlTrans import TransSQL as tSQL
from out_RecircInfo import PrepRecirc as riPrep
from trans_UniversalETL import Universal as uETL

#from decimal import Decimal
import calendar



sql_outPRID = 0
prev_prDateKey = ""
sqlUpdate_PayReimbList = []

creditPRList = []

creditPRDict = {}


#print('start: sql_outPRID=',sql_outPRID)


class PayReimb:
    

#--> the following method determines if a payment/charge transaction 
#       requires reimbursement from originator
    def setPRGlobals(keyPR):
        global sql_outPRID
        
        sql_outPRID = keyPR       
        print('setPRGlobals sql_outPRID=',sql_outPRID)
    
    def determinePayReimb \
        (transSource,transCategory,transDescription,transDate):
        #print('determinePayReimb: sql_outPRID=',sql_outPRID)
        global sql_outPRID
        
        yesPayer = False
        yesReimburser = False
        payer = ""
        reimburser = ""
        
        
        if varG.headerList[2] == 'Credit':
            payer, reimburser, yesPayer = \
                uETL.getPayerAttributes(transSource,transDate)
            if yesPayer == True:
                transDescription = "pay for:  " + payer \
                    + "  and  reimburse to:  " + reimburser
        else:
            fP1 = transCategory.find("pay for")
            fP2 = transDescription.find("up jm savings")
            fP3 = transCategory.find("reimbursement")
            if fP1 >= 0 or fP2 >= 0:
                yesPayer = True
                payer = varG.headerList[0] + varG.headerList[3]
                listTC = transCategory.split(" ")
                reimburser = listTC[-1]
            elif fP3 >= 0:
                yesReimburser = True
                
        #if yesPayer == True:
            #print('determinePayReimb: payer=',payer,'reimburser=',\
            #      reimburser,'sql_outPRID=',sql_outPRID,\
            #      'yesPayer=',yesPayer,'payer=',payer,'reimburser=',\
            #      reimburser,'transSource=',transSource,'transDescription=',\
            #      transDescription)
            
        return yesPayer, yesReimburser, payer, reimburser, transDescription
            
             		
#--> the below method creates sql insert tuple for the payReimburse table
#       stored within mySQL Family Finance database.
#--> dictionary, recircInfoDict contains all reimburement info by transaction
#       contained on the table for payReimb and payReimbCrCard.  It is updated
#       to: a) include new insert PR rows  and b) include reimbursement amount
#       and date for existing PR rows which then used to determine which table
#       PR row requires an sql update indicating reimbursement
               
    def sql_outPayReimb(yesPayer,yesReimburser,payer,reimburser,\
        sqlInsert_TransTuple):
        
        
        global sql_outPRID       
        global prev_prDateKey
        global creditPRList
        global creditPRKeyDict

                
        transID = sqlInsert_TransTuple[0]
        transDate = sqlInsert_TransTuple[1]
        transAmount = sqlInsert_TransTuple[2]
        transSource = sqlInsert_TransTuple[4]
        transDestination = sqlInsert_TransTuple[5]
        transDescription = sqlInsert_TransTuple[6]
        
        
     
        transPayReimb_ID = 0
        
		
# output for payReimbrCrCard  --> header type equals Credit   -  additional
#     output when transaction file is for banks: providing credit purchase 
#     payment with monthly billing of credit account - 
        
        if varG.headerList[2] == 'Credit':
            
            if yesPayer == True:
                
                thisPayer = Payer()               
                thisPayer.creditPROutput (payer,reimburser,\
                    sqlInsert_TransTuple) 
                    
                      
            if yesReimburser == True:
                
                thisReimburser = Reimburser()
                thisReimburser.setPayReimbAttributes(payer,reimburser,transID,\
                    transDate,transAmount,transDescription,transSource)
                
                                  
        elif varG.headerList[2] == 'Debit':
            
            if yesPayer == True:
                
                thisPayer = Payer()               
                thisPayer.debitPROutput (payer,reimburser,transID,\
                    transDate,transAmount,transDestination)
                                                                
            if yesReimburser == True:
                
                thisReimburser = Reimburser()
                thisReimburser.setPayReimbAttributes(payer,reimburser,transID,\
                    transDate,transAmount,transDescription,transSource)
                    

        return transPayReimb_ID
             
    
    def creditPRPostTransaction():
        
        global prev_prDateKey
        global sql_outPRID
        
        if prev_prDateKey != '':
            crOut = CreditOutput()
            crOut.createCreditPayReimbSQL()  #create PR tuple(s) for last month        
                                             #stored in creditPRDict
        else:
            print("creditPRPostTransaction","sql_outPRID=", sql_outPRID)
        
            
class Payer:
          
    
    def creditPROutput (self,payer,reimburser,sqlInsert_TransTuple):
                    
        global sql_outPRID       
        global prev_prDateKey
        global creditPRList        
        global creditPRDict
                                
        
        self.payer = payer 
        self.reimburser = reimburser 
        self.sqlInsert_TransTuple = sqlInsert_TransTuple
	

#sqlInsert_TransTuple
# [0] = sql_outTransID, [1] = transDate, [2] = transAmount, [3] = transAction, 
# [4] = transSource [5] transDestination [6] = transDescription [7] transCategory 
# [8] varG.headerList[0] [9] transLocation [10] varG.headerList[0]) [11] reimburse amount
# [12] 'now()'
        
#        
#creditPRTuple
# [0] = sql_outTransID, [1] = trans date, [3] = transAmount, [5] payer
# [6] = reimburser 
        
#creditPRDict = {payer/reimburser:[sql_outTransID,transAmount]}

		
# --> 1) Update Credit PayReimburse tuple holding list for yyyymm
# --> 2) Create sql insert tuple from summarized tuple holding list when change in yyyymm 
        
#   set up yyyymm key
        dte_List = []
        dte_List = self.sqlInsert_TransTuple[1].split("/")	
        prDateKey = dte_List[0] + dte_List[1]

        prDictTuple = (self.sqlInsert_TransTuple[0],\
            self.sqlInsert_TransTuple[2])
        prDictKey = self.payer + "/" + self.reimburser             
        
#   determine actions based on previous current key values
        
        if prev_prDateKey == "":          #key = yyyymm

            creditPRList.append(prDictTuple)
            creditPRDict[prDictKey] = creditPRList
            creditPRList = []          	
        elif prDateKey == prev_prDateKey:
            if prDictKey in creditPRDict:
                creditPRList = creditPRDict[prDictKey]
            creditPRList.append(prDictTuple)
            creditPRDict[prDictKey] = creditPRList
            creditPRList = []
        else:                             #change in month or year
            print("creditPROutput"," prev_prDateKey=",prev_prDateKey)
            crOut = CreditOutput()
            crOut.createCreditPayReimbSQL()  #create PR tuple(s) for month end
                                          #from data stored in creditPRDict          
            creditPRList = []
            creditPRDict ={}
            creditPRList.append(prDictTuple)
            creditPRDict[prDictKey] = creditPRList
            creditPRList = []

        prev_prDateKey = prDateKey
        
        
    def debitPROutput (self,payer,reimburser,transID,transDate,transAmount,\
        transDestination):
        
        self.payer = payer
        self.reimburser = reimburser
        self.transID = transID
        self.transDate = transDate
        self.transAmount = transAmount
        self.transDestination = transDestination
        
        
        sqlInsertPRTuple \
            = prSQL.createDebitPROutput(self.payer,self.reimburser,\
            self.transID,self.transDate,self.transAmount,\
            self.transDestination)
        
        sql_outPRID = sqlInsertPRTuple[0]                       
        tSQL.sqlUpdate_TransPayReimbID(transID,sql_outPRID)
        riPrep.insertRecircPRInfo(sqlInsertPRTuple)
          
                                    
        
class Reimburser:
    
    def setPayReimbAttributes(self,payer,reimburser,transID,transDate,transAmount,\
        transDescription,transSource):
                                                                                                                               	
        global sqlUpdate_PayReimbList
					
        self.payer = payer
        self.reimburser = reimburser
        self.transID = transID
        self.transDate = transDate
        self.transAmount = transAmount
        self.transDescription = transDescription
        self.transSource = transSource
        
        hdrOwner = varG.headerList[0]
        hdrAccount = varG.headerList[3]
    
        transPayReimb_ID = ""
        
        prKeyList = []

        listPayReimbDestinations = ["visa","amazon"," dell ","paypal"]
        fPvalue = ""
        transPayReimb_ID = ""
    
        hdrAccountID = hdrOwner + " " + hdrAccount
        prKey = str(self.transAmount) + "*" +  hdrAccountID
        #print("\t","\t","prKey=",prKey)
                
        transAmt = self.transAmount
        for prKey in varG.recircInfoDict:
            prKeyL = prKey.split('*')
            if len(prKeyL) == 3:
                prKLAmt = prKeyL[1]
                prKListAmt = varG.recircInfoDict[prKey][4]
                if prKLAmt == prKListAmt:
                    continue
                else:
                    fP1 = prKeyL[2].find(payer)
                    if fP1 == -1:
                        continue
                    else:   
                        if varG.recircInfoDict[prKey][2] != reimburser:
                            continue
                        else:
                            prKListAmt, transAmt
                            prU = Utility()
                            prU.apply_Reimbursement(prKLAmt,prKListAmt,\
                                transAmount) 
                                                      
                            prKListAmt = "%.2f" %prKListAmt
                            riPrep.updateRecircPRInfo(prKey,self.transDate,
                                prKListAmt)
                            
                            prSQL.createUpdateSQL(self.transDate,\
                                varG.recircInfoDict[prKey][4],\
                                varG.recircInfoDict[prKey][0])
                            
                            transPayReimb_ID = transPayReimb_ID + \
                                "," + varG.recircInfoDict[prKey][0]
                            if transAmt != 0:
                                continue
                            else:
                                tSQL.sqlUpdate_TransPayReimbID(transID,\
                                    transPayReimb_ID)                                
                                break
        
    

class CreditOutput:
    
    def createCreditPayReimbSQL(self):
        
        global sql_outPRID       
        global prev_prDateKey
        global creditPRList
        global creditPRDict
                
        dict_sum = {}
        k_date = ""
        
        
        k_yr = prev_prDateKey[:4]
        k_mth = prev_prDateKey[4:]
        print("\n", "\t","prev_prDateKey=", prev_prDateKey, " k_yr=", k_yr, " k_mth=", k_mth)
        k_day = calendar.monthrange(int(k_yr),int(k_mth))[1]
        k_date = str(k_yr) + "/" + str(k_mth) + "/" + str(k_day)
        kv_amount = 0.00
        
        varG.studyOutList.append('createCreditPayReimbSQL-0:  sql_outPRID=' + \
                str(sql_outPRID) + ' k_date=' + k_date)
        
        for key in creditPRDict:
            kPRList = key.split('/')
            kPRList = creditPRDict[key]
            
            sql_outPRID = sql_outPRID + 1
            
            varG.studyOutList.append('createCreditPayReimbSQL-1:  sql_outPRID=' + \
                str(sql_outPRID) + '\n' + '\t' + ' key='+ key + ' kPRList= ' + str(kPRList) + '\n')
        
            for x, y in enumerate(kPRList):
                transID = y[0]
                tSQL.sqlUpdate_TransPayReimbID(transID,sql_outPRID)
                l_amount = float(y[1])
                ds_key = key
                varG.studyOutList.append('\n' + 'createCreditPayReimbSQL-2a:  sql_outPRID=' + \
                    str(sql_outPRID) + '\n' + '\t' + ' ds_key=' + key + \
                    ' l_amount=' + str(l_amount) + ' dict_sum= ' + str(dict_sum) + '\n')
                if ds_key in dict_sum:
                    kv_amount = dict_sum[ds_key][0]
                    kv_amount = float(kv_amount) + float(l_amount)
                    dict_sum[ds_key][0] = kv_amount
                else:	
                    dict_sum[ds_key] = [float(l_amount), sql_outPRID]
                varG.studyOutList.append('createCreditPayReimbSQL-2b:  sql_outPRID=' + \
                    str(sql_outPRID) + '\n' + '\t' + \
                    ' ds_key=' + key + ' dict_sum= ' + str(dict_sum) + '\n' + '\n')

        for key in dict_sum:
            varG.studyOutList.append('\n' + 'createCreditPayReimbSQL-3a:  sql_outPRID=' + \
                str(sql_outPRID) + '\n' + '\t' + \
                ' key=' + key + ' dict_sum= ' + str(dict_sum))
            pr_list = key.split("/")
            payer = pr_list[0]
            reimburser = pr_list[1]
            kv_amount = dict_sum[key][0]
            kv_amount = "%.2f" %kv_amount
            sql_PRID = dict_sum[key][1]
            
            sqlInsertPRTuple,sql_outPRID \
                = prSQL.createCreditPROutput(payer,reimburser,k_date,kv_amount,\
                sql_PRID)
                                        
            riPrep.insertRecircPRInfo(sqlInsertPRTuple)
            
            varG.studyOutList.append('\n' + 'createCreditPayReimbSQL-3b:  sql_PRID=' + \
                str(sql_outPRID) + '\n' + '\t' + \
                ' key=' + key + ' sqlInsertPRTuple= ' + str(sqlInsertPRTuple))
            
                                            

class Utility:
    
    def apply_prReimBursement(self,prKLAmt,prKListAmt,transAmt):
        self.prKLAmt = prKLAmt  
        self.prKListAmt = prKListAmt
        self.transAmt = transAmt
        
        appliedAmt = 0.00
        
        appliedAmt = float(self.prKListAmt) + float(self.transAmt)
        
        if appliedAmt > self.prKLAmt:
            self.prKListAmt = float(self.prKLAmt)
            self.transAmt = float(appliedAmt) - float(self.prKLAmt)
        else:
            self.prKListAmt = float(appliedAmt)
            self.transAmt = 0.00            
            
            
        return self.prKListAmt, self.transAmt

            
            
            