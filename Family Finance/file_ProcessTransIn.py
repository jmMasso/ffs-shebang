# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 20:28:13 2019

@author: Jeanette
"""

from variables_Global import VarGlobals as varG
from trans_Transformation import Date
from trans_Transformation import Amount
from trans_Transformation import Location
from trans_Transformation import Descriptors
from output_FFS import OutputPrep as opP
from payReimb_Prep import PayReimb as prP
from out_sqlPayReimb import PayReimbSQL as prSQL
from out_sqlTrans import TransSQL as tSQL
#from acct_Transform import Account
from trans_UniversalETL import Universal as uETL


class Transaction(object):
    def __init__(self,iT_Lines):
        
        self.iT_Lines = iT_Lines
                        
        fields = []
            
        datePrevious = ""
        prevDate_Set = False
                 
#TransAnalysis setup variables        
        descriptionTuple = ()
        descriptionSet = set()
      
        
#for loop iterates through variable lines that contains all input file data by lines
        for line in self.iT_Lines:
            #break
            description = ""
            descriptionList = []
    
            if line == " ":
                break

            if line == '"':
                continue

            
            fields = line.split("\t")   #date, amount, payee          
             			
            if fields[0] == "" or fields[0] == '"':
                continue

#setUp headerList and starting sqlIDs via trans line with owner in fields[0]            
            if str.isalpha(fields[0]):     #header record   
                
                varG.headerList = fields
                #hdrOwner = [0]   #
                #hdrSource = [1]
                #hdrType = [2]  #Debit   or   Credit
                #hdrAccount = [3]  #Checking, Savings, Bank Card, Online Account
                
                #hdrAccountID = varG.headerList[0] + "-" + varG.headerList[1] \
                #    + "-" + varG.headerList[2] + "-" + varG.headerList[3]
                    
                varG.studyOutList.append('\n'+ 'owner=' + varG.headerList[0] + 
                     ' source=' + varG.headerList[1] + ' type=' +
                     varG.headerList[2] + ' account=' + varG.headerList[3])
                
                sql_outPRID = int(varG.recircInfoDict[varG.prRIKey][0])
                
                if varG.headerList[2] == "Credit":
                    prP.setPRGlobals(sql_outPRID)
                    
                    varG.tRIKey = varG.headerList[0] + '/' + varG.headerList[2]              
                    
                    if varG.headerList[3] == 'Master Card':
                        varG.tRILastRunLine = \
                             varG.recircInfoDict[varG.tRIKey][1]
                    
                    elif varG.headerList[3] == 'Visa Card':
                        varG.tRILastRunLine = \
                            varG.recircInfoDict[varG.tRIKey][2]

                else:
                    prSQL.setPRGlobals(sql_outPRID)
                    print('varG.headerList=', varG.headerList)
                    varG.tRIKey = varG.headerList[0] + '/' + varG.headerList[3]
                    varG.tRILastRunLine = varG.recircInfoDict[varG.tRIKey][1]                   
                                        
                sql_outTransID = int(varG.recircInfoDict[varG.tRIKey][0])                                                
                tSQL.setOTGlobals(sql_outTransID)
                
                                
                varG.studyOutList.append('\n' + 'tRILastRunLine=' + 
                     varG.tRILastRunLine)
                                                
                varG.studyOutList.append('\n'+ 'sql_outTransID=' + 
                     str(sql_outTransID))
                                                
                varG.studyOutList.append('\n'+ 'sql_outPRID=' + 
                     str(sql_outPRID) + '\n')

                                                
                continue
            
            
            date = fields[0]                 
            
#date:  transform date into yyyy/mm/dd  format with leading zeros for mm and dd
            ttDate = Date(date) 
            transDate = ttDate.dateYearFirst
            

#ensure trans line not previously loaded

            fields[0] = transDate
            p1 = 'all'
            p2 = 0
            p4 = 0
            chkLine = uETL.extractFromList(fields,p1,p2,p4)
            riLineL = varG.tRILastRunLine.split(' ')

            

            if fields[0] < riLineL[0]: #and fields[1] > riLineL[1]:
                print("\n",\
                  "****trans line already processed****",\
                  "\n","\t","  current=",fields[0],"\t",fields[1],\
                      "\t",fields[2],
                  "\n","\t"," previous=",riLineL[0],"\t",riLineL[1],
                  "\t",riLineL[2])
                continue
            elif chkLine == varG.tRILastRunLine:
                print("\n","\n",\
                  "****trans line already processed****",\
                  "\n","\t","  current=",chkLine,"\n","\t",\
                  " previous=",varG.tRILastRunLine)
                continue
            else:
                varG.tRILastRunLine = chkLine
                                  		
            #datePrevious = transDate
            
#amount: 
            
#    validation 
            if fields[1] == "":    
                continue
            
            amount = fields[1]
            
#     transformation 			
            
            ttAmt = Amount(amount)
            transAmount = ttAmt.amount
            
            #print('\n','transAmount=',transAmount)

#description:
            description = fields[2]
                        
#add descriptionTuple to analysisOutSet
            descriptionTuple = description
            varG.analysisOutSet.add(descriptionTuple)


#Location extract from description
            description = description.strip('"')
            description = description.rstrip()
            descriptionList = description.split(" ")
            #descriptionList = list(filter(None, descriptionList))
            #print("description=",description)
            #print("descriptionList=",descriptionList)
            
            ttLoc = Location(description,descriptionList)
                
            
            transLocation = ttLoc.transLocation
            description = ttLoc.description
            descriptionList = ttLoc.descriptionList
            
            descriptionList = list(filter(None, descriptionList))
            

#???
#cleanse the description before creating descriptionList
#            if descriptionList == prev_DescriptionList:
#                payee = prev_payee
#            else:	
#            description = UniversalB.cleanseDescription(description)
#                
#            prev_DescriptionList = descriptionList
           
            
#Descriptors extract from description and transform
            #transAction, transSource, transDestination, transDescription \
            
            ttDesc = Descriptors(description,descriptionList,\
                transDate,transAmount,transLocation,fields)
            
            transAction = ttDesc.transAction
            transSource = ttDesc.transSource
            transDestination = ttDesc.transDestination
            transDescription = ttDesc.transDescription
            transCategory = ttDesc.transCategory
            
                            
            opP.prepDriver(transDate,transAmount,\
                transLocation,transAction,transSource,\
                transDestination,transDescription,\
                transCategory,sql_outTransID)


            
        opP.postTransaction()   

            
            
            
            
            
            
            
            
            