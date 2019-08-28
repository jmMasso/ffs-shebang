# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:00:24 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from trans_DescriptionETL import DebitType as dDB
from trans_UniversalETL import Universal as uETL



hdrSource = ""
hdrOwnerAccount = ""

description = ""
descriptionList = []

transDate = ""
transAmount = 0
transLocation = ""

transAction = ""
transSource = ""
transDestination = ""
transDescription = ""
transCategory = ""

transOwner = ""
transAccount = ""

class Debit:
    
    def setDebitAcctAttributes(in_description,in_descriptionList, \
        in_transDate,in_transAmount,in_transLocation):
        
        global hdrSource
        global hdrOwnerAccount
        
        global description
        global descriptionList

        global transDate
        global transAmount
        global transLocation
        
        global transAction
        global transSource
        global transDestination
        global transDescription
        global transCategory
        
        global transOwner
        global transAccount
         
        hdrSource =  varG.headerList[1]
        hdrOwnerAccount = varG.headerList[0] + " " + varG.headerList[3]
        transOwner  = varG.headerList[0]
        transAccount = varG.headerList[3]
        
        description = in_description.lower()
        descriptionList = in_descriptionList

        transDate = in_transDate
        transAmount = in_transAmount
        transLocation = in_transLocation
        
        transAction = ""
        transSource = ""
        transDestination = ""
        transDescription = ""
        transCategory = ""
        
        
        if varG.headerList[3] == "Checking":
            
            #print("sent sql_outTransID=",sql_outTransID)
            #print("\n","\t","beforeSet: inRecircPR_Dict=",inRecircPR_Dict,\
            #      " transAmount=",transAmount)
			
            dChkg = Checking()
            dChkg.setCheckingAttributes()			

        elif varG.headerList[3] == "Savings":
                       
            #print("sent sql_outTransID=",sql_outTransID)
            #print("\n","\t","beforeSet: inRecircPR_Dict=",inRecircPR_Dict,\
            #      " transAmount=",transAmount)
			
            dSvgs = Savings()	
            dSvgs.setSavingsAttributes()
                
        
        return transAction, transSource, transDestination, transDescription,\
            transCategory
            
            
class Checking:
    
    def setCheckingAttributes(self):                
        global hdrSource
        global hdrOwnerAccount
        
        global description
        global descriptionList

        global transDate
        global transAmount
        global transLocation
        
        global transAction
        global transSource
        global transDestination
        global transDescription
        global transCategory
        
        global transOwner
        global transAccount
                
        lLen = 0
        debitAttributeList = []
        transList = []
        transSource_Destination = ""
        transValue = ""
        
		
        fP1 = 0
        fP2 = 0
        fP3 = 0		
        fP4 = 0
        fP5 = 0
        fP6 = 0
        fP7 = 0
        fP8 = 0
        fDeposit = ""

        p1 = ""
        p2 = 0
        p3 = ""
        p4 = 0
        amt_p1 = ""

        finalByPass = ""
		
#class instantiation        

        outStudy = Study()

#-> set up
#-> description split -->  by  "#" within value if it exists  
#-> creates a List with [0] and [1] if "#"  
        
        debitAttributeList = description.split("#")
	
#-> number of indexes obtained to determine if list is [0][1]  or [0]   
#   based on presence of split character "#"

        lLen = len(debitAttributeList)
		
#-> [0] value converted to list for further interogation and use

        transValue = str(debitAttributeList[0])
        transValue = transValue.rstrip(" ")
        transList = transValue.split(" ")

        varG.studyOutList.append("\n" + "->checking S: transDate=" + \
            transDate + " transAmount=" + str(transAmount) + \
            " description=" + description + \
            " debitAttributeList=" + str(debitAttributeList) + \
            " transValue=" + transValue + " transList=" + str(transList) + \
            "\n")


#-> deposit or withdraw determining factor 
#--> based on first position of transAmount 
#---> "-" value indicates withdraw (N) otherwise deposit

#-> BRANCH --> not Negative ?  ---> Yes --> Deposit ---> No ---> Withdraw

        amt_p1 = str(transAmount)[0]  #--> first position value of transAmount
        if amt_p1 != "-":
			
#--> not Negative ?  
#---> Yes ----> proceed with transactions that reflect a deposit "to" action
#--> BRANCH ---> number of split List indeices > 1 
#-----> Yes/No --> proceed with split type checks/actions based on index count

            if lLen >1:

#---> number of split List indeices > 1 -----> Yes	
#--> locates "ref" in [0] value for removal using slicing based on find position

                fP1 = debitAttributeList[0].find("ref ")      
                fP2 = debitAttributeList[0].find("online transfer")
                fP3 = debitAttributeList[0].find("credit")
 
                if transList[0] == "edeposit" or transList[0] == "deposit":
                    fDeposit = "yes"

                    #print("\n","\t","--->P2: debitAttributeList[0]=",debitAttributeList[0])

#---> "ref" found ?  ---> Yes ----> remove "ref" from [0] list value via splice	
#---> #[0] "ref" removed from [0] value 
#--> determined by find/position locate of value  
#--> not found will supply "" within attribute properties

                if fP1 >= 0 and fP2 >= 0:			
                    debitAttributeList[0] = debitAttributeList[0][:fP1]        

#print("\t","---->1: fP1=",fP1," debitAttributeList[0]=",debitAttributeList[0])

#----> [0] with removed "ref" 
#--> all attribute properties obtained through function 
#--> dDB.attributesOnlineTransfer(debitAttributeList)

                    transAction, transSource, transDestination, \
                        transDescription, transCategory  \
                        = dDB.attributesOnlineTransfer(transAmount, \
                        debitAttributeList)  
                    finalByPass = "yes"
					
                    numTransform = "\t" + "---->1:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)
	
#-----> "deposit" found? ------> Yes ------->DEPOSIT MADE IN A BRANCH/STORE

                elif fDeposit == "yes":

                    transAction, transSource, transDestination, \
                        transDescription, transCategory, transLocation \
                        = dDB.extract_eDeposit(debitAttributeList,transAmount)
                    finalByPass = "yes"
                    numTransform = "\t" + "---->2:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)
					
#-----> "credit" found? ------> Yes ------->PROVISIONAL CREDIT FOR CLAIM - REF


                elif fP3 >= 0:    #--> fP3 = debitAttributeList[0].find(credit)
                    p2 = transList.index("credit")
                    p4 = debitAttributeList[0].find("claim")


                    transAction = "deposit"

                    p1 = "left"
                    p2 = p2 - 1
 
                    transSource \
                        = uETL.extractFromList(transList,p1,p2,p4)
                    
                    transCategory = uETL.getDictCategory(transSource)
                    
                    transDestination = hdrOwnerAccount

                    if p4 >= 0:
                        p4 = transList.index("claim")+1
                        #p2 = p2 + 1
                        p1 = "middle"
 
                        transDescription \
                            = uETL.extractFromList(transList,p1,p2,p4)
                        
                    else:
                        transDescription = debitAttributeList[0]
                        transCategory = "unknown"

                    numTransform = "\t" + "---->3:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)



#--> list [0] created  --> "#" NOT FOUND in description 					

            else:
                varG.studyOutList.append("\n" + "\t" + \
                    "--->only[0]-1: debitAttributeList=" + \
                    debitAttributeList[0] + "\n")
                
                fP2 = transValue.find("irs treas ")	
                fP3 = transValue.find("bill pay return")
                fP4 = transValue.find("bill pay")
                fP5 = transValue.find("interest payment")
                fP6 = transValue.find("on-line")
                fP7 = transValue.find("opening deposit")



#---> transOwner ----> IRS TREAS 310 TAX REF 091218 XXXXXXXXXX00999 
#     last, first middle  -----> transformation to first, middle, last
                
                if fP5 == -1:
                    varG.studyOutList.append("\n" + "\t" + \
                    "--->only[0]-2a: Not interest payment" + \
                    "  transList=" + str(transList) + "\n")
                    p1 = transList[-3]              
                    p2 = p1.find(',')
                    if p2 >= 0:     	             			
                        p1 = p1[:-1]                               
                    p3 = transList[-1]
                    p4 = p3.find('"')
                    if p4 >= 0:
                        p3 = p3[:p2]
                        transOwner = p1 + " " + transList[-1] + " " +  p3
                        
                        varG.studyOutList.append("\n" + "\t" + \
                            "--->only[0]-2b: transOwner" + \
                            "  transOwner=" + transList + "\n")

				
#---> "irs treas" found ? ----> 
#Yes -----> transSource_Destination, transOwner, transAction, transDescription

                if fP2 >= 0: 
                    p1 = "left"	
                    
#----> "ref" found ? ----> Yes -----> get ------> transLocation 

                    p2 = transValue.find(" ref ")
                    if p2 >= 0:
 
                        transSource = "IRS Treasury"

                    transDestination = hdrOwnerAccount

                    transOwner = transList[-3] + " " + transList[-2] + " " +\
                        transList[-1]

                    transAction = "draft deposit"

                    transDescription = "irs tax refund"

                    transCategory = uETL.getDictCategory(transDescription)

                    finalByPass = "yes"

                    varG.studyOutList.append("\t" + "---->5: transValue=" + \
                        transValue + "transValue[:p2]" + \
                        transValue[:p2] + " transList=" + transList)
                    
                    numTransform = "\t" + "---->5:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)
                    
#----> "bill pay return" found 

                elif fP3 >= 0:
                    p2 = transList.index("return")

                    transAction = "bill pay return"
                    
                    transDestination = varG.headerList[0] + " "  + \
                        varG.headerList[3]
				
                    if fP6 >= 0:
                        
                        transAction = "on-line " + transAction
                        
                        p4 = transList.index("on-line")-1                        
                        p1 = "middle"
                        p2 =+ 2

                        transSource = uETL.extractFromList(transList,p1,p2,p4)

                        transDescription = "returned bill payment"
                        
                        transCategory = "bill payment error"
					
                    else:
                        p1 = "right"
                        p2 =+ 1

                        transDescription \
                            = uETL.extractFromList(transList,p1,p2,p4)
                            
                    transOwner = varG.headerList[0] + " "  + varG.headerList[3]

                    numTransform = "\t" + "---->6a:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)
						
#----> "bill pay return" found 

                elif fP4 >= 0:
                    p2 = transList.index("bill")

                    transAction = "deposit"
                    
                    transDestination = varG.headerList[0] + " "  + \
                        varG.headerList[3]
				
                    if fP6 >= 0:
                        p4 = transList.index("on-line")

                        transDescription = transList[p4] + " " +\
                            transList[p2] + " " + transList[p2+1] + " " +\
                            transList[p2+2] 
					
                        p1 = "middle"
                        p2 =+ 2
 
                        transSource = uETL.extractFromList(transList,p1,p2,p4)
                    else:
                        p1 = "right"
                        p2 =+ 1
 
                        transDescription \
                            = uETL.extractFromList(transList,p1,p2,p4)

                    transOwner = varG.headerList[0] + " "  + varG.headerList[3]

                    numTransform = "\t" + "---->6b:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)						

                elif fP7 >= 0:
                    transAction = "acct open"
                    transSource = varG.headerList[0]
                    transDestination = varG.headerList[0] + " "  + varG.headerList[3]
                    transDescription = transValue
                    transCategory = "Account Opening Balance"
                    transOwner = transDestination
                    
#---> "irs treas" found ? ----> No ----->

                else:
					
                    fP2 = transValue.find(" sys ")
                    fP3 = debitAttributeList[0].find("bill pay")

#----> " sys " found ? ----> Yes -----> TEACHER RET SYS TRSANNUITY 
#                                                   ---            -
                    if fP2 >= 0:

                        transAction = "draft deposit"


                        transDescription = "teacher retirement check" 

                        transCategory = uETL.getDictCategory(transDescription)

                        transDestination = hdrOwnerAccount

#------> " 1" found? ------> Yes -------> left keep/slice 

                        fP2 = transValue.find(" 1")
                        if fP2 >= 0:
                            transValue = transValue[:fP2]          
                            transList = transValue.split(" ")

                            transSource = transList[-1]
                        else:
                            transSource = transValue[:fP2]

                        finalByPass = "yes"

                        varG.studyOutList.append("\t" + 
                            "------>7: transValue=" + transValue + \
                            "transValue[:fP2]" + transValue[:fP2] + \
                            " transList=" + transList)

                        
                        numTransform = "\t" + "---->7:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)
					
#-----> "deposit" found? ------> Yes ------->DEPOSIT MADE IN A BRANCH/STORE
					
                    elif transList[0] == "edeposit":

                        transOwner = ""

                        transAction, transSource, transDestination, \
                            transDescription, transCategory, transLocation \
                            = dDB.extract_eDeposit(debitAttributeList,\
                            transAmount)
                        finalByPass = "yes"
                        numTransform = "\t" + "---->8:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)
					                    	
#-----> "safe" found? ------> Yes -------> SAFE DEPOSIT BOX AUTO DEBIT REFUND

                    elif transList[0] == "safe":
 
                        transSource = varG.headerList[1]

                        transDestination = hdrOwnerAccount

                        transOwner = ""

                        transAction = "draft deposit"

                        transDescription = transValue

                        transCategory = uETL.getDictCategory(transDescription)	

                        finalByPass = "yes"

                        numTransform = "\t" + "------>9:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)

#default will supply default values	


#N-> transAmount is negative  --> determined by useing first position value of transAmount				

        else:
            print("\n","\t","->N: debitAttributeList=",debitAttributeList, \
                  " transList=", transList)
            fP1 = debitAttributeList[0].find("ref ")		
            fP2 = debitAttributeList[0].find(" check ")
            fP3 = debitAttributeList[0].find("bill pay")
            fP4 = debitAttributeList[0].find("chase credit")
            fP5 = debitAttributeList[0].find("equitable")
            fP6 = debitAttributeList[0].find("cpenergy")
            fP7 = debitAttributeList[0].find("paypal credit")
            fP8 = debitAttributeList[0].find("catholic life")
            fP9 = debitAttributeList[0].find("online transfer")
            fP10 = debitAttributeList[0].find("purchase auth")
			
#N--> "ref" found ?  ---> Yes ----> remove "ref" from [0] list value via splice

            if fP1 >= 0 and fP9 >= 0:			
                debitAttributeList[0] = debitAttributeList[0][:fP1]

#print("\t","N-->a/t: debitAttributeList[0]=",debitAttributeList[0])

#N----> [0] with removed "ref" 
#--> all attribute properties obtained through function 

                transAction, transSource, transDestination, transDescription, \
                    transCategory \
                    = dDB.attributesOnlineTransfer(transAmount, \
                    debitAttributeList)  
                finalByPass = "yes"

                numTransform = "\t" + "N---->1:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
	
#N----> "check" found ---> Yes 

            elif fP2 >= 0:    #--> fP2 = debitAttributeList[0].find(" check ")
                #---> "check" found ? ----> Yes -----> get transaction attributes:                  				
                
                p2 = transList.index("check")-1
                
                p5 = transValue.find("bcp pay ")
                p6 = transValue.find("bcf pay ")
                
                if p5 >= 0 or p6 >= 0:
                    transAction = transValue[:7]
                    
                    p1 = "middle"
                    
                    p4 = p2 + 1
                    
                    p2 = 1
                    
                    transDestination = uETL.extractFromList(transList,p1,p2,p4)
                    
                    p1 = "right" 
                    
                    p2 = p4 + 1
                    
                    transDescription = uETL.extractFromList(transList,p1,p2,p4)
                    
                    transCategory = uETL.getDictCategory(transDescription)
                else:
                    transAction = "withdraw"
    
                    p1 = "left"
     
                    transDestination = uETL.extractFromList(transList,p1,p2,p4)
                                                
                    p1 = "right"
    
                    transDescription = uETL.extractFromList(transList,p1,p2,p4)
    
                    transCategory = uETL.getDictCategory(transDestination)
                
                
                transSource = hdrOwnerAccount
    
                transOwner = varG.headerList[0] + " "  + varG.headerList[3]
                
                numTransform = "\t" + "N---->2:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)	

#N----> "bill pay" found 

            elif fP3 >= 0:
                p2 = transList.index("bill")
                p4 = debitAttributeList[0].find("on-line")
                p5 = debitAttributeList[0].find("- on-line")

                if p4 >= 0:
                    p4 = transList.index("on-line")
                    if p5 != -1:
                        p4 -= 1
                    transAction, transSource, transDestination, \
                        transDescription, transCategory  \
                        = dDB.attributesOnlineBillPay(p2, p4, transList) 
                    finalByPass = "yes"
                else:   #  may need to be included with attributeOnLine
                    p1 = "right"
                    p2 =+ 1

                    transDescription = uETL.extractFromList(transList,p1,p2,p4)
                    
                transCategory = uETL.getDictCategory(transDestination)

                numTransform = "\t" + "N---->3:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)

#N----> "chase credit" found

            elif fP4 >= 0:						
										
                p2 = transList.index("chase")
                p4 = debitAttributeList[0].find("autopay")

                transAction = "withdraw"
                
                transSource = hdrOwnerAccount
 
                transDestination = transList[p2] + " bank"			
 
                transDescription = "credit card bill pay"		

                transCategory = uETL.getDictCategory(transDestination)
                
                transOwner = ""

                numTransform = "\t" + "N---->4:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
                
#N----> "equitable" found 

            elif fP5 >= 0:						
                p2 = transList.index("equitable")
                p4 = debitAttributeList[0].find("renew")

                transAction = "withdraw"
                
                transSource = hdrOwnerAccount
 
                transDestination = transList[p2] + " insurance"

                if p4 >= 0:
                    p4 = transList.index("renew")
					
                    p1 = "middle"
                    p2 =+ 1
 
                    transDescription = uETL.extractFromList(transList,p1,p2,p4)
				
                else:
                    p1 = "right to not alpha"
                    p2 =+ 1

                    transDescription = uETL.extractFromList(transList,p1,p2,p4)

                    transOwner = ""
                    
                transCategory = uETL.getDictCategory(transDestination)

                numTransform = "\t" + "N---->5:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
	
#N----> "cpenergy" found 

            elif fP6 >= 0:
                p2 = transList.index("cpenergy")
                p4 = debitAttributeList[0].find("renew")

                transAction = "withdraw"
                
                transSource = hdrOwnerAccount
 
                transDestination = transList[p2]
 
                transDescription = "autopay gas bill"				

                transCategory = uETL.getDictCategory(transDestination)
                
                transOwner = ""

                numTransform = "\t" + "N---->6:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)	
	
#N----> "paypal credit" found 

            elif fP7 >= 0:
                p2 = transList.index("paypal")

                transAction = "withdraw"
                
                transSource = hdrOwnerAccount
 
                transDestination = transList[p2] + " " + transList[p2+1] 

                p1 = "not alpha right to end"
	
                transDescription = uETL.extractFromList(transList,p1,p2,p4)
                transDescription = transDescription + " " + "bill payment"

                transCategory = uETL.getDictCategory(transDestination)

                transOwner = ""

                numTransform = "\t" + "N---->7:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
	
#N----> "catholic life" found 

            elif fP8 >= 0:

                transAction = "withdraw"
                
                transSource = hdrOwnerAccount 
 
                transDestination = transList[p2] + " " + \
                    transList[p2+1] + " insurance"	

                transDescription = "life insurance premium payment"
                
                transCategory = uETL.getDictCategory(transDestination)

                transOwner = ""

                numTransform = "\t" + "N---->8:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)

#N----> "purchase auth" found

            elif fP10 >= 0:

                transAction = "purchase auth"
 
                transSource = transList[-2] + " " + transList[-1]
 
                transDestination = transList[4]
                transDestination = transDestination.strip(" ")

                transDescription = "debit card purchase"

                transCategory = uETL.getDictCategory(transDestination)

                transOwner = hdrOwnerAccount

                finalByPass = "yes"

                numTransform = "\t" + "N---->9:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
	
#N-----> "withdraw" found? ------> Yes ------->WITHDRAWAL MADE IN A BRANCH/STORE

            elif transList[0] == "withdrawal":

                fP1 = debitAttributeList[0].find("anch/store")

                if fP1 >= 0:
                    tlSplit = transList[-1].split("/")
                    transAction = tlSplit[0] + " " + transList[0]
                    transDestination = varG.headerList[0]
                    transDescription = debitAttributeList[0]
                    transCategory = varG.headerList[0] + " " + transAction
                else:
                    transAction = "withdraw"
                    transDescription = debitAttributeList[0]
                    transCategory = "unknown withdrawal"

                transSource = hdrOwnerAccount

                finalByPass = "yes"											

                numTransform = "\t" + "N---->10:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)

#N-----> "safe" found? ------> Yes -------> SAFE BOX ANNUAL FEE TX-NOR01963-00417

            elif transList[0] == "safe":
 
                transSource = varG.headerList[1]

                transDestination =  hdrOwnerAccount

                transOwner = ""

                transAction = "draft withdraw"

                fP1 = transValue.find(" fee")
                if fP1 >= 0:    #--> to remove --> TX-NOR01963-00417
                    transDescription = transValue[:fP1+4]     
                else:
                    transDescription = transValue

                transCategory = uETL.getDictCategory(transDescription)

                finalByPass = "yes"

                print("\t","N---->11: transList[-1]=",transList[-1],\
                      " str.isalnum(transList[-1])=",\
                      str.isalnum(transList[-1])," p2=",p2," p4=",p4,\
                      " transValue=",transValue," transValue[:p4-p2]=",\
                      transValue[:p4-p2])
	
                numTransform = "\t" + "N---->11:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
		
#N-----> DEFAULT --------> IRS USATAXPYMT 99 999 first m last
#                -------> HOCHHEIM PRAIRIE Hochheim 10HP 999 first m last
            else:

                transAction = "draft payment"

                print("\t","N----->12: transList=",transList,\
                      " transList[0]=",transList[0]," description=",description)
				
                fP1 = transValue.find("usataxpymt ")
                fP2 = transValue.find("0hp ")
                fP3 = transValue.find("check")
				
                if fP1 >= 0: 
                    p2 = transValue.find(" 0")

                    transSource = hdrOwnerAccount

                    transDestination = "irs treasury"

                    transDescription = "irs usa tax payment"
			
                    transOwner = transList[-3] + " " + transList[-2] + " " + \
                        transList[-1]	

                    transCategory = uETL.getDictCategory(transDescription)

                    finalByPass = "yes"							

                    numTransform = "\t" + "N---->12:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)

#N----->  "0hp" --> found    fP2 = transValue.find("0hp ") 

                elif fP2 >= 0:
		
                    transList = transValue[:fP2-2].split(" ")
                    transDestination = transList[0] + " " + transList[1]
                    transSource = hdrOwnerAccount

                    transDescription = "insurance premium payment"
			
                    transOwner = transList[-3] + " " + transList[-2] + " " + \
                        transList[-1]

                    transCategory = uETL.get_transAction(str(transAmount))	
                    finalByPass = "yes"
                    
                    numTransform = "\t" + "N---->13:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)				

                else:

                    transAction = "withdraw"
                    
                    transSource = hdrOwnerAccount

                    p1 = "right to not alpha"
                    p2 = 0

                    transDestination \
                        = uETL.extractFromList(transList,p1,p2,p4)
					
                    p4 = transDestination.find("harland")
                    if p4 >= 0:
					
                        transDescription = "checks for checking account"
                        
                    transCategory = uETL.getDictCategory(transDestination)
	
                    numTransform = "\t" + "N---->14:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)              
        
class Savings:
    
    def setSavingsAttributes(self):        
        global hdrSource
        global hdrOwnerAccount
        
        global description
        global descriptionList

        global transDate
        global transAmount
        global transLocation
        
        global transAction
        global transSource
        global transDestination
        global transDescription
        global transCategory
        
        global transOwner
        global transAccount
                
        lLen = 0
        debitAttributeList = []
        transList = []
        
        transSource_Destination = ""
        transValue = ""
        

        fP1 = 0
        fP2 = 0
        fP3 = 0		
        fP4 = 0
        fP5 = 0


        p1 = ""
        p2 = 0
        p4 = 0

        finalByPass = ""

        
        outStudy = Study()
        
        
        debitAttributeList = description.split("#")
        lLen = len(debitAttributeList)
        if lLen >1:
#---> number of split List indeices > 1 -----> Yes		
#--> locates "__" in [0] value for removal using slicing based on find position
            fP1 = debitAttributeList[0].find("ref ")      
            fP2 = debitAttributeList[0].find("online transfer")
            fP3 = debitAttributeList[0].find("credit")
            fP4 = debitAttributeList[0].find("recurring tr")

#---> #[0] "ref" removed from [0] value 
#--> determined by find/position locate of value  
#--> not found will supply "" within attribute properties
            if fP1 >= 0 and fP2 >= 0  or \
                fP1 >= 0 and fP4 >= 0:			
                debitAttributeList[0] = debitAttributeList[0][:fP1]
				#print("\t","---->1: fP1=",fP1," debitAttributeList[0]=",\
                #    debitAttributeList[0])
#----> [0] with removed "ref" --> all attribute properties obtained through function 
#--> dDB.attributesOnlineTransfer(debitAttributeList)
                transAction, transSource, transDestination, transDescription, \
                    transCategory \
                    = dDB.attributesOnlineTransfer(transAmount,debitAttributeList)
				
                finalByPass = "yes"   #change item --- may not need
                numTransform = "\t" + "---->1:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)                

        else:
            fP1 = debitAttributeList[0].find("interest payment")
            fP2 = debitAttributeList[0].find(" sec ")			
            if fP1 >= 0:
                transAction = "eDeposit"
                transSource = varG.headerList[1]
                transDestination = hdrOwnerAccount
                transDescription = varG.headerList[3] + " interest earned"
                transCategory = "interest earnings"
                finalByPass = "yes"
                numTransform = "\t" + "---->2:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)

            elif fP2 >= 0: 
                transValue = str(debitAttributeList[0])
                transList = transValue.split(" ")
                transLocation, transOwner  = dDB.extract_Social_Security(transList)
                transSource = transLocation + " " + transOwner
                transDestination = hdrOwnerAccount
                transAction = "eDeposit"
                transDescription  = "social security draft auto deposit"
				#print ("\t","SSN: transSource=",transSource)
                transCategory = uETL.getDictCategory(transDescription)
                finalByPass = "yes"
                print("\t","SSN: transCategory=",transCategory)
                numTransform = "\t" + "---->3:"
                outStudy.formatOutTransStudy(numTransform,\
                    transSource_Destination,finalByPass)
			
            else:
                transValue = str(debitAttributeList[0])
                transList = transValue.split(" ")
                #print("\t","\t","transList=",transList," transList[0]=",\
                #   transList[0]," description=",description)
                if transList[0] == "edeposit":	

                    transAction, transSource, transDestination, \
                        transDescription, transCategory, transLocation \
                        = dDB.extract_eDeposit(debitAttributeList,transAmount)
					
                    finalByPass = "yes"
                    numTransform = "\t" + "---->4:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)						
				
 

                else:
                    fP1 = debitAttributeList[0].find("item retn")
                    fP2 = debitAttributeList[0].find("unpaid")
                    fP3 = debitAttributeList[0].find("cashed")
                    fP4 = debitAttributeList[0].find("go far rew")
                    fP5 = debitAttributeList[0].find("service fee")
                    finalByPass = "yes"
                    if fP1 >= 0 and fP2 >=0:
                        transAction = debitAttributeList[0][:fP2+6]
                        transSource = hdrSource
                        transDestination = varG.headerList[0] +  " " + \
                            varG.headerList[3]
                        transDescription = debitAttributeList[0]
                        transCategory = "item return unpaid"
                        if fP3 >=0:
                            transCategory = transCategory + " fee"
                        numTransform = "\t" + "---->5:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)
                    elif fP4 >= 0:
                        transAction = "reward deposit"
                        transSource = hdrSource + " credit"
                        if transSource in varG.inTHelpersDict:
                            transSource = varG.inTHelpersDict[transSource][0]
                        transDestination = hdrOwnerAccount
                        transDescription = "go for rewards"
                        transCategory = "credit account reward"
                        finalByPass = "yes"
                        numTransform = "\t" + "---->6:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)
                    elif fP5 >= 0:
                        transAction = "eWithdraw"
                        transSource = hdrOwnerAccount
                        transDestination = hdrSource 
                        transDescription = "monthly service fee"
                        transCategory = "bank account fee"
                        finalByPass = "yes"
                        numTransform = "\t" + "---->7:"
                        outStudy.formatOutTransStudy(numTransform,\
                            transSource_Destination,finalByPass)
                    else:
                        p1 = "all"
                        transList = str(debitAttributeList[0]).split(" ")
                        transDescription = uETL.extractFromList(transList,p1,p2,p4)
                        transCategory = "unknown"
                        if str(transAmount)[0] == "-":
                            transAction = "withdraw"
                            transSource = hdrOwnerAccount
                            transDestination = "unknown"
                            numTransform = "\t" + "---->8:"
                            outStudy.formatOutTransStudy(numTransform,\
                                transSource_Destination,finalByPass)
                        else:
                            transAction = "deposit"
                            transDestination = hdrOwnerAccount
                            transSource = "unknown"
                            numTransform = "\t" + "---->9:"
                            outStudy.formatOutTransStudy(numTransform,\
                                transSource_Destination,finalByPass)

                    numTransform = "\t" + "---->10:"
                    outStudy.formatOutTransStudy(numTransform,\
                        transSource_Destination,finalByPass)

        numTransform = "\t" + "->sE1-n:"
        outStudy.formatOutTransStudy(numTransform,\
            transSource_Destination,finalByPass)
        

class Study:
    
    def formatOutTransStudy(self,numTransform,transSource_Destination,\
        finalByPass):
        
        self.numTransform = numTransform
        self.transSource_Destination = transSource_Destination
        self.finalByPass = finalByPass
        
        global transLocation
        global transAction
        global transSource
        global transDestination
        global transDescription
        global transCategory
        global transLocation
        
        varG.studyOutList.append("\t" + \
            self.numTransform + " transAction=" + transAction + \
            " transSource=" + transSource + \
            " transDestination=" + transDestination + \
            " transDescription=" + transDescription + \
            " transCategory=" + transCategory + \
            " transOwner=" + transOwner + \
            " transLocation=" + transLocation + \
            "\n" + "\t" + \
            " transSource_Destination=" + self.transSource_Destination + \
            " finalByPass=" + self.finalByPass)