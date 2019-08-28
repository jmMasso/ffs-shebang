# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:24:09 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from trans_UniversalETL import Universal as uETL
#import calendar

class CreditSource:
    		             
    def First_iValue_Check(iValue,description):
        
        sourceSet = ""
        useValue = ""
        countUse = 0
        changeCase = "y"
        splitList = []
        splitFirst = ""
        
        #varG.studyOutList.append("\n" + "\t" + \
        #    " First_iValue_Check-B: iValue=" + iValue + \
        #    " description=" + description)
        
        fP = iValue.find("'s")
        if fP!= -1:
            #splitFirst = iValue[:fP]
            useValue = iValue
            for key in varG.convertStopDict:
                fP = iValue.find(key)
                if fP != -1:
                    useValue = varG.convertStopDict[key]
                    sourceSet = "break" + "Apostrophe-s-find-convertStop"
                    changeCase = ""
            if sourceSet == "":
                useValue = iValue[:fP-1].title() + "'s"
                sourceSet = "continue" + "-Apostrophe-s"                
                changeCase = ""
                
            useValue = uETL.firstPositionSplitKeepRight(useValue)
            #print("\t","-->2a1")        
        elif iValue  in varG.singleNameList:
            useValue = iValue 
            sourceSet = "break" + varG.singleNameList[-1]
        elif iValue  in varG.rejectList:
            sourceSet = "continue" + varG.rejectList[-1]
        elif iValue  in varG.convertStopDict:
            useValue = varG.convertStopDict.get(iValue)  
            sourceSet = "break" + "-convertStop"
            changeCase = ""
            if useValue in varG.checkGasList:
                gP = description.find("gas")
                if useValue == "wal-mart":
                    useValue.title()
                if gP >= 0:
                    useValue = useValue + " " + "Gas"
                    sourceSet = sourceSet + "-Gas"
        elif str.isalpha(iValue):
            useValue = iValue 
            sourceSet = "continue" + "-alpha"
        else:
            for key in varG.convertStopDict:
                fP = iValue.find(key)
                if fP != -1:
                    useValue = varG.convertStopDict[key]
                    sourceSet = "break" + "-find-convertStop"
                    changeCase = ""
                    break
            if sourceSet == "":
                splitSource = uETL.splitCheck(iValue) 
                #print("\t","splitSource=",splitSource)
                if splitSource != "":
                    splitList = splitSource.split(" ")
                    splitFirst = splitList[0]
                    if splitFirst in varG.convertStopDict:
                        useValue = varG.convertStopDict.get(splitFirst) 
                        sourceSet = "break" + "-split-convertStop"
                        changeCase = ""
                    else:
                        useValue = splitSource
                        sourceSet = "continue" + "-split"
                else:
                    changeCase = ""


        if changeCase == "y":
            if useValue in varG.allCapsList:
                useValue = useValue.upper()
                countUse = countUse + 1
            else:
                useValue = useValue.title()
                countUse = countUse + 1

        #print("\n","First: countUse=",countUse,"useValue=",useValue,"\n")

        return useValue, sourceSet, countUse
    
    
    def Second_iValue_Check(iValue,transSource):
        sourceSet = ""
        useValue = ""
        countUse = 0
        firstPosValue = ""
        firstPosValue = iValue[:1]
        changeCase = "y"
        splitFirst = ""
        #print("\t","firstPosValue=", firstPosValue,"iValue =",iValue )
        
        fP = iValue.find("'s")
        if fP!= -1:
            #splitFirst = iValue[:fP]
            useValue = iValue
            for key in varG.convertStopDict:
                fP = iValue.find(key)
                if fP != -1:
                    useValue = varG.convertStopDict[key]
                    sourceSet = "break" + "-find-convertStop"
                    changeCase = ""
                    break
            if sourceSet == "":
                useValue = iValue[:fP-1].title() + "'s"
                sourceSet = "continue" + "-Apostrophe-s"                
                changeCase = ""
                
            useValue = uETL.firstPositionSplitKeepRight(useValue)
            
            #print("\t","-->2a1") 
        elif iValue  in varG.singleNameList:
            useValue = iValue 
            sourceSet = "break" + varG.singleNameList[-1] 
            #print("\t","-->2ab")
        elif iValue  in varG.stopList:
            useValue = iValue 
            sourceSet = "break" + varG.stopList[-1]
            #print("\t","-->2b")
        elif iValue  in varG.rejectList:
            sourceSet = "continue" + varG.rejectList[-1]
            #print("\t","-->2c")
        elif iValue  in varG.convertStopDict:
            useValue = varG.convertStopDict.get(iValue)  
            sourceSet = "break" + "-convertStop"
            changeCase = ""
            #print("\t","-->2d")
        elif iValue  in varG.convertContinueDict:
            useValue = varG.convertContinueDict.get(iValue) 
            sourceSet = "continue" + "-convertContinue"
            changeCase = ""
            #print("\t","-->2e")
        elif firstPosValue in varG.firstPositionRejectStopList:
            if transSource == "":
                sourceSet = "continue" + varG.firstPositionRejectStopList[-1]
            else:
                sourceSet = "break" + varG.firstPositionRejectStopList[-1]
            #print("\t","-->2f")	
        elif firstPosValue in varG.firstPositionSplitKeepRightList:
            iValue  = iValue[1:]
            if str.isalpha(iValue):
                useValue = iValue 
                if iValue  in varG.convertStopDict:
                    useValue = varG.convertStopDict.get(iValue)  
                    sourceSet = "break" + \
                        varG.firstPositionSplitKeepRightList[-1] + "-convertStop"
                    changeCase = ""
                    #print("\t","-->2g")
                else:
                    sourceSet = "continue" + \
                        varG.firstPositionSplitKeepRightList[-1]
                    #print("\t","-->2h")                   
            else:
                #print("\t","first-rest iValue =", iValue )
                splitSource = uETL.splitCheck(iValue) 
                useValue = splitSource
                if useValue in varG.convertStopDict:
                    useValue = varG.convertStopDict.get(useValue) 
                    sourceSet = "break" + \
                        varG.firstPositionSplitKeepRightList[-1] + \
                        "-split" + "-convertStop"
                    changeCase = ""
                    #print("\t","-->2i-a")
                elif useValue in varG.stopList:
                    sourceSet = "break" + \
                        varG.firstPositionSplitKeepRightList[-1] + \
                        "-split" + "-stopList"
                    #print("\t","-->2i-b")
                else:
                    sourceSet = "continue" + \
                        varG.firstPositionSplitKeepRightList[-1] + "-split"
                    #print("\t","-->2i-c")


        elif str.isalpha(iValue):
            useValue = iValue 
            sourceSet = "continue" + "-alpha"
            #print("\t","-->2k")
        else:
            for key in varG.convertStopDict:
                fP = iValue.find(key)
                if fP != -1:
                    useValue = varG.convertStopDict[key]
                    sourceSet = "break" + "-find-convertStop"
                    changeCase = ""
                    break
            if sourceSet == "":
                splitSource = uETL.splitCheck(iValue) 
                #print("\t","splitSource=",splitSource)
                if splitSource != "":
                    if splitSource in varG.convertStopDict:
                        useValue = varG.convertStopDict.get(splitSource) 
                        sourceSet = "break" + "-split-convertStop"
                        changeCase = ""
                        #print("\t","-->2l")
                    else:
                        useValue = splitSource
                        sourceSet = "continue" + "-split"
                        #print("\t","-->2j")
                else:
                    changeCase = ""
                    #print("\t","-->2k")
        
        if changeCase == "y":
            if useValue in varG.allCapsList:
                useValue = useValue.upper()
                countUse = countUse + 1
                #print("\t","-->2l")
            else:
                useValue = useValue.title()
                countUse = countUse + 1
                #print("\t","-->2m")

        #print("\n","Second: countUse=",countUse,"useValue=",useValue,"\n")

        return useValue, sourceSet, countUse
    
    
class DebitType:

#--> Method  attributesOnlineTransfer ---> used by 
#----> checking when [0] list value has -----> "ref" found in value
#   --> [0] AND [1] list values are within supplied parameter	

    def attributesOnlineTransfer(transAmount, debitAttributeList):
    
        lLen = len(debitAttributeList)
        transValue = ""
        transList = []
        yAccount = ""
        hdrOwnerAccount =  varG.headerList[0] + " " +  varG.headerList[3] 

        amt_p1 = str( transAmount)[0]
	

        #return attributes
        transAction = ""
        transSource = ""
        transDestination = ""
        transDescription = ""
        transCategory = ""
		
		

        p1 = ""
        p2 = 0
        p4 = 0
        fP1 = 0
        fP2 = 0
        fP3 = 0
        fP4 = 0
        fP5 = 0

        lLen = 0
        fMom = -1

        transferName = ""
		
#STATEMENTS
        varG.studyOutList.append("\n" + "\t" + "refSplit: amt_p1=" + amt_p1 \
            + "  debitAttributeList=" + str(debitAttributeList))   
        transValue = str(debitAttributeList[0])
        transList = transValue.split(" ")
        varG.studyOutList.append("\t" + "\t" + "transList=" + str(transList) + " transList[0]=" + transList[0])


#transAction --> first two in transList        
#--> ONLINE TRANSFER TO SCHNEIDER A EVERYDAY CHECKING XXXXXX2969
        p1 = "left"                                
        p2 = 1
        transAction = uETL.extractFromList(transList,p1,p2,p4)
        varG.studyOutList.append("\t" + "\t" + "transAction=" + transAction)
        transAction = transAction.lstrip(" ")
        transAction = transAction.rstrip(" ")


#trans name --> 3                
#--> ONLINE TRANSFER TO MASSO J REF # EVERYDAY CHECKING TO MOMS CHKG FOR JUNE RETIREMENT
        p1 = "right"
        p2 = 3

        transferName = uETL.extractFromList(transList,p1,p2,p4)
        transferName = transferName.rstrip(" ")
        transferName = transferName.lstrip(" ")
        varG.studyOutList.append("\t" + "\t" + "transferName=" + transferName)
		

        fP1 = debitAttributeList[1].find("to moms sav")
        fP2 = transferName.find("schneider a")
        fP3 = debitAttributeList[1].find("prime checking")


        if fP1 >= 0 or fP2 >= 0:
            if fP2 >= 0:
#print("\t","\t","IFchg transferName=",transferName)
                tNameList = transferName.split(" ")
                lLen = len(tNameList)
                transferName = transferName[:fP2+11]
                if lLen > 2:
                    yAccount = tNameList[-2]
            if fP3 == -1:
                if transferName in varG.convertOwnerDict:
                    transferName = varG.convertOwnerDict[transferName]
            else:
                yAccount = "checking"

            varG.studyOutList.append("\t" + "\t" + "IFchg transferName=" + transferName + \
                  " lLen=" + str(lLen) + " yAccount=" + yAccount)

	
        tNameList = transferName.split(" ")
        tNLen = len(tNameList)

        varG.studyOutList.append("\t" + "\t" + "tNLen=" + str(tNLen) + " tNameList=" + str(tNameList))
        if tNLen > 2:
            transferName = tNameList[0] + " " + tNameList[1]
            varG.studyOutList.append("\t" + "\t" + "tNl transferName=" + transferName)
            fP1 = debitAttributeList[0].find("checking")
            fP2 = debitAttributeList[0].find("savings")
            if yAccount == "":
                if fP1 >= 0:
                    yAccount = "checking"
                elif fP2 >= 0:
                    yAccount = "savings"
                varG.studyOutList.append("\t" + "\t" + "tNl yAccount=" + yAccount)


        varG.studyOutList.append("\t" + "  debitAttributeList[1]=" +  str(debitAttributeList[1]) + \
              " varG.inTHelpersList=" + str(varG.inTHelpersList))
        if lLen >= 0:
            for x, y in enumerate(varG.inTHelpersList):
                fP1 = debitAttributeList[1].find(y)
                varG.studyOutList.append("\t" + "\t" + "fP1=" + str(fP1) + "x=" + str(x) + " y=" + y)
                if fP1 >= 0:
                    fP2 = fP1 + len(y)
                    varG.studyOutList.append("\n" +  "\t" + "fP2=" + str(fP2))
                    transDescription =  debitAttributeList[1][fP2+1:]
                    varG.studyOutList.append("\t" + "\t" + "1 transDescription=" + transDescription)
                    y = y.lstrip(" ")
                    y = y.rstrip(" ")
                    fP1 = y.find(" ")
                    yAccount = y[fP1+1:]

                varG.studyOutList.append("\t" + "\t" + "yAccount=" + yAccount)



        if varG.headerList[0] == "Jeanette":
            fMom = transDescription.find("mom")
            if fMom >= 0:
                transferName = varG.headerList[0] + "mom"
                if transferName in varG.convertOwnerDict:
                    transferName = varG.convertOwnerDict[transferName]

        varG.studyOutList.append("\t" + "varG.headerList[0]=" + str(varG.headerList[0]))
        varG.studyOutList.append("\n" + "\t" + "S- varG.headerList[0]=" + str(varG.headerList[0]) + \
              " transferName=" +  transferName + "transSource=" + transSource + \
              " transDestination=" + transDestination)
        if varG.headerList[0] == "JMmom" or varG.headerList[0] == "ASMom":
            varG.studyOutList.append("\t" + "\t" + "1 varG.headerList[0]=" + str(varG.headerList[0]))
            if varG.headerList[3] == "Checking":
                if amt_p1 == "-":
                    if transferName in varG.inTHelpersDict:
                        transDestination = varG.inTHelpersDict[transferName][0] + \
                            " " +  yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                        varG.studyOutList.append("\t" + "\t" + "\t" + "a- transSource=" + transSource + \
                              " transDestination=" + transDestination)
                    else:
                        transDestination = transferName + " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                        varG.studyOutList.append("\t" + "\t" + "\t" + "b- transSource=" + transSource + \
                              " transDestination=" + transDestination)
                    varG.studyOutList.append("\t" + "\t" + "1- transSource=" + transSource + \
                          " transDestination=" + transDestination)
                else:
                    if transferName in varG.inTHelpersDict:
                        print("varG.inTHelpersDict[transferName]=",\
                              varG.inTHelpersDict[transferName])
                        transSource = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    else:
                        transSource = transferName + " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    varG.studyOutList.append("\t" + "\t" + "2- transSource=" + transSource + \
                          " transDestination=" + transDestination)


            elif varG.headerList[3] == "Savings":
                if amt_p1 == "-":
                    if transferName in varG.inTHelpersDict:					
                        transDestination = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                    else:
                        transDestination = transferName + " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                    varG.studyOutList.append("\t" + "\t" + "3- transSource=" + transSource + \
                          " transDestination=" + transDestination)
                else:
                    varG.studyOutList.append("\t" + "4-I: transferName=" + transferName)
                    if transferName in varG.convertOwnerDict:
                        transSource = varG.convertOwnerDict[transferName] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    elif transferName in varG.inTHelpersDict:
                        transSource = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    else:
                        transSource = transferName + " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    varG.studyOutList.append("\t" + "\t" + "4- transSource=" + transSource + \
                          " transDestination=" + transDestination)

            varG.studyOutList.append("\n" + "\t" + "F- transSource=" + transSource + " transDestination=" + \
                  transDestination)
		
        elif varG.headerList[0] == "Jeanette":
            print("\t" + "\t" + "2 varG.headerList[0]=" + str(varG.headerList[0]) + \
                  " transferName=" + transferName)
            if varG.headerList[3] == "Checking":
                if amt_p1 == "-":
                    if transferName in varG.inTHelpersDict:
                        transDestination = varG.inTHelpersDict[transferName][0] + \
                            " " +  yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                        varG.studyOutList.append("\t" + "\t" + "\t" + "5a- transSource=" + transSource + \
                              " transDestination=" + transDestination)
                    else:
                        transDestination = transferName + " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                        varG.studyOutList.append("\t" + "\t" + "\t" + "5b- transSource=" + transSource + \
                              " transDestination=" + transDestination)
                    varG.studyOutList.append("\t" + "\t" + "5- transSource=" + transSource + \
                          " transDestination=" + transDestination)
                else:
                    if transferName in varG.inTHelpersDict:
                        varG.studyOutList.append("varG.inTHelpersDict[transferName]=" + \
                              str(varG.inTHelpersDict[transferName]))
                        transSource = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    else:
                        transSource = transferName + " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                    varG.studyOutList.append("\t" + "\t" + "5- transSource=" + transSource + \
                          " transDestination=" + transDestination)

            elif varG.headerList[3] == "Savings":
                if amt_p1 == "-":
                    if transferName in varG.inTHelpersDict:
                        transDestination = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                    else:
                        transDestination = transferName + " " + yAccount
                        transSource = varG.headerList[0] + " " + varG.headerList[3]
                    varG.studyOutList.append("\t" + "\t" + "6- transSource=" + transSource + \
                          " transDestination=" + transDestination)
                else:
                    fP10 = transDescription.find("close out")
                    varG.studyOutList.append("\t" + "7-I: transferName=" + transferName + \
                          " transAction=" + transAction + " yAccount=" + yAccount)
                    if transAction == "recurring transfer" or fP10 >= 0:
                        tNfound = ""
                        varG.studyOutList.append("\t" + "7-I-a: transferName=" + transferName)
                        for key in varG.convertOwnerDict:
                            #transferName = transferName.lstrip(" ")
                            #transferName = transferName.rstrip(" ")
                            varG.studyOutList.append("\t" + " transferName=" + transferName + " key=" + \
                                  key + " varG.convertOwnerDict[key]=" + \
                                  str(varG.convertOwnerDict[key]))
                            if varG.convertOwnerDict[key] == transferName:
                                transSource = key + " " + yAccount
                                tNfound = "yes"
                        if tNfound != "yes":
                            transSource = transferName + " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                        varG.studyOutList.append("\t" + "7-I-a: transferName=" + transferName)
                    
                    elif fMom >= 0 and transferName in varG.convertOwnerDict:           
                        varG.studyOutList.append("\t" + "7-I-b: transferName=" + transferName)
                        transSource = varG.convertOwnerDict[transferName] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                        varG.studyOutList.append("\t" + "7-I-b: transferName=" + transferName)
                    elif transferName in varG.inTHelpersDict:
                        varG.studyOutList.append("\t" + "7-I-c: transferName=" + transferName)
                        transSource = varG.inTHelpersDict[transferName][0] + \
                            " " + yAccount
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                        varG.studyOutList.append("\t" + "7-I-c: transferName=" + transferName)
                    else:
                        if transferName in varG.convertOwnerToFirstDict:
                            transferName = varG.convertOwnerToFirstDict[transferName]
                        varG.studyOutList.append("\t" + "7-I-d: transferName=" + transferName)
                        transSource = transferName + " " + yAccount                        
                        transDestination = varG.headerList[0] + " " + \
                            varG.headerList[3]
                        varG.studyOutList.append("\t" + "7-I-d: transferName=" + transferName)
					
                    varG.studyOutList.append("\t" + "\t" + "7- transSource=" + transSource + \
                          " transDestination=" + transDestination)
		

        if transSource == "Julia Checking" \
            and transDestination == "ASmom checking":
                
            transDescription \
                = uETL.getDictCategory(str(transAmount))
            varG.studyOutList.append("\t" + "\t" + "2 transDescription=" + transDescription)
            transCategory = "funds to " + transDestination
            #transCategory = uETL.getDictCategory(transDescription,  varG.inTHelpersCatDict)
        else:
            if hdrOwnerAccount == transSource \
                or transDestination == "ASmom checking":
                    
                transCategory \
                    = uETL.getDictCategory(transDestination)
            else:
                transCategory \
                    = uETL.getDictCategory(transSource)


#transDescription ---> extract type requires qualification     
#--> ONLINE TRANSFER TO MASSO J REF #   ---> [0]	                                                               
#    IB04Y8GT68 EVERYDAY CHECKING JS TO MOMS CHKG RETIREMENT IN    ---> [1]	                                                               
#                        --------															       
#--> ONLINE TRANSFER FROM MASSO J REF #															       
#    IB04TB4C33 EVERYDAY CHECKING TO JS CHKG FOR TO 500														       
#                        --------
	
#list [1] value --> used 
#--> stores list values in secondary list with each [1] value as a separate 
#[0...] value in secondary list 
		#print("\t","a/t:  debitAttributeList[1]=", debitAttributeList[1])
        
        transValue = str( debitAttributeList[1])
        transList = transValue.split(" ")
        #print("\t","\t","transList=",transList," transList[0]=",transList[0])

        if "checking" in transList or "savings" in transList:
            fP1 = transValue.find("retirement")
            fP2 = transValue.find("trs and s")
            fP3 = transValue.find(" 500") 
            fP4 = transValue.find("to500")
            fP5 = transValue.find("js chk")  
            fP6 = transValue.find("to moms sav")
            fP7 = transValue.find("hocheim car claim")
            fP8a = transValue.find("xxxxxx2969 ref #")
            fP8b = transValue.find("up jm savings")
            fP9 = transDescription.find("bml over trnsfr")
            fP9b = transDescription.find("overage")
            fP10 = transDescription.find("close out")
            fP11a = transDescription.find("future")
            fP11b = transDescription.find("to savings")
            fP12a = transDescription.find("overdraf")
            fP12b = transDescription.find("next month vis")
            fP13 = transDescription.find("tax exp to chkg")
            fP14 = transDescription.find("double tr")
            fP15a = transDescription.find("bml")
            fP15b = transDescription.find("payp")
            

			 
			#print("\t","\t","checking in transList    transList=",transList)     
            if fP1 >=0 or fP2 >=0:
                transDescription = "retirement funds to mom"
                transCategory \
                    = uETL.getDictCategory(transDescription)
            elif fP3 >= 0 or fP4 >= 0:                                       
                transDescription = "JS checking up to 500"
                transCategory \
                    = uETL.getDictCategory(transDescription) 
            elif fP5 >= 0:
                transDescription = "JS checking in"
                transCategory \
                    = uETL.getDictCategory(transDescription)  
            elif fP6 >= 0:
                transDescription = "mom checking down to 1000"
                transCategory \
                    = uETL.getDictCategory(transDescription)
            elif fP7 >= 0:
                transDescription = "hocheim car claim payment"
                transCategory = \
                    uETL.getDictCategory(transDescription)
            elif fP8a >= 0:
                transDescription = transValue[fP8b:]
                transCategory = "transfer out funds"
            elif fP9 >= 0 or fP9b >= 0:
                transSource =  varG.headerList[0] + " " +  yAccount
                transCategory = "over transfer correction"
            elif fP10 >= 0:
                transCategory = "account close out transfer"

            elif fP11a >= 0 or fP11b >= 0:
                transCategory = "future expense funds" 
            elif fP12a >= 0 or fP12b >= 0:
                transCategory = "account overdraft prevention"
            elif fP13 >= 0:
                transCategory = "tax expense funds"
            elif fP14 >= 0:
                transCategory = \
                    uETL.getDictCategory(transDescription)
            elif fP15a >= 0 or fP15b >= 0:
                transCategory = "checking PayPal Payment"

            varG.studyOutList.append("\t" + "\t" + "3 transDescription=" \
                + transDescription + " transCategory=" + transCategory \
                + " fP14=" + str(fP14))

			#print("\t","\t","checking in transList     varG.headerList[3]=", varG.headerList[3])
            fP1 = transValue.find("for jm")
            fP2 = transValue.find("bill")
            fP3 = transValue.find("reimb")
            fP4 = debitAttributeList[1].find("prime checking")

            varG.studyOutList.append("\n" + "\t" + "desc/cat: amt_p1= " + str(amt_p1) + " varG.headerList[0]=" + \
                  str(varG.headerList[0]) + " fP4=" + str(fP4))


            if varG.headerList[0] == "Julia" and amt_p1 != "-":
                varG.studyOutList.append("fP4=" + str(fP4))
                if fP4 >= 0:
                    fP4 = debitAttributeList[1].find("checking")
                    varG.studyOutList.append("\n" + "\t" + "Julia: amt_p1= " + str(amt_p1) + " varG.headerList[0]=" + \
                          str(varG.headerList[0]) + " fP4=" + str(fP4))
                    transDescription = debitAttributeList[1][fP4+9:]
                    varG.studyOutList.append("\t" + "\t" + "4 transDescription=" + transDescription)
                    transCategory = "reimbursement from anthony"
			
            if varG.headerList[0] != "Jeanette" and amt_p1 != "-":
                if fP1 >= 0:
                    transCategory = "reimbursement from jeanette"
                elif fP2 >= 0:
                    transCategory = "reimbursement from jeanette"
                elif fP3 >= 0:
                    transCategory = "reimbursement from jeanette"

            elif varG.headerList[0] != "Jeanette" and amt_p1 == "-":
                if fP1 >= 0:
                    transCategory = "reimbursement for jeanette"
                elif fP2 >= 0:
                    transCategory = "reimbursement for jeanette"
                elif fP3 >= 0:
                    transCategory = "reimbursement for jeanette"
			
            elif varG.headerList[0] == "Jeanette" and amt_p1 == "-":
                if fP1 >= 0:
                    transCategory = "reimbursement for mom"
                elif fP2 >= 0:
                    transCategory = "reimbursement for mom"
                elif fP3 >= 0:
                    transCategory = "reimbursement for mom"

            elif varG.headerList[0] == "Jeanette" and amt_p1 != "-":
                if fP1 >= 0:
                    transCategory = "reimbursement from mom"
                elif fP2 >= 0:
                    transCategory = "reimbursement from mom"
                elif fP3 >= 0:
                    transCategory = "reimbursement from mom"
            else: 
                if  varG.headerList[3] == "Savings" and "checking" in transList:
                    transCategory = "funds from checking"
                elif  varG.headerList[3] == "Checking" and "savings" in transList:
                    transCategory = "funds to savings"

            if fP8b >=0:
                transCategory = "up jm savings"
                transCategory = uETL.getDictCategory(transCategory)

		
		
        if transAction == "recurring transfer":
            transDescription = "automated transfer from " + transSource
            transCategory = "auto transfer funds"


        varG.studyOutList.append("\t" + "\t" + "transDescription=" + transDescription)
        transDescription = transDescription.lstrip(" ")
        transDescription = transDescription.rstrip(" ")
        
        return transAction, transSource, transDestination, transDescription, \
            transCategory 
    
    
    def extract_Social_Security(transList):

        extractValue1 = ""
        extractValue2 = ""
        p1 = ""
        p2 = 0
        p4 = 0

		#print("\n","\t","ssn:  transList=",transList,"\n")

#extractValue1 =s list values before wkValue
		
        transList[0] = "ssa1"
		
        p2 = transList.index("ssa")+1
        p1 = "right"
        #print("\t","\t","p1=",p1,"p2=",p2)
        extractValue2 = uETL.extractFromList(transList,p1,p2,p4)

        transList[0] = "ssa"
        p2 = transList.index("sec") + 1
        transList = transList[:p2] 
        p1 = "all"
        #print("\t","\t","p1=",p1,"p2=",p2)
        extractValue1 = uETL.extractFromList(transList,p1,p2,p4)

    #print("\t","ssn:  extractValue1=",extractValue1," extractValue2=",extractValue2,"\n")
		
        return extractValue1, extractValue2
    

    def extract_eDeposit(debitAttributeList,transAmount):

        transValue = ""
        transList = []

        p1 = ""
        p2 = 0
        p4 = 0
        fP1 = -1
        fP2 = -1
		
#return attributes
        transAction = ""

        transSource = ""
        transDestination = ""
        transDescription = ""
        transCategory = ""
        transLocation = ""

        transValue = str(debitAttributeList[0])
        transList = transValue.split(" ")
        print("\n","\t","eDeposit-IN: transList=",transList," transList[0]=",\
              transList[0]," varG.headerList[0]=",varG.headerList[0]," varG.headerList[3]=",varG.headerList[3])
        print("\t","\t","eDeposit-IN: transAction=",transAction," transSource=",\
              transSource," transDestination=",transDestination, \
              " transDescription=",transDescription," transCategory=",\
              transCategory," transLocation=",transLocation)
        p2 = debitAttributeList[0].find("branch/store")
        if p2 >= 0:
            transList = debitAttributeList[0].split(" ")
            p1 = "left"
            p2 = transList.index("branch/store")
            transAction = uETL.extractFromList(transList,p1,p2,p4)
            fP1 = transAction.find("depo")   #transAction = "deposit" or "edeposit"
            print("\n","\t","find deposit: fP1=",fP1,"fP1"," transAction=",\
                  transAction)
            fP2 = transAction.find("/")
            if fP1 >= 0:
                transAction = transAction[fP1:]
            if fP2 >= 0:
                transAction = transAction[:fP2-1]
                transSource = varG.headerList[0]

            transCategory = uETL.getDictCategory(str(transAmount))
            if transCategory != "":
                dictKey = transCategory + str(transAmount)
                transDescription = uETL.getDictCategory(dictKey)
                if transDescription == "":
                    transDescription = "in Branch Fund Deposit"	
            else:
                transDescription = "in Branch Fund Deposit"
                transCategory = "received funds deposited"

            print("\t","a/f 1 transAction=",transAction)

        if varG.headerList[3] == "Checking":
            if fP1 == 0:      # in transAction = "deposit"				
                transSource = varG.headerList[0]
                transDescription =  "in Branch Fund Deposit"
                transCategory = uETL.getDictCategory(str(transAmount))
                if transCategory == "":
                    transCategory = "received funds deposited"
            else:
                transSource = "BCP renters"
                transDescription = "renter payments"
                transCategory = uETL.getDictCategory(transSource) 

        transDestination = varG.headerList[0] + " "  + varG.headerList[3]

        fP1 = debitAttributeList[0].find(" am ")
        fP2 = debitAttributeList[0].find(" pm ")
        #print("\t","\t","fP1=",fP1," fP2=",fP2)
        if fP1 >= 0 or fP2 >= 0:
            p2 = fP1 + fP2 + 5
            transLocation = debitAttributeList[0][p2:]
            p2 = len(transLocation)
            transLocation = transLocation[:p2-5]

        print("\t","\t","eDeposit-IN: transAction=",transAction," transSource=",\
              transSource," transDestination=",transDestination, \
              " transDescription=",transDescription," transCategory=",\
              transCategory," transLocation=",transLocation)

        return transAction, transSource, transDestination, transDescription, \
            transCategory, transLocation
 
    
    def attributesOnlineBillPay(p2, p4, transList):

        transAction = ""
        transSource = ""
        transDestination = ""
        transDescription = ""
        transCategory = ""
		
        print("\t","billPay: transList=",transList)
		
#Step 1:  determine transSource and transDestination Values
# 
        transAction = transList[p2] + " " + transList[p2+1] + " " + \
            transList[p4]

        transSource = varG.headerList[0]  + " " + varG.headerList[3]

        p1 = "middle"
        p2 =+ 1   #p2 and p4 transList positions supplied by statement that invoked billpay method
                       #p2 =s start and p4 =s stop

        transDestination = uETL.extractFromList(transList,p1,p2,p4)

        transCategory = uETL.getDictCategory(transDestination)

        if transAction == "":
            transAction = "Bill Pay"

        return transAction, transSource, transDestination, transDescription, \
            transCategory
            

    