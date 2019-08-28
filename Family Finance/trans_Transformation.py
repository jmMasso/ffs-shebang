# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:43:46 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG
from trans_UniversalETL import Universal as uETL
from trans_CreditTransform import Credit as crT
from trans_DebitTransform import Debit as dbT
from trans_JMChkTransform import Fields as jmchkF

class Date:
    
    def __init__(self,date):
        self.date = date
        
        dateSplit = []
    
        dateSplit = self.date.split("/")	 #zero pad the mm and dd
        dateSplit[0] = str(dateSplit[0]).zfill(2) 
        dateSplit[1] = str(dateSplit[1]).zfill(2)
    
        self.dateYearFirst = str(dateSplit[2]) + "/" + str(dateSplit[0]) \
            + "/" + str(dateSplit[1])
            
        #print('self.dateYearFirst=',self.dateYearFirst)

    
        
class Amount:
    
    def __init__(self,amount):
        self.amount = amount
        
        dP = self.amount.find("$")
        mP = self.amount.find("-")
        
        if dP >= 0:
            self.amount = self.amount[dP+1:]
            cP = str(self.amount).find(",")
            if cP >= 0:
                varG.studyOutList.append("\n" + "\t" + \
                     "-->2 b/f - Amount Transform -->" +  str(self.amount) + "\n")
                self.amount = str(self.amount)[:cP] + str(self.amount)[cP+1:]
                self.amount = str(self.amount).strip('"')
                self.amount = float(self.amount)
                varG.studyOutList.append("\n" + "\t" + \
                    "-->2 a/t - Amount Transform -->" +  str(self.amount) + "\n")
            if mP >= 0:
                self.amount = float(self.amount) * -1
                
                
        

    
class Location:
    
    def __init__(self,description,descriptionList):       
        self.description = description
        self.descriptionList = descriptionList
        
        self.transLocation = ""
                                  

        def extract_Visa_Location(descriptionList):	  
            self.descriptionList = descriptionList
            saveDescriptionList = self.descriptionList 
            
            nSL = 0
            nLI = 0
            iLL = 0
            fP = 0
            
            iL = 0
            iState = ""
            oL = len("ovilla")
            rL = len("red")
            lvList = []
            iValue  = ""
            iL = 0
            
            cityFirstofTwoList = ["cedar","red","glenn","waxahachie",\
                "dallas","college","san"]
            
            cityCheckConvertDict = {"sta":"station","stat":"station",\
                "stati":"station"}
            
            cityLastofTwoList = ["oak"]
            
            valueRejectStopList = ["oil","qt","ach","inc"]
            
            embedList = ["tx","denton","austin","duncanville","carrollton",\
                "waxahachie","karnes","floresville"]
            
#establish the number of indexes within list            
            nSL = len(self.descriptionList )-1   
            #print("\n","\t","start:  nSL=",nSL," self.descriptionList =",\
            #      self.descriptionList )
            iSL = nSL
                
#extract from uncleansed List            
                
            descLSP = 0
            while iSL > 0:   
                
                if self.descriptionList[iSL] != "":
                    iValue = self.descriptionList[iSL]
                
                    iValue = str.lower(iValue)
                    #print('01')
#convert iValue to the correct value for city  before remainig checks
                    if iValue in cityCheckConvertDict:   
                        iValue = cityCheckConvertDict.get(iValue)
                        #print('02')
                        #print('nLI=',nLI,'iSL=',iSL,' nSL=',nSL,' iValue=',\
                        #      iValue,' self.transLocation=',self.transLocation)
                    elif len(iValue) > 2:
                        fP = -1
                        fPcnt = 0
                        #print('nLI=',nLI,'iSL=',iSL,' nSL=',nSL,' iValue=',\
                        #      iValue,' self.transLocation=',self.transLocation)
                        for x, y in enumerate(embedList):

                            fP = iValue.find(y)
                            #print('y=',y,'fP=',fP)
                            if fP >= 0:
                                self.transLocation = y + " " + self.transLocation
                                descLSP = iSL
                                #print('02b')
                                fPcnt += 1
                        
                        #print('fPcnt=',fPcnt,'nLI=',nLI,'iSL=',iSL,' nSL=',nSL,\
                        #      ' iValue=',iValue,' self.transLocation=',\
                        #      self.transLocation)
                        if fPcnt > 0:
                            if len(iValue) > 2:
                                break
                            else:
                                iState = iValue
                                nLI = 1
                                iSL -= 1
                                continue
                    else:
                        y = 1
                        #print('nLI=',nLI,'iSL=',iSL,' nSL=',nSL,' iValue=', \
                        #      iValue,' self.transLocation=',self.transLocation)
                                
                else:
                    iValue = self.descriptionList[iSL]
                    #print('02d')
                    #print('nLI=',nLI,'iSL=',iSL,' nSL=',nSL,' iValue=',iValue,\
                    #      ' self.transLocation=',self.transLocation)
                    iSL -= 1
                    continue
                
                #First Check  going  right to  left list values
                if iSL == nSL:
                    iL = len(iValue)
                    if str.isalpha(iValue): 
#state abbreviation -  zero or 1+  follows for transLocation
                        if iL == 2:   
#to inform further checks of state placed in transLocation - no more that 2 more loads
                            iState = iValue    
#state abbreviation placed in transLocation
                            self.transLocation = iValue      
                            descLSP = iSL
                            #print('1')
                        else:
#city 1 of 1 or 2, placed in transLocation
                            self.transLocation = iValue       
                            descLSP = iSL
                            #print('2')
                
                        nLI = 1
                        iSL -= 1
                        continue
#iValue is not valid -  may want to break instead of continue  - ????
                    else:          
                        #print('3')
                        iSL -= 1   
                        continue
#remaining checks after First
                else:
                    iL = len(iValue)
                    if str.isalpha(iValue):
                        if nLI == 1 and iState == "":
# city double value check for indicating last value to place into transLocation
                            if iValue in cityFirstofTwoList:   
                                self.transLocation = iValue + " " \
                                    + self.transLocation
                                descLSP = iSL
                                nLI += 1
                                #print('4')
                                break
                            else:
                                #print('5') #Location value set during First Check
                                break
                        elif nLI == 1 and iState != "":
# state abbreviation in transLocation needing city
                            self.transLocation = iValue + " " \
                                + self.transLocation
                            descLSP = iSL
                            nLI += 1
                            iSL -= 1
                            #print('6')
                            continue
                        elif nLI == 2:
# city double value check for indicating last value to place into transLocation
                            if iValue in cityFirstofTwoList:   
                                self.transLocation = iValue + " " \
                                    + self.transLocation
                                descLSP = iSL
                                nLI += 1
                                #print('7')
                                break
                            else:  #Location value set during First Check
                                #print('8')
                                break
                        else:	#transLocation is set
                            #print('9')
                            break
                    else:   #transLocation is set
                        #print('10')
                        break
                iSL -= 1
                #print('11')                   
            
            self.transLocation = self.transLocation.rstrip(" ")
            self.transLocation = self.transLocation.lstrip(" ")

            if len(self.transLocation) == 2:
                iValue = str.lower(self.descriptionList[0])              
                if iValue in embedList:
                    self.transLocation = iValue + " " +  self.transLocation

            if self.transLocation != "":
                self.descriptionList  = self.descriptionList [:descLSP]
                iValue = self.descriptionList[0]
                #print("\n","\t","iValue=",iValue)
                fP = iValue.find('"')
                #print('12')
                if fP >= 0:     #value = -1 when not found
                    fP = fP + 1
                    iValue = iValue[fP:]
                    self.descriptionList[0] = iValue
                    #print('13')
                    #print("\n","\t","self.descriptionList[0]=",\
                    #      self.descriptionList[0]," iValue=",iValue)
            #print('14')
            #print("\t","end:  transLocation=",self.transLocation,\
            #      " self.descriptionList =",self.descriptionList)
            
            if self.transLocation in varG.crCardLocationRejectList:
                self.descriptionList = saveDescriptionList
                self.transLocation = ""
            else:
                self.transLocation = uETL.cleanLocation(self.transLocation)
    
            return self.transLocation, self.descriptionList
        
        
        def extract_Master_Location(description):
            self.description = description
    
            locationDict = {"6463":"Red Oak    Tx", \
                            "EDAR":"CEDAR","OLLEGE":"COLLEGE",\
                            "STATI":"STATION"}
    
            #print("\n","\t","Loc2: descriptionList=",descriptionList,\
            #      " description=",description)

            saveDescription = self.description
            self.transLocation = self.description[23:len(self.description)]
            self.description = self.description[:22]
                
            self.descriptionList = []
            s_value = self.description.lstrip('"')
            self.descriptionList = s_value.split(" ")
            sl_len = len(self.descriptionList)-1
            
            varG.studyOutList.append("\n" + "\t" + \
                " extract_Master_Location-S: transLocation=" + self.transLocation + \
                " description=" + self.description + \
                " descriptionList=" + str(self.descriptionList))
     
            if sl_len > 0:
                #print("\n","\t","Loc2-a: self.descriptionList[0]=",self.descriptionList[0],\
                #      " self.descriptionList[1]=",self.descriptionList[1])
                if self.descriptionList[0].isnumeric():
                    #print("\n","\t","Loc2-b: self.descriptionList[0]=",self.descriptionList[0])
                    if self.descriptionList[0] in locationDict:
                        #print("\n","\t","Loc2-c: self.descriptionList[1]=",self.descriptionList[1])
                        if self.descriptionList[1] == "Dominos":
                            #print("\n","\t","Loc2-d: locationDict[self.descriptionList[0]=",\
                            #    locationDict[self.descriptionList[0]])
                            self.transLocation = locationDict[self.descriptionList[0]]
    
            tl_list = []
            tl_list = self.transLocation.split(" ")
            tl_len = len(tl_list)-1
    
    
            if not tl_list[0].isalpha():
                if tl_len > 0:	
                    self.transLocation = uETL.extractFromList \
                        (tl_list,"right",1,0)
                else:
                    self.transLocation = ""
            else:
                for x, y in enumerate(tl_list):
                    if y in locationDict:
                        tl_list[x] = locationDict[y]			
                        if tl_len > 0:
                            self.transLocation = uETL.extractFromList\
                                (tl_list,"all",0,0)
                        else:
                            self.transLocation = tl_list[0]
    
            if self.transLocation in varG.crCardLocationRejectList:
                self.description = saveDescription
                self.transLocation = ""
            else:
                self.transLocation = uETL.cleanLocation(self.transLocation)
                
            varG.studyOutList.append("\n" + "\t" + \
                " extract_Master_Location-E: transLocation=" + self.transLocation + \
                " description=" + self.description + \
                " descriptionList=" + str(self.descriptionList))
            
    
            return self.transLocation, self.descriptionList, self.description   



#def determineByType(self,fields,description,descriptionList,hdrType,hdrAccount):
    #def __main__():
    
        #print('varG.headerList[2]=',varG.headerList[3])
        
        if varG.headerList[2] == "Credit":
            if varG.headerList[3] == "Visa Card":
                
                self.transLocation, self.descriptionList \
                    = extract_Visa_Location(self.descriptionList) 
    
            elif varG.headerList[3] == "Master Card":
    
                self.transLocation, self.descriptionList, self.description \
                    = extract_Master_Location(self.description)
        else:
            self.transLocation = ""
            
        #print('self.transLocation=',self.transLocation)
                
                          

class Descriptors:                                    

    def __init__(self,description,descriptionList,\
                transDate,transAmount,transLocation,fields):
                

        self.description = description
        self.descriptionList = descriptionList
        self.transDate = transDate
        self.transAmount = transAmount
        self.transLocation = transLocation
        self.fields = fields

        
#       hdrOwner - [0], hdrSource - [1], hdrType - [2], hdrAccount - [3]
        #print('\n','varG.headerList=',varG.headerList)
        
        if varG.headerList[2] == 'Credit':
            self.transAction,self.transSource,self.transDestination, \
                self.transDescription,self.transCategory \
                = crT.setCreditCardAttributes(self.description,\
                self.descriptionList,self.transDate,self.transAmount,\
                self.transLocation) 
        elif varG.headerList[2] == 'Debit':
            if varG.jmChecking == True:                 
                self.transAction,self.transSource,self.transDestination, \
                    self.transDescription,self.transCategory \
                    = jmchkF.setJMcheckingAttributes(self.fields)
            else:
                self.transAction,self.transSource,self.transDestination, \
                    self.transDescription,self.transCategory \
                    = dbT.setDebitAcctAttributes(self.description,\
                    self.descriptionList,self.transDate,self.transAmount,\
                    self.transLocation)
                  
        
        #print('\n','varG.headerList=',varG.headerList)
        
        #return self.transAction, self.transSource, self.transDestination, self.transDescription