# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:56:53 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
#from collections import defaultdict
#from re import sub
#from decimal import Decimal
#import datetime

class Fields: 
    
    def setJMcheckingAttributes(fields):


#        print("\n","\t","-->S  transAction=",transAction," transSource=",transSource," transDestination=",transDestination, \
#              " transDescription=",transDescription," transCategory=",transCategory)


        toNegative = "no"
        inT_Date = fields[0]
        inT_AmountOne = fields[1]
        inT_AmountTwo = fields[2]
        inT_Description = fields[3]
        inT_Category = fields[4]


        transAction = ""
        transSource = ""
        transDestination = ""	
        transDescription = ""
        transCategory = ""
        transOwner = varG.headerList[0]
        transLocation = ""
        transAccount = varG.headerList[3]
        prevMonth = ""        
                      
        saveMonth = ""

        sqlTupleCnt = 0
        second_mySQL = ""

        toNegative = ""
              
        bypassOut = False
        sqlTuple = ()
        sqlTupleCnt = 0
        tuple_Sam = ()
        list_Sam = []
        dict_Sam = {}
        cntSam = 0
        tuple_Mom = ()
        list_Mom = []
        dict_Mom = {}
        cntMom = 0
        
        dict_Category = {"wells fargo cred":"credit card payment",\
            "dell financial services":"laptop no interest payment",\
            "Bill Me Later":"paypal no interest payment",\
            "Month Start Transfer":"auto online transfer to savings",\
            "GECRB/AMAZON":"credit card payment",\
            "auto online transfer to savings":"auto funds for savings",\
            "end month online transfer to savings":"manual funds for savings",\
            "Month End Transfer":"manual funds for savings",\
            "Pam":"Pam K Service Pay Check"}


        

        if inT_AmountOne == "":
            inT_AmountOne = 0.0
        if inT_AmountTwo == "":
            inT_AmountTwo = 0.0

        inT_AmountOne = float(inT_AmountOne)
        inT_AmountTwo = float(inT_AmountTwo)

        dateSplit = inT_Date.split("/")	      #this bit of code is to zero pad the mm and dd
        dateSplit[0] = str(dateSplit[0]).zfill(2) 
        dateSplit[1] = str(dateSplit[1]).zfill(2)
	
        transDate = str(dateSplit[2]) + "/" + str(dateSplit[0]) + "/" + str(dateSplit[1])

        print("\n","-->Start:  fields=",fields)
        inT_Category = inT_Category.lstrip(" ")
        inT_Category = inT_Category.rstrip(" ")

        if inT_Category == "":    # withdraw set of input transactions
            print("\n","-->1:  inT_Category=",inT_Category)
            fP1 = inT_Description.find("ransfer")
            #fP2 = inT_Description.find()
            transAction = "bill pay on-line"
            if fP1 >= 0:
                transAction = "online transfer"
                transSource = varG.headerList[0] + " " + varG.headerList[3]
                transDestination = inT_Description
                transDescription = "bill payment for month - " + str(dateSplit[0])
                transCategory = "bill payment"

            if inT_Category in dict_Category:		
                transCategory = dict_Category[inT_Category]	
		
            toNegative = "yes"
            print("\n","\t","-->1  transDate=",transDate," transAction=",transAction," transSource=",transSource," transDestination=",transDestination, \
              " transDescription=",transDescription," transCategory=",transCategory)				

        elif inT_Category == "Sam Out and In":
            print("\n","-->2:  inT_Category=",inT_Category)
            cntSam = cntSam + 1
            tuple_Sam = (str(inT_AmountOne),str(inT_AmountTwo),str(inT_Description))
		
            if dateSplit[0] != saveMonth and cntSam > 1:							
                dict_Sam[saveMonth] = list_Sam
                list_Sam = []

            list_Sam.append(tuple_Sam)
            saveMonth = dateSplit[0]
            transAction = ""
            toNegative = "yes"

        elif inT_Category == "Mom Out and In":
            print("\n","-->3:  inT_Category=",inT_Category)
            fP1 = inT_Description.find("eimb")
            if fP1 == -1:  # not found
                cntMom = cntMom + 1
                tuple_Mom = (str(inT_AmountOne),str(inT_AmountTwo),str(inT_Description))
			
                if dateSplit[0] != prevMonth and cntMom > 1:							
                    dict_Mom[prevMonth] = list_Mom
                    list_Mom = []

                list_Mom.append(tuple_Mom)
                prevMonth = dateSplit[0]
                transAction = ""
            else:
                transAction = "online transfer"
                transSource = "JMmom Checking"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = "to Jeanette for utility bill payment"
                transCategory = "reimbursement from JMmom"
                
        elif inT_Category == "Bank Fee":
            print("\n","-->4:  inT_Category=",inT_Category)
            transAction = "bill pay on-line fee"
            transSource = varG.headerList[1]
            transDestination = varG.headerList[0] + " " + varG.headerList[3]
            transDescription = "1 day on-line payment fee"
            transCategory = "online bank fee"
            toNegative = "yes"

        elif inT_Category == "Money In":
            print("\n","-->5:  inT_Category=",inT_Category)
            if inT_Description != "January  NET":
                fP1 = inT_Description.find("Pam")
                if fP1 >= 0:  # found
                    transAction = "deposit in branch"
                    transSource = "Pam K Properties"
                    transDestination = varG.headerList[0] + " " + varG.headerList[3]
                    transDescription = inT_Description
                    transCategory = "Pam K Service Pay Check"
                else:
                    transAction = "unkown"
                    transSource = "unkown"
                    transDestination = varG.headerList[0] + " " + varG.headerList[3]
                    transDescription = inT_Description
                    transCategory = inT_Category

        elif inT_Category == "other - transfer in":
            print("\n","-->6:  inT_Category=",inT_Category)
            fP1 = inT_Description.find("imburse")
            fP2 = inT_Description.find("payment")
            fP3 = inT_Description.find("savings")
            fP4 = inT_Description.find("overdraft")
            fP5 = inT_Description.find("Tax Pa")
            fP6 = inT_Description.find("BML Pay")

            if fP1 >= 0:  # found
                transAction = "online transfer"
                transSource = "JMmom Checking"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = inT_Description
                transCategory = "reimbursement from JMmom"

            elif fP2 >= 0 or fP3 >= 0  or fP4 >= 0 :  # found
                transAction = "online transfer"
                transSource = "Jeanette Savings"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = inT_Description
                transCategory = "savings funds to checking"
            elif fP5 >= 0:
                transAction = "online transfer"
                transSource = "Jeanette Savings"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = inT_Description
                transCategory = "tax payment funds"
            else:
                transAction = "online transfer"
                transSource = "Jeanette Savings"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = inT_Description
                transCategory = "bill payment funds"

        elif inT_Category == "Debit Card/Money Out":
            print("\n","-->7:  inT_Category=",inT_Category)
            fP1 = inT_Description.find("over transf")
            if fP1 >= 0:  # found
                transAction = "online transfer"
                transSource = varG.headerList[0] + " Savings"
                transDestination = varG.headerList[0] + " " + varG.headerList[3]
                transDescription = inT_Description
                transCategory = "over transfer correction"
        else:
            print("\n","-->Default:  inT_Category=",inT_Category)
            transAction = "unkown"
            transSource = "unkown"
            transDestination = "unkown"
            transDescription = inT_Description
            transCategory = "unkown"


        print("\n","\t","-->E1  transAction=",transAction," transSource=",transSource," transDestination=",transDestination, \
              " transDescription=",transDescription," transCategory=",transCategory)

        if transAction == "" or \
            inT_Description == "January  NET":
            bypassOut == True


        if inT_AmountOne > 0:
            transAmount = float(inT_AmountOne)
        else:
            transAmount = float(inT_AmountTwo)

	
        if toNegative == "yes":
            transAmount = float(transAmount) * -1

        transAmount = "%.2f" %transAmount

			
        sqlTupleCnt = sqlTupleCnt + 1		

        sqlTuple = (sqlTupleCnt, str(transDate), float(transAmount), str(transAction), str(transSource),str(transDestination), 		
            str(transDescription), str(transCategory), str(transOwner), str(transLocation),str(transAccount),0,'now()')
	
        print("\n","\t","-->E2  sqlTuple=",sqlTuple)
	
        second_mySQL = second_mySQL + "," + str(sqlTuple)
	
        transAction = ""
        transSource = ""
        transDestination = ""	
        transDescription = ""
        transCategory = ""
        transLocation = ""


        print("\n","dict_Mom=",dict_Mom)
        print("\n","dict_Sam=",dict_Sam)


class Payment:

    def samPayment(self,dict_Sam):
        self.dict_Sam = dict_Sam
        
        transAction = ""
        transSource = ""
        transDestination = ""	
        transDescription = ""
        transCategory = ""
        transOwner = varG.headerList[0]
        transLocation = ""
        transAccount = varG.headerList[3]
        
        aOne_Total = 0.0 
        a_One = 0.0
        aTwo_Total = 0.0
        a_Two = 0.0
        
        for key in dict_Sam:
            if key == "06":
                break
            list_Sam = dict_Sam[key]
            transDate = key + "/15/2018"
            for x, y in enumerate(list_Sam):
                print("\t","key=",key," transDate=",transDate," y[0]=",y[0],"y[1]=",y[1],"y[2]=",y[2])
                if y[0] == "":
                    a_One = 0.0
                else:
                    a_One = y[0]
            if y[1] == "":
                a_Two = 0.0
            else:
                a_Two = y[1]

            aOne_Total = float(aOne_Total) + float(a_One)
            aTwo_Total = float(aTwo_Total) + float(a_Two)
            yList = y[2].split(" ")
            y2Value = ""
            y2Value = yList[0] + " " + yList[1]
            lLen = len(y2Value)
            print("\n","\t","y2Value=",y2Value," lLen=",lLen)

            if lLen > 10:
                y2Value = y2Value[:10]
                print("\t","y2Value=",y2Value,"\n")

            transDescription = transDescription + "-" + y2Value
            print("\t","transDescription=",transDescription)

	
        print("\n","\t","transDescription=",transDescription," aOne_Total=",aOne_Total," aTwo_Total=",aTwo_Total)
        transAction = "pay on-line"
        transSource = varG.headerList[0] + " " + varG.headerList[3]
        transDestination = "Sam"
        transDescription = transDescription.lstrip("- ")
        transCategory = "Sam owed payment"

        transAmount = "%.2f" %aOne_Total

        if aTwo_Total > 0:
            transAmount = "%.2f" %aTwo_Total

        transAmount = float(transAmount) * -1

        print("\n","\t","transAmount=",transAmount)

        sqlTupleCnt = sqlTupleCnt + 1		

        #sqlTuple = (sqlTupleCnt, str(transDate), float(transAmount), str(transAction), str(transSource),str(transDestination), 		
        #    str(transDescription), str(transCategory), str(varG.headerList[0]), str(transLocation),str(varG.headerList[3]),0,'now()')
        #print("\n","2 sqlTuple=",sqlTuple)

        #second_mySQL = second_mySQL + "," + str(sqlTuple)
        transDescription = ""
        aOne_Total = 0.0
        aTwo_Total = 0.0



