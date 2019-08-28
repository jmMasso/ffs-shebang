# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 12:26:49 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from trans_DescriptionETL import CreditSource as dCR
from trans_UniversalETL import Universal as uETL

class Credit: 
    
    def setCreditCardAttributes(description,descriptionList,\
         transDate,transAmount,transLocation):
         
        
        varG.studyOutList.append("\n" + "\t" + \
            " setCreditCardAttributes-S: description=" + description + \
            " descriptionList=" + str(descriptionList) + \
            " transDate=" + transDate + " transAmount=" + str(transAmount) + \
            " transLocation=" + transLocation)
        
        
        #print('\n','varG.headerList=',varG.headerList)
        
        sourceSet = ""

        
        
#Start of setCreditCardAttributes -->Driver Logic<--
		
        #print("\n", "descriptionList=",descriptionList)
        useZvalues = ""
        setActions = ""
        transAction = ""        
        transSource = ""
        transDestination = ""
        transDescription = ""
        transCategory = ""
        #   Owner - [0]  Bank - [1]  Type - [2]  Account - [3]
        transOwner = varG.headerList[0]
        transAccount = varG.headerList[3]
        
        transSourceList = []
        transSourceLast = ""

        splitPos = 0
        #if hdrType = "Credit":

        updatePayReimbTupleList = []

        #print("\n","\n","\t","CrCard --->S: descriptionList=",descriptionList,\
        #      "\n","\t"," transAction=",transAction," transSource=",\
        #      transSource," transDestination=",transDestination, \
        #      " transDescription=",transDescription, " transOwner=",transOwner,\
        #      " transLocation=",transLocation,"\n")	

        for z, iValue  in enumerate(descriptionList):
						
            #print("\n","\n","  z=",z," iValue =",iValue )	
            countUse = 0
            useValue = ""
            sourceSet = "" 
            setActionList = ["",""]
            iValue  = iValue.lower()
#  When first z in list the zValue is evaluated for determining only  
#  transSource only list value
#  useValue, sourceSet, countUse = return values for building tranSource    
            if z == 0:
                useValue, sourceSet, countUse = dCR.First_iValue_Check(iValue,\
                    description)
                
                varG.studyOutList.append("\n" + "\t" + \
                    " setCreditCardAttributes-z-" + str(z) + ": iValue=" + iValue + \
                    " useValue=" + useValue + " sourceSet=" + sourceSet + \
                    " countUse=" + str(countUse))               
                
							
                if sourceSet != "":
                    transSource = useValue
                    setActionList = sourceSet.split("-")
                    useZvalues = str(z)
                    setActions = setActions + " " + str(z) +  "," \
                        + str(setActionList[1:]) 
                    #print("\n","\t","--->0: setActionList[0]=",setActionList[0],\
                    #      "useValue=",useValue," transSource=",transSource)
                    if setActionList[0] == "break":	
                        break
                    if setActionList[0] == "continue":
                        continue	
                    #elif setActionList[0] == "reject":
                    #	continue

            elif z <= 3:
                useValue, sourceSet, countUse = dCR.Second_iValue_Check(iValue,\
                    transSource)				

                if sourceSet != "":
                    setActionList = sourceSet.split("-")
                    useZvalues = useZvalues + " " + str(z)
                    setActions = setActions + " " + str(z) +  "," \
                        + str(setActionList[1:])
                    transSource = transSource + " " + useValue 
                    #print("\n","\t","--->1: setActionList[0]=",\
                    #      setActionList[0],"useValue=",useValue,\
                    #      " transSource=",transSource)
                    if setActionList[0] == "break":	
                        break
                    if setActionList[0] == "continue":	
                        continue
                    #elif setActionList[0] == "reject":
                    #	continue
            
                varG.studyOutList.append("\n" + "\t" + \
                    " setCreditCardAttributes-z-" + str(z) + ": iValue=" + iValue + \
                    " useValue=" + useValue + " sourceSet=" + sourceSet + \
                    " countUse=" + str(countUse))
	
			
#--> wrapup attribute setting by creating necessary return variables 

#--> necessary prep

        #transAmount = float(transAmount) * -1     #-->  analysis requires conversion to 

        varG.studyOutList.append("\n" + "\t" + \
            " setCreditCardAttributes-M: transSource=" + transSource + \
            " sourceSet=" + sourceSet)
        
        transSource = transSource.lstrip(" ")
        transSource = transSource.rstrip(" ")
        transSourceList = transSource.split(" ")

        transSourceLast = transSourceList[-1].lower() 
        transSourceLast = transSourceLast.strip()


        #print("\n","\n","\t","transSourceList=",transSourceList,"\n","\n",\
        #      " transSourceLast=",transSourceLast,"\n"," lastDropList=",\
        #      varG.lastDropList,"\n","\n")
        if transSourceLast in varG.convertContinueDict:
            transSourceList[-1] = varG.convertContinueDict[transSourceLast]
            p1 = "all"
            p2 = 0
            p4 = 0
            transSource = uETL.extractFromList(transSourceList,p1,p2,p4)
            #print("\t","-->sE1")
        elif transSourceLast in varG.lastDropList:
            splitPos = len(transSource) - len(transSourceList[-1])

            #print("\t","transSourceLast=",transSourceLast," transSource=",
            #      transSource,"  ",len(transSource),"-",\
            #      len(transSourceList[-1]),"-",splitPos)
            transSource = transSource[:splitPos]
            #print("\t","transSourceLast=",transSourceLast,\
            #       " transSource=",transSource,"\n","\n")

        transSource = transSource.lstrip(" ")
        transSource = transSource.rstrip(" ")


        transCategory = uETL.getDictCategoryByKey(transSource)
        
        varG.studyOutList.append("\n" + "\t" + \
            " setCreditCardAttributes-M: transSource=" + transSource + \
            " transCategory=" + transCategory)

        #print("\n","\t", \
        #      " transAction=",transAction," transSource=",transSource,\
        #      " transDestination=",transDestination," transDescription=",\
        #      transDescription," transCategory=",transCategory, \
        #      " transOwner=",transOwner," transCategory=",transCategory,\
        #      " transOwner=",transOwner," transLocation=",transLocation,\
        #      " transAccount= ", transAccount)							



        print1 = description.ljust(120," ")
        print2 = transAction.ljust(30," ")
        print4 = transSource.ljust(40," ")
        print5 = transDescription.ljust(40," ")
        print6 = transCategory.ljust(30," ")		
        print7 = transOwner.ljust(20," ")
        print8 = transLocation.ljust(20," ")
        print9 = transAccount.ljust(40," ")
        outLine = "\t" + " in-" + str(print1) + "   " + str(transAmount) + "\t" + "\t" + "Act= " + str(print2) + "\t" + "\t" + "\t" + \
            "Sour/Dest= " + str(print4) +"\t" + "\t" + "\t" +  "Desc= " + str(print5) +  \
            "Cat= " + str(print6) + "Owner= " + str(print7) +  "Loc= " + str(print8) + "Acct= " + str(print9) +  "\n"
		
		
        outLine2 = str(description) + "\t" + str(transDate) + "\t" + str(transAmount) + "\t" + str(transAction) + "\t" + str(transSource) + \
            "\t" + str(transSource) + \
            "\t" + str(transDescription) + "\t" + str(transCategory) + "\t" + str(transOwner) + "\t" + str(transLocation) + \
            "\t" + str(transAccount) + "\n"

		
        #transStudy.write(outLine2)
		
			

        return transAction, transSource, transDestination, transDescription, transCategory
        #return transSource, sqlTuple, sql_outTransID, sqlTuple_PayReimbCrCard, keyPayReimbCrCard, updatePayReimbTupleList, inRecircPR_Dict