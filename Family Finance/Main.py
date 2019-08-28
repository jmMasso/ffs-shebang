# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:40:50 2019

@author: Jeanette
"""
from file_NameParameters import Parameters
from file_CreateFileNames import fileNames
from file_OpenFiles import InputOutput 
from file_ProcessPrep import Main
from file_ProcessTransIn import Transaction
from output_FFS import OutputWrite



#update per Run

runPath = "C:/Users/Jeanette/Documents/Finance/Family Finance System/File IO/"

runDictKey = '3'               #see below for value   values '1', '2' or '3'

#runDictKey = 
#   {'1':{'sql':('1','1'),'recirc':'0','output1':'r#','output2':'rOA#'},
#    '2':{'sql':('2','2'),'recirc':'r#-1','output1':'r#','output2':'rOA#'}, 
#    '3':{'sql':('2','1'),'recirc':'r#-1','output1':'r#','output2':'rOA#'}}        
#
#        'sql':('1','1') = 'sql:(A group sql files, B group sql files)
#                        = '1' equals create-insert  sql ddl
#                        = '2' equals insert sql ddl
#        A group sql files:  PayReimb
#        B group sql files:  owner/account Trans
#        output1 = is for PayReimb and Recirc
#        output2 = all trans files that are at the owner and account level
        
runNumber = '4'            #incremented by 1 per run:  last run number: 2
runOAnumber = '1'          #increment by 1 per Owner/Account run
                           # Jeanette: CrCard-2    Checking-     Savings-  
                           # JMmom:  Checking-      Savings-
                           # ASmom:  Checking-      Savings-
                           # Julia:  Checking-      Savings-
runYear = '2017'            #'2016-18', '2018', '2019'
runRange = '05-12'          #'01-12' , '01-03', '04-06', '07-09', '10-12'
runType = 'Debit'          #'Credit', 'Debit'
runOwner = 'JMmom'       #'Jeanette', 'Julia', 'JMmom', 'ASmom'
runAccount = 'Checking'    #'crCard Master', 'crCard Visa', 'Checking', 'Savings'
runPrefix1 = 'FFS'          #'FFS' 
runPrefix2 = 'FFS'          #'FFS'


runList = [runPath,runDictKey,runNumber,runOAnumber,runYear,runRange,runType,runOwner,
           runAccount,runPrefix1,runPrefix2]

nameList = []

mParam = Parameters(runList)
    
mNames = fileNames(mParam.runList) 

mIOF = InputOutput(mNames.nameList)

mIOFPrep = Main(mIOF.sql_inPayReimb,mIOF,mIOF.sql_inTrans,
            mIOF.sql_inUpdateTrans,mIOF.sql_inUpdatePayReimb,
            mIOF.inTrans,mIOF.inT_Helpers,mIOF.recircInfo)

mTrans = Transaction(mIOFPrep.iT_Lines)

mWrite = OutputWrite.writeOutFiles(mIOF.sql_outTrans,mIOFPrep.sqlI_tDDL_List,
            mIOF.sql_outPayReimb,mIOFPrep.sqlI_prDDL_List,
            mIOF.sql_outUpdateTrans,mIOFPrep.sqlU_tDDL_List,
            mIOF.sql_outUpdatePayReimb,mIOFPrep.sqlU_prDDL_List,
            mIOF.recircOutInfo,mIOF.transStudy,mIOF.transAnalysis)