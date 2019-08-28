# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 10:30:36 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from out_sqlTrans import WriteTrans as wT

class prepIO:
    
    def prep_sql_inPayReimb(self,sql_inPayReimb):
        self.sql_inPayReimb = sql_inPayReimb
   
        sql_iPR_Lines =  self.sql_inPayReimb.read()
        sqlI_prDDL_List = sql_iPR_Lines.split("\n")
        self.sql_inPayReimb.close()
        
        sList = sqlI_prDDL_List[-4].split(" ")
        varG.sql_prTableName = sList[-2]
        varG.sql_prTableName = varG.sql_prTableName.strip("'")        
        
        return sqlI_prDDL_List
    
    
#    def prep_sql_inPayReimbCrCard(self,sql_inPayReimbCrCard,sql_outPayReimbCrCard):
#        self.sql_inPayReimbCrCard = sql_inPayReimbCrCard
#        self.sql_outPayReimbCrCard = sql_outPayReimbCrCard

#        sql_iPRCC_Lines =  self.sql_inPayReimbCrCard.read()
#        sql_iPRCC_List = sql_iPRCC_Lines.split("\n")
#        self.sql_inPayReimbCrCard.close()
        
#        lLimit = len(sql_iPRCC_List)-3
#        for x, y in enumerate(sql_iPRCC_List):
#            if x > lLimit:
#                break
#            self.sql_outPayReimbCrCard.write(y)
#        
#        self.sql_outPayReimbCrCard.close()
#        
#        return sql_iPRCC_List,self.sql_outPayReimbCrCard
        
    
    def prep_sql_inTrans(self,sql_inTrans):
        self.sql_inTrans = sql_inTrans
        
        sql_iT_Lines = self.sql_inTrans.read()
        sqlI_tDDL_List = sql_iT_Lines.split("\n")
        self.sql_inTrans.close()
        
        sList = sqlI_tDDL_List[-4].split(" ")
        varG.sql_transTableName = sList[-2]
        varG.sql_transTableName = varG.sql_transTableName.strip("'")        
               
        return sqlI_tDDL_List
        
    def prep_sql_inUpdateTrans(self,sql_inUpdateTrans):
        self.sql_inUpdateTrans = sql_inUpdateTrans
              
        sql_iUpdteT_Lines = self.sql_inUpdateTrans.read()
        sqlU_tDDL_List = sql_iUpdteT_Lines.split("\n")
        
        self.sql_inUpdateTrans.close()
             
        return sqlU_tDDL_List
    
        
    def prep_sql_inUpdatePayReimb(self,sql_inUpdatePayReimb):
        self.sql_inUpdatePayReimb = sql_inUpdatePayReimb
        
        iUPR = self.sql_inUpdatePayReimb.read()
        sqlU_prDDL_List = iUPR.split("\n")
        self.sql_inUpdatePayReimb.close()        
        
        return sqlU_prDDL_List
    
    
    def prep_inTrans(self,inTrans):
        self.inTrans = inTrans
               
        inT = self.inTrans.read()
        
        iT_Lines = inT.split('\n')
        
        self.inTrans.close()
        
        return iT_Lines
    
    def prep_inT_Helpers(self,inT_Helpers):
        self.inT_Helpers = inT_Helpers
        
        iTH_List = []
        inTHelpers = self.inT_Helpers.read()
        iTH_List = inTHelpers.split("\n")
        self.inT_Helpers.close()
        
        inTHelpersList = []
        inTHelpersDict = {}
        inTHelpersCatDict_HP = {}
        inTHelpersCatDict = {}
        inTHelpersPayReimbDict = {}
        

        hList = []
        hCnt = 1
        save_ListZero = ""
        saveCredit_ListZero = ""
        for helper in iTH_List:
            #print("helper=",helper)
			
            if hCnt == 1:
                inTHelpersList = helper.split(",")
                #print("inTHelpersList=",inTHelpersList)
                saveCredit_ListZero = inTHelpersList[0]
                hCnt = hCnt + 1
                continue
            elif hCnt > 1:
                hList = helper.split(':')
                if hList[0] == "cat" and hList[1] == "category" \
                        or  hList[0] == "pay" and hList[1] == "reimburse":
                            save_ListZero = hList[0] + ":" + hList[1]
		
                lCnt = len(hList)
                #print("hList=",hList," lCnt=",lCnt)
                if lCnt < 2:
                    break
                #print("\t"," hCnt=",hCnt," save_ListZero=", \
                #      save_ListZero)
                
                if saveCredit_ListZero != "credit:card":
                    for x, y in enumerate(hList):
                        #print("lCnt=",lCnt," x=", x," y=",y, "x % 2 =",x % 2 )
                        if x % 2 == 0:
                            yList = hList[x+1].split(",")
                            if hCnt == 2:
                                inTHelpersDict[y] = yList
                            elif hCnt > 2 and hCnt < 6:
                                inTHelpersCatDict_HP[y] = yList
                            elif hCnt > 5:
                                inTHelpersCatDict[y] = yList
                else:	
                    #print("\n","\n","intHelperPayReimbDict: save_ListZero =",
                    #save_ListZero ,"\n")
                    for x, y in enumerate(hList):
                        #print("lCnt=",lCnt," x=", x," y=",y, "x % 2 =",x % 2 )

                        if x % 2 == 0:
                            yList = hList[x+1].split(",")
                            if save_ListZero == "cat:category": 
                                inTHelpersCatDict[y] = yList
                            elif save_ListZero == "pay:reimburse":
                                inTHelpersPayReimbDict[y] = yList

            hCnt = hCnt + 1
        
        #print(inTHelpersDict)
        
        #print('\n','prepIO: inTHelpersList=',inTHelpersList)
        #print('\n','prepIO: inTHelpersDict=',inTHelpersDict)
        #print('\n','prepIO: inTHelpersCatDict_HP=',inTHelpersCatDict_HP)
        #print('\n','prepIO: inTHelpersCatDict=',inTHelpersCatDict)
        #print('\n','prepIO: inTHelpersPayReimbDict=',inTHelpersPayReimbDict)
        
        varG.inTHelpersList = inTHelpersList
        varG.inTHelpersDict = inTHelpersDict
        varG.inTHelpersCatDict_HP = inTHelpersCatDict_HP
        varG.inTHelpersCatDict = inTHelpersCatDict
        varG.inTHelpersPayReimbDict = inTHelpersPayReimbDict
        
        return inTHelpersList,inTHelpersDict,inTHelpersCatDict_HP, \
            inTHelpersCatDict,inTHelpersPayReimbDict
            
           
    def prep_recircInfo(self,recircInfo):
        self.recircInfo = recircInfo
        
        recircInfo_Lines = self.recircInfo.read()
        self.recircInfo.close()
        

        #inRecircPR_D_KeyList = []
		
        yKey = ""
        rI_List = []

        #print("\n","varG.recircInfoDict=",varG.recircInfoDict)
        rI_List = recircInfo_Lines.split('\n')
        for l,v in enumerate(rI_List):
            hList = v.split(":")
            #print("\n","hList=",hList)
            lCnt = 0
            for x, y in enumerate(hList):
                #print("lCnt=",lCnt," x=", x," y=",y, "x % 2 =",x % 2, \
                #      " yKey=",yKey," hList[x]=",hList[x])
                if x % 2 == 0:
                    yKey = hList[x]
                    #inRecircPR_D_KeyList.append(yKey)
                    lCnt = lCnt + 1
                else:
                    yList = y.split(",")
                    varG.recircInfoDict[yKey] = yList
                    #print("\t","varG.recircInfoDict=",varG.recircInfoDict,"\n","yKey=",yKey," yList=",yList, \
                    #      " varG.recircInfoDict[yKey]=",varG.recircInfoDict[yKey])
    
    
        print("Start: varG.varG.recircInfoDict=",varG.recircInfoDict)
        	        


class Main(object):
     
     def __init__(self,sql_inPayReimb,sql_inPayReimbCrCard, \
            sql_inTrans,sql_inUpdateTrans,sql_inUpdatePayReimb, \
            inTrans,inT_Helpers,recircInfo):
#sql_outPayReimbCrCard,      
        self.sql_inPayReimb = sql_inPayReimb
        self.sql_inPayReimbCrCard = sql_inPayReimbCrCard
        self.sql_inTrans = sql_inTrans
        self.sql_inUpdateTrans = sql_inUpdateTrans
        self.sql_inUpdatePayReimb = sql_inUpdatePayReimb
        
        self.inTrans = inTrans
        self.inT_Helpers = inT_Helpers
        self.recircInfo = recircInfo
        
        
        self.sqlI_prDDL_List = []
        self.sql_iPRCC_List = []
        self.sqlI_tDDL_List = []
        self.sqlU_tDDL_List = []
        self.sqlU_prDDL_List = []
        self.iT_Lines = ""
        
        self.inTHelpersList = []
        self.inTHelpersDict = {}
        self.inTHelpersCatDict_HP = {}
        self.inTHelpersCatDict = {}
        self.inTHelpersPayReimbDict = {}
             
        pIO = prepIO()
        self.sqlI_prDDL_List \
            = pIO.prep_sql_inPayReimb(self.sql_inPayReimb)
        #print(self.sqlI_prDDL_List)
        
#        self.sql_iPRCC_List,self.sql_outPayReimbCrCard \
#            = pIO.prep_sql_inPayReimbCrCard(self.sql_inPayReimbCrCard, \
#                self.sql_outPayReimbCrCard)
        
        #print(self.sql_iPRCC_List)
        
        self.sqlI_tDDL_List \
            = pIO.prep_sql_inTrans(self.sql_inTrans)
        
        self.sqlU_tDDL_List \
            = pIO.prep_sql_inUpdateTrans(self.sql_inUpdateTrans)
        
        self.sqlU_prDDL_List \
            = pIO.prep_sql_inUpdatePayReimb(self.sql_inUpdatePayReimb)
        
        self.iT_Lines = pIO.prep_inTrans(self.inTrans)
        
        self.inTHelpersList,self.inTHelpersDict,self.inTHelpersCatDict_HP, \
            self.inTHelpersCatDict,self.inTHelpersPayReimbDict \
            = pIO.prep_inT_Helpers(self.inT_Helpers)

        
        pIO.prep_recircInfo(self.recircInfo)
            
        #print('io_Prep=',self.inTHelpersDict)
        


