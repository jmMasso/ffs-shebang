# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:08:55 2019

@author: Jeanette
"""
from variables_Global import VarGlobals as varG

class WriteSA:

    def write_TransStudy(transStudy):        
        
        for x, y in enumerate(varG.studyOutList):
            yLine = y +' \n'
            transStudy.write(yLine)
            
        transStudy.close()
        
        print('transStudy closed')
        
    

    def write_TransAnalysis(transAnalysis):

        descriptionSet = varG.analysisOutSet
        transAnalysis = transAnalysis

        descriptionTuple = ()
        descriptionTuple = tuple(descriptionSet)
        descriptionTuple = sorted(descriptionTuple)

        sDescriptionList = []
        psDescriptionList = ["",""]

        svN = 0
        transAnalysisCnt = 0

        outLine = ""

        for sDescription in descriptionTuple:
			
            sDescriptionList = list(sDescription)
            if sDescriptionList[:1] != psDescriptionList[:1]:
                svN += 1
                outLine = "\n" + "\n"" " + str(svN)
                transAnalysis.write(outLine)

            outLine = "\t" + sDescription + "\n"
            transAnalysis.write(outLine)
            
            transAnalysisCnt += 1

            psDescriptionList = list(sDescription)
            
        
        transAnalysis.close()
        
        varG.studyOutList.append('\n' + 'transAnalysis closed')       
        varG.studyOutList.append('transAnalysisCnt=' + str(transAnalysisCnt))