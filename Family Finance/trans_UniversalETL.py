# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:56:23 2019

@author: Jeanette
"""

from variables_Global import VarGlobals as varG
#import calendar
  
class Universal:   #11 methods within class UniversalB
    
    def splitCheck(iValue):
        iValue = iValue
        
        sourceBefore = ""
        sourceAfter = ""
        splitSource = ""

        lenValue = len(iValue) 
        i = 0
        while i < lenValue:
            if str.isalpha(iValue[i]):
                i += 1
                continue
            else:
               # print('iValue[i]=',iValue[i],'splitList=',varG.splitList)
                if iValue[i] in varG.splitList:
                    sourceBefore = iValue[:i]
                    sourceAfter = iValue[i+1:]
    					
                    #print("\n","\t","y=",iValue , " iValue[i]=", iValue[i], \
                    #      " sourceBefore=",sourceBefore," sourceAfter=",sourceAfter)
                          #" sourceSet=",sourceSet)
    													
                    if str.isalpha(sourceBefore) and sourceAfter == "":
                        splitSource = sourceBefore
                        break
#special character check like "-""                     
                    if str.isalpha(sourceBefore) and str.isalpha(sourceAfter):  
                        splitSource =  sourceBefore + " " + sourceAfter
                        if iValue[i] == "&":
#  alpha before and after special character = keep                            
                            splitSource = sourceBefore + " & " + sourceAfter                                            
                            break
#special character in middle of string with alpha before and not alpha after                        
                        elif str.isalpha(sourceBefore):      
                            splitSource = sourceBefore    # keep alpha before 
                            break
#special character with numeric before and after,  don't keep                        
                        else:
                            splitSource = ""         
                            break
                    else:
                        splitSource = iValue[:i]
                        break
            i += 1
    
        #print("\t","iValue =",iValue ," splitSource=",splitSource)
    
        return splitSource

    
    def get_transAction(transDestination):

        transDestination = transDestination


        transAction = ""

        for key in varG.inTHelpersDict:
            #hKList = list(inTHelpersDict.get(y))
            #print("key=",key," varG.inTHelpersDict[key]=",\
            #      varG.inTHelpersDict[key], " transDestination=",\
            #      transDestination) 
            if transDestination in varG.inTHelpersDict[key]: 
                fP1 = key.find("check")
                
                if fP1>= 0:	
                    fP1 = transDestination.find("check")		
                    if fP1 >= 0:
                        transAction = key
                        break
                    else:
                        transAction = key
                elif "default" in varG.inTHelpersDict[key]:
                    if fP1 >= 0:
                        transAction = key

        return transAction


    def extractFromList(transList,p1,p2,p4):
        transList = transList
        extractValue = ""
        tL_len = 0
        tL_len = len(transList)-1
        not_alpha = ""

        for x, y in enumerate(transList):
            #print("\t","y=",y," extractValue=",extractValue)
            if p1 == "all":
                extractValue =  extractValue + " " + y
                continue

            if p1 == "right":
                if x >= p2:
                    extractValue =  extractValue + " " + y
                    continue

            if p1 == "left":
                if x <= p2:
                    extractValue =  extractValue + " " + y
                    continue
                else:
                    break

            if p1 == "middle":
                if x > p2 and x < p4:
                    extractValue =  extractValue + " " + y
                    continue
                elif x == p4:
                    break

            if p1 == "right to not alpha" and x >= p2:
                if str.isalpha(y):
                    extractValue =  extractValue + " " + y
                    continue
                else:
                    break

            if p1 == "not alpha right to end":
                if str.isalpha(y) is False:
                    not_alpha = "y"
                elif not_alpha == "y":
                    extractValue =  extractValue + " " + y
                continue


        #print("\n","\t","y=",y," extractValue=",extractValue,"\n")

        extractValue = extractValue[1:]   #--> to remove leading " "
        
        return extractValue


    def getDictCategory(transFind):
        transFind = transFind

        dictCategory = ""

#	"bill me later":"Jeanette PayBack","wells fargo cred":"Jeanette PayBack","paypal credit":"Jeanette PayBack", \
#	"catholic life insurance":"insurance","equitable insurance":"insurance", \
#	"chase bank":"moms expense", \
#	"al wiatrek":"irs taxes", \
#	"cpenergy":"house utilities","poth - water":"house utilities", \
#	"retirement funds to mom":"transfer in funds", \
#	"raul bosquez":"rental expense","borrego creek properties":"rental income", \
#	"three oaks wsc":"farm expense","farmers gin co.":"farm expense","lyssy & eckel feeds, inc.":"farm expense"}


        if transFind in varG.inTHelpersCatDict:
            dictCategory = varG.inTHelpersCatDict[transFind][0]

        #print("\t"," transFind=",transFind,\
        #      " dictCategory=",dictCategory)
        
        return dictCategory


    def getDictCategoryByKey(transFind):
        transFind = transFind

        dictCategory = ""
        varG.studyOutList.append("\n" + "\t" + \
            " getDictCategoryByKey-: transFind=" + transFind)

        for key in varG.inTHelpersCatDict:
            #print("key=",key, " transFind=",transFind,\
            #      " varG.inTHelpersCatDict[key]=",varG.inTHelpersCatDict[key]) 
            varG.studyOutList.append("\n" + "\t" + "\t" + \
                " getDictCategoryByKey-: key=" + key + \
                " keyValue=" + str(varG.inTHelpersCatDict[key]))
            
            if transFind in varG.inTHelpersCatDict[key]:
                dictCategory = key
                break
        varG.studyOutList.append("\n" + "\t" + "\t" + \
            " getDictCategoryByKey-: dictCategory=" + dictCategory)

        #print("\t"," transFind=",transFind,\
        #      " dictCategory=",dictCategory)

        return dictCategory


    def findListValueInDescription(listPayReimbDestinations,transDescription):
        
        
        transDescription = transDescription
        listPayReimbDestinations = listPayReimbDestinations

        fPvalue = ""
        fP = 0

        for x, y in enumerate(listPayReimbDestinations):
            y = y.lstrip(" ")
            y = y.rstrip(" ")
            fP = transDescription.find(y)

            if fP >=0:
                #print("find visa=",y)
                if y == "visa":
                    fPvalue = "fargo cred"
                    #print("found visa=",y," fPvalue=",fPvalue)
                elif y == "amazon":
                    fPvalue = "gecrb/amazon"
                    #print("found amazon=",y," fPvalue=",fPvalue)
                else:
                    fPvalue = y
                break

        
        return fPvalue


    def cleanLocation(transLocation):
        transLocation = transLocation.rstrip(" ")
        transLocation = transLocation.lstrip(" ")

        tl_List = transLocation.split(" ")
        #print("\n","\n","\t","cleanLocation-S:  transLocation=",\
        #      transLocation,"\n","\t","\t","\t","tl_List=",tl_List,"\n")

        tl_len = len(tl_List)
        if tl_len > 2:
            tl_1 = False
            tl_2 = False
            tl_3 = False
            #print("\n","\t","-->1  tl_len=",tl_len," tl_2=",tl_2,\
            #      " tl_3=",tl_3," transLocation=",transLocation)
            for x, y in enumerate(tl_List):
                if y != "" and tl_1 == False:
                    tl_1 = True
                    transLocation = y
                    #print("\n","\t","-->2  tl_len=",tl_len," tl_2=",tl_2,\
                    #      " tl_3=",tl_3," x=",x," y=",y," transLocation=",\
                    #      transLocation)
                    continue
                elif y != "" and tl_2 == False:
                    tl_2 = True
                    tl_len = len(y)
                    if tl_len == 2:
                        transLocation = transLocation + "  " + y
                        #print("\n","\t","-->3  tl_len=",tl_len," tl_2=",tl_2,\
                        #      " tl_3=",tl_3," x=",x," y=",y," transLocation=",\
                        #      transLocation)
                        break
                    else:
                        transLocation = transLocation+ " " + y
                        #print("\n","\t","-->4  tl_len=",tl_len," tl_2=",tl_2,\
                        #      " tl_3=",tl_3," x=",x," y=",y," transLocation=",\
                        #      transLocation)
                        continue
                elif y != "" and tl_3 == False:
                    tl_len = len(y)
                    if tl_len == 2:
                        transLocation = transLocation + "  " + y
                        #print("\n","\t","-->5  tl_len=",tl_len," tl_2=",tl_2,\
                        #      " tl_3=",tl_3," x=",x," y=",y," transLocation=",\
                        #      transLocation)
                    else:
                        transLocation = transLocation+ " " + y
                        #print("\n","\t","-->6  tl_len=",tl_len," tl_2=",tl_2,\
                        #      " tl_3=",tl_3," x=",x," y=",y," transLocation=",\
                        #      transLocation)
                        break

        elif tl_len == 1:
            transLocation = tl_List[0]
            #print("\n","\t","-->7  tl_len=",tl_len," tl_List[0]=",tl_List[0],\
            #      " transLocation=",transLocation)
        else:
            tl_len = len(tl_List[1])
            if tl_len == 2:
                transLocation = tl_List[0] + "  " + tl_List[1]
                #print("\n","\t","-->8  tl_len=",tl_len," tl_List[0]=",\
                #      tl_List[0]," tl_List[1]=",tl_List[1]," transLocation=",\
                #      transLocation)
            elif tl_len == 1:
                transLocation = tl_List[0] + "  " + 'TX'    
            else:
                transLocation = tl_List[0] + " " + tl_List[1]
                #print("\n","\t","-->9  tl_len=",tl_len," tl_List[0]=",\
                #      tl_List[0]," tl_List[1]=",tl_List[1]," transLocation=",\
                #      transLocation)


        tl_List = transLocation.split(" ")		
        tl_len = len(tl_List[0])

        #print("\n","\n","\t","-->12: tl_len=",tl_len," transLocation=",\
        #      transLocation,"\n","\t","\t","\t","tl_List=",tl_List,"\n")
        if tl_len > 2:
            tl_len = len(tl_List[-1])
            if tl_len != 2:
                transLocation = transLocation + "  TX"
                #print("\n","\n","\t","-->13:  tl_len=",tl_len,\
                #      " transLocation=",transLocation)	
                if tl_List[0] == "COLLEGE":
                    transLocation = "COLLEGE STATION  TX"
                    #print("\n","\n","\t","-->14:  tl_List[0]=",tl_List[0],\
                    #      " transLocation=",transLocation)
                elif transLocation == "PAST DUE  TX":
                    transLocation = "crCard PAST DUE"
                    #print("\n","\n","\t","-->15:  transLocation=",\
                    #      transLocation)

        transLocation = transLocation.upper()

        #print("\n","\n","\t","cleanLocation-E:  transLocation=",\
        #      transLocation,"\n")


        return transLocation


    def getPayerAttributes(transSource,transDate):
        
        transSource = transSource
        transDate = transDate
        hdrAccount = varG.headerList[3]

        helpKey1 = transSource
        helpKey2 = transSource + str(transDate)
        helpKey3 = transSource + hdrAccount

        fP1 = transSource.find("ville Elec")
        fP2 = transSource.find("arnes Elec")
        fP3 = transSource.find("USPS")

        varG.studyOutList.append("\n" + "\t" + "getpayerAttributes: transSource=" + \
              transSource + " transDate=" + transDate + " fP1=" + str(fP1) + " fP2=" + str(fP2))
        
        if fP1 >= 0 or fP2 >= 0 or fP3 >= 0:
            dte_List = transDate.split("/")
            varG.studyOutList.append("\n" + "\t" + "\t" + "str(dte_List[0])=" + str(dte_List[0]) + \
                  " str(dte_List[1])=" + str(dte_List[1]))
            if int(dte_List[0]) <= 2018 and int(dte_List[1]) <= 6:
                helpKey1 = "PreJuly" + helpKey1
                helpKey2 = "PreJuly" + helpKey2
                helpKey3 = "PreJuly" + helpKey3
                varG.studyOutList.append("\n" + "\t" + "\t" + "helpKey1=" + helpKey1)

        payer = ""
        reimburser = ""
        yesPayer = False
        prList = []

        if helpKey1 in varG.inTHelpersPayReimbDict:
            prList = varG.inTHelpersPayReimbDict[helpKey1]
            payer = prList[0]
            reimburser = prList[1]
            yesPayer = True
            varG.studyOutList.append("\n" + "\t" + "\t" + "-->1" + " helpKey1=" + helpKey1)
        elif helpKey2 in varG.inTHelpersPayReimbDict:
            prList = varG.inTHelpersPayReimbDict[helpKey2]
            payer = prList[0]
            reimburser = prList[1]
            yesPayer = True
            varG.studyOutList.append("\n" + "\t" + "\t" + "-->2" + " helpKey2=" + helpKey2)
        elif helpKey3 in varG.inTHelpersPayReimbDict:
            prList = varG.inTHelpersPayReimbDict[helpKey3]
            payer = prList[0]
            reimburser = prList[1]
            yesPayer = True
            varG.studyOutList.append("\n" + "\t" + "\t" + "-->3" + " helpKey3=" + helpKey3)


        payer = payer.strip(" ")
        reimburser = reimburser.strip(" ")
        
        varG.studyOutList.append('\n' + 'payer=' + payer + ' reimburser=' + \
            reimburser + ' yesPayer=' + str(yesPayer))


        return  payer, reimburser, yesPayer


    def updateCrCardPayReimbDict(dict_PayReimbCrCard,sqlTuple_PayReimb,\
        prevDictKey,pr_DictList):
        
        dict_PayReimbCrCard = dict_PayReimbCrCard
        sqlTuple_PayReimb = sqlTuple_PayReimb
        prevDictKey = prevDictKey
        pr_DictList = pr_DictList

        #print("\n","\t","updateCrCardPayReimbDict-S:  dict_PayReimbCrCard=",\
        #      dict_PayReimbCrCard,"\n","\t"," sqlTuple_PayReimb=",\
        #      sqlTuple_PayReimb)		

#sqlTuple_PayReimbCrCard
# [0] = prtransID, [1] = trans date, [2] = trans amount, [3] = trans source, 
# [5] = crCard [6] = payer [7] = reimburser [8] date reimbursed 
# [9] amt reimbursed [10] now()

# [0] = prtransID, [1] = trans date, [3] = trans source, [5] = crCard 
# [6] = reimburser [7] date reimbursed [8] amt reimbursed

        dte_List = []
        dte_List = sqlTuple_PayReimb[1].split("/")
        #print("\n","\t","\t","dte_List=",dte_List)	

        dictKey = dte_List[0] + dte_List[1]
        #print("\n","\t","\t","dictKey=",dictKey," prevDictKey=",prevDictKey)

        if prevDictKey == 0:
            pr_DictList.append(sqlTuple_PayReimb)
            #print("\n","\t","\t","1 pr_DictList=",pr_DictList)	
        elif dictKey == prevDictKey:
            pr_DictList.append(sqlTuple_PayReimb)
            #print("\n","\t","\t","2 pr_DictList=",pr_DictList)
        else:
            dict_PayReimbCrCard[prevDictKey] = pr_DictList
            pr_DictList = []
            pr_DictList.append(sqlTuple_PayReimb)
            #print("\n","\t","\t","3 pr_DictList=",pr_DictList)

        prevDictKey = dictKey

        #print("\n","\t","updateCrCardPayReimbDict-E:  dict_PayReimbCrCard=",\
        #      dict_PayReimbCrCard," prevDictKey=",prevDictKey,\
        #      " pr_DictList=",pr_DictList)	

        
        return dict_PayReimbCrCard, prevDictKey, pr_DictList 
    
   
    def cleanseDescription(description):
        description = str(description)

        description = description.strip('"')
        description = description.rstrip()
		
        description = description.replace("  ","")
		
        findPosition = description.find('"')

        if findPosition >= 0:     #value = -1 when not found
            findPosition = findPosition + 1
            description = description[findPosition:] 
            
        return description
  
    
    def firstPositionSplitKeepRight(transSource):
        
        varG.studyOutList.append('\n' + 'firstPositionSplitKeepRight:  ' + \
            'transSource=' + transSource + ' transSource[0]=' + '\n' + \
            transSource[0] + '\n' + 'varG.firstPositionSplitKeepRightList=' + \
            str(varG.firstPositionSplitKeepRightList) + '\n')
        #chkValue = transSource[0]
            
        if transSource[0] in varG.firstPositionSplitKeepRightList:
            transSource = transSource[1:]
            
        return transSource
        
    
        