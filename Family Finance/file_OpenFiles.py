# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:47:07 2019

@author: Jeanette
"""


class InputOutput(object):
    def __init__(self,nameList):
        
        self.nameList = nameList

    #-->input files        
        #sql A list:
        name_sql_inPayReimb = self.nameList[0]
        
        self.sql_inPayReimb = open(name_sql_inPayReimb, "r")
        
        #sql B list:
        name_sql_inTrans = nameList[1]
        self.sql_inTrans = open(name_sql_inTrans, "r")        
            
        #sql C list:
        name_sql_updateTrans = nameList[2]
        name_sql_updatePayReimb = nameList[3]

        
        self.sql_inUpdateTrans = open(name_sql_updateTrans,'r') 
        self.sql_inUpdatePayReimb = open(name_sql_updatePayReimb,'r')
        
      #->Driver file  source file downloaded from online accounts 
      #               with initial prep (column allignment) in Excel
        name_inTrans = self.nameList[4]
        self.inTrans = open(name_inTrans, "r")
        
        #Helper files
        name_inT_Helpers = self.nameList[5]
        name_recircInfo = self.nameList[6]
        
        self.inT_Helpers = open(name_inT_Helpers, "r")
        self.recircInfo = open(name_recircInfo, "r") 
    
    
    #-->output files 
        #sql A list:
        name_sql_outPayReimb = self.nameList[7]     
        
        self.sql_outPayReimb = open(name_sql_outPayReimb, "w")

        
        #sql B list:
        name_sql_outTrans = self.nameList[8]  
        
        self.sql_outTrans = open(name_sql_outTrans, "w")
       
        #sql C List
        name_sql_updateTrans = self.nameList[9]
        name_sql_updatePayReimb = self.nameList[10]
        
        self.sql_outUpdateTrans = open(name_sql_updateTrans, "w")
        self.sql_outUpdatePayReimb = open(name_sql_updatePayReimb, "w")      
  
    #non sql
        name_recircOutInfo = self.nameList[11]      
        name_transStudy = self.nameList[12]      
        name_transAnalysis = self.nameList[13]
        
        self.recircOutInfo = open(name_recircOutInfo, "w")      
        self.transStudy = open(name_transStudy, "w")      
        self.transAnalysis = open(name_transAnalysis, "w")
                          
