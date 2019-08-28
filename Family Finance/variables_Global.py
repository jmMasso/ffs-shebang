# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:04:17 2019

@author: Jeanette
"""

class VarGlobals(object):
    
    sql_transTableName = ""
    sql_prTableName = ""
    
    
    inTHelpersList = []
    inTHelpersDict = {}
    inTHelpersCatDict_HP = {}
    inTHelpersCatDict = {}
    inTHelpersPayReimbDict = {}
    
    recircInfoDict = {}   #Dict created with input recirc info file data
                          #within io_Prep.py and updated with new dict entries
                          #in out_RecircInfo.py 
                          #Dict entry reference in out_PayReimb.py per inTrans
                          #line of data
    
    jmChecking = False
    
    tRIKey = ""
    prRIKey = 'payReimb'    
    tRILastRunLine = ""    
    headerList = []  
           
    studyOutList = []
    analysisOutSet = set()
    
    
    #   Owner - [0]  Source - [1]  Type - [2]  Account - [3]

    
    singleNameList = ["albertsons", "medprovider", "whataburger","wal-mart",\
        "starbucks", "udemy","Macys","exxonmobil","saltgrass","wingstop",\
        "usps","Netflix","udemy","dell","nike","pluckers","valero",\
        "shipley","7-eleven","hoochies","kfc","-Single"]
				
    convertStopDict = {"htpn":"HTPN MyCharts","5guys":"5 Guys",\
        "BR":"Banana Republic Factory","domino":"Dominos Pizza",
        "Sprouts":"Sprouts Farmers Market","bedbathbey":"Bed Bath Beyond",\
        "h-e-b":"HEB","on lin":"On-Line","exxonmobile":"Exxonmobil",\
        "luckybrand":"Lucky Brand","officedepot":"Office Max/Dep",\
        "murphy":"Murphy Gas","mar":"Market","mark":"Market","chuy":"Chuy's",\
        "br":"Banana Republic Factory","heb":"HEB","apl":"Apple I-tunes",\
        "adobe":"Adobe Export Pdf","motor":"Motor Vehicle","cane":"Canes",\
        "bcp":"Americas Test Kitchen","luckybrandd":"Lucky Brand",\
        "flexjobs":"Flexjobs.com","dq":"Dairy Queen","gril":"Grill",\
        "gri":"Grill","gr":"Grill","interest":"Interest Charged",
        "late":"Late Fee Charged","e-z":"E-Z Mart","wm":"Wal-Mart",\
        "international":"International House of Pancakes",\
        "kohl":"Kohl's","mcalist":"McAlister's Deli","cvs":"CVS Pharmacy",\
        "pashunpubli":"Pashun Publishing Press",\
        "tpcscstore":"The PC Software Connection Store"}
        
		
    convertContinueDict = {"cath":"Catholic","gri":"Gril",\
        "automoti":"Automotive","ba":"Bar"}
	
    rejectList = ["on-line","bb","bcp","brk","dalla","paypal","eb","bryan",\
        "com","-Reject"]

    allCapsList = ["heb","usa","ut","usps","cvs","kfc","llc","-allCaps"]

    checkGasList = ["HEB","wal-mart","-Gas"]

    stopList = ["building", "electric","usps", "usa", "grill","saltgrass",
        "tacos","canes","udemy","-Stop"]

    lastDropList = ["at","on-lin","cooperat","and","po","on","ref","com",
        "waxahachie","ach","cedar","dallas","on-line","corp","bryan","-lDrop"]

    firstPositionRejectStopList = ["0","1","2","3","4","5","6","7","8","9",\
        "#","-FirstPosRejStop"]

    firstPositionSplitKeepRightList = ["*","-FirstPosSpltKeepRight"]

    splitList = ["&","-","/","*",".","#","0","1","2","3","4","5","6","7","8",\
        "9","-SplitList"]

    crCardLocationRejectList = ['PAYMENT','PURCHASES','PAST DUE',\
        'TELEPHONE PAYMENT','STANDARD PURCHASE','REF','NDARD PURCH','T']
    
#--> used to reflect these are Mom's accounts managed by person Initials     
    convertOwnerDict = {"masso j":"JMmom","schneider a":"ASmom",\
        "Jeanette":"masso j","Jeanettemom":"JMmom"}
#--> used to convert last name First name intial to First Name
    convertOwnerToFirstDict = {"masso j":"Jeanette"}
