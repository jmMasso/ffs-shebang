# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 20:00:42 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG

class fileNames(object):
    def __init__(self,runList):
        self.runList = runList
 
#->variable prep:       
        
#-->unload runList assigned by System Administrator in Main.py  and  
#       configured by run_Parameters.py
        
        runPath = self.runList[0]
        runYear = self.runList[4]
        runRange = self.runList[5]
        runType = self.runList[6]
        runOwner = self.runList[7]
        runAccount = self.runList[8]
        runPrefix1 = self.runList[9] 
        runPrefix2 = self.runList[10]
        runSfxinSQLA = self.runList[11]
        runSfxinSQLB = self.runList[12]
        runSfxinRecirc = self.runList[13]
        runSfxoutSQLA = self.runList[14]
        runSfxoutSQLB = self.runList[15]
        runSfxoutput1 = self.runList[16]
        runSfxoutput2 = self.runList[17]
        
  
#->establish jmChecking awareness to trigger JMCHKTansform.py usage     
        
        if runOwner == 'Jeanette' and \
            runAccount == 'Checking':
            varG.jmChecking = True
        
#->variable setup process:         
        
        nFile_S = " - "  #separator        
        nFile_SQL = "mySQL"
        
        nFile_DteRng = runYear + "-" + runRange

# --->input trans file prefix - FFS - 2018-01-12        
        
        runPrefix2 = runPrefix1 + nFile_S + runOwner + nFile_S + runAccount
        #runPrefix2 = runPrefix1 + nFile_S + runYear + "-" + runRange
        
        if runType == 'Credit':
            inSQL_Acct = 'crCard'
        else:
            inSQL_Acct = runAccount
        
# --->input sql A,B and C list files
        
        if runSfxinSQLA == '1':
            nFile_SQLA = 'mySQL-create-insert'
        elif runSfxinSQLA == '2':
            nFile_SQLA = 'mySQL-insert'
            
        if runSfxinSQLB == '1':
            nFile_SQLB = 'mySQL-create-insert'
        elif runSfxinSQLB == '2':
            nFile_SQLB = 'mySQL-insert'
            
        nFile_SQLC = 'mySQL-update'
        
#-->add key variable information to studyOutList
        
        varG.studyOutList.append('\n' + 'inSQL_Acct=' + inSQL_Acct + 
             ' nFile_SQLA=' + nFile_SQLA + ' nFile_SQLB=' + nFile_SQLA + 
             ' nFile_SQLC=' + nFile_SQLC)        
        
        
# --->list for all input and output configured file names 
        self.nameList = []


#->create self.nameList = [] process:

#-->Configure File Names using established run and name variable values 

#--->input files:
        
# --->sql A list
        
#  --->account type PayReimb - created by System Administrator with two types
#          of input names:  1) mySQL-create-insert or 2) mySQL-insert                  
            
        name_sql_inPayReimb = runPath + runPrefix1 + nFile_S + nFile_SQLA  \
                + nFile_S + 'PayReimb.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - mySQL-create-insert - PayReimb.txt"
        self.nameList.append(name_sql_inPayReimb)    # [0]                
        
# --->sql B list:
        
#  --->account type Trans - created by System Administrator with two types
#          of input names:  1) mySQL-create-insert or 2) mySQL-insert
                        
        name_sql_inTrans = runPath + runPrefix1 + nFile_S + runOwner + nFile_S \
                + inSQL_Acct + nFile_S + nFile_SQLB + nFile_S + 'Trans.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - Jeanette - Checking - mySQL-create-insert - Trans.txt"
        self.nameList.append(name_sql_inTrans)    # [1]        
        
# --->sql C list:
        
#  --->account type Trans - created by System Administrator with one type
#          of input names:  1) mySQL-update
        
        name_sql_updateTrans = runPath + runPrefix1 + nFile_S + runOwner + nFile_S \
                + inSQL_Acct + nFile_S + nFile_SQLC + nFile_S + 'Trans.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - Jeanette - Checking - mySQL-update - Trans.txt"
        self.nameList.append(name_sql_updateTrans)    # [2]

#  --->account type PayReimb - created by System Administrator with one type
#          of input names:  1) mySQL-update
        
        name_sql_updatePayReimb = runPath + runPrefix1 + nFile_S + nFile_SQLC \
            + nFile_S + 'PayReimb.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - mySQL-update - PayReimb.txt"
        self.nameList.append(name_sql_updatePayReimb)    # [3]
        

# --->non sql files

#  --->owner/account Transaction file - downloaded and name/format prepped by
#          System Administrator    
        
        name_inTrans = runPath + runPrefix2 + nFile_S + nFile_DteRng \
            + nFile_S + 'inTrans.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - 2018-01-12 - Jeanette - Checking - inTrans.txt"
        self.nameList.append(name_inTrans)    # [4]
    
#  --->account type Helper file - updated by System Administrator    
        
        name_inT_Helpers = runPath + runPrefix1 + nFile_S + runType \
                + nFile_S + 'inT_Helpers.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - Credit - inT_Helpers.txt")
        self.nameList.append(name_inT_Helpers)    # [5]
        
#  --->recircInfo - created by System Administrator before first FFS run

        name_recircInfo = runPath + runPrefix1 \
                + nFile_S + 'recircInfo-' + str(runSfxinRecirc) + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - recircPayReimb-1-1-0.txt")     
        self.nameList.append(name_recircInfo)    # [6]
        

#--->output files:
        
# --->sql A list
        
#  --->account type SQL out PayReimb - contains: 1) create and insert SQL 
#          statements  or  2) insert SQL statements.   requires: 1) Removal of
#          "'" within the insert field containing 'now()', 2) copy to the 
#          base mySQL run Script file for the FS_PayReimb table        
               
        name_sql_outPayReimb = runPath + runPrefix1 + nFile_S + nFile_SQL \
                + nFile_S + 'PayReimb-' + runSfxoutSQLA + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - mySQL - PayReimb-1-1-1.txt"
        self.nameList.append(name_sql_outPayReimb)    # [7]
        
        
# --->sql B list:
        
#  --->account type SQL out Trans - contains: 1) create and insert SQL 
#          statements  or  2) insert SQL statements.   requires: 1) Removal of
#          "'" within the insert field containing 'now()', 2) copy to the 
#          base mySQL run Script file for the FS_owner_account_Trans table
        
        name_sql_outTrans = runPath + runPrefix1 + nFile_S + runOwner + nFile_S \
                + inSQL_Acct + nFile_S + nFile_SQL + nFile_S + 'Trans-' \
                + runSfxoutSQLB + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - 2018-01-12 - Jeanette - Checking - mySQL-create-insert - Trans-1-1-1.txt"
        self.nameList.append(name_sql_outTrans)    # [8]
        
        
#  --->account type SQL out updateTrans - contains: 1) update SQL statements
#          2) copy to the base mySQL run Script file for the 
#          FS_owner_account_Trans table
        
        name_sql_updateTrans = runPath + runPrefix1 + nFile_S + runOwner + nFile_S \
                + inSQL_Acct + nFile_S + nFile_SQL + nFile_S + 'updateTrans-' \
                + runSfxoutSQLB + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - 2018-01-12 - Jeanette - Checking - mySQL-update - updateTrans-1-1-1.txt"
        self.nameList.append(name_sql_updateTrans)    # [9]

                
#  --->account type SQL out updatePayReimb - contains: 1) update SQL statements
#          2) copy to the base mySQL run Script file for the 
#          FS_PayReimb table
        
        name_sql_updatePayReimb = runPath + runPrefix1 + nFile_S + nFile_SQL \
                + nFile_S + 'updatePayReimb-' + runSfxoutSQLA + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - mySQL-update - PayReimb-1-1-1.txt"
        self.nameList.append(name_sql_updatePayReimb)       # [10]     
                
        
# --->non sql
        
#  --->recirc file - requires input to the next FFS run obtained through run
#          number indicated in 'Main.py' by System Administrator
        
        name_recircOutInfo = runPath + runPrefix1 + nFile_S \
                + 'recircInfo-' + runSfxoutput1 + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - recircInfo-1.txt")
        self.nameList.append(name_recircOutInfo)    # [11]

#  --->transStudy file - requires review by FFS run study team before 
#          proceeding with next action items by System Administrator         
        
        name_transStudy = runPath + runPrefix2 + nFile_S + nFile_DteRng \
                 + nFile_S + 'transStudy-' + runSfxoutput2 + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - 2018-01-12 - Jeanette - Checking - transStudy-1.txt"
        self.nameList.append(name_transStudy)    # [12]

#  --->transAnalysis file - requires review by FFS run analysis team if run
#          study team deems FFS system code changes           
        
        name_transAnalysis = runPath + runPrefix2 + nFile_S + nFile_DteRng \
                + nFile_S + 'transAnalysis-' + runSfxoutput2 + '.txt'
        #"C:/Users/Jeanette/Downloads/Python/Practice/
        #    FFS - 2018-01-12 - Jeanette - Checking - transAnalysis-1.txt"
        self.nameList.append(name_transAnalysis)    # [13]


#-->add configured file names to studyOutList   
        print("\n","File Names:","\n") 
        for x, y in enumerate(self.nameList):
            varG.studyOutList.append(y + '\n') 
            print("\t",y) 

        