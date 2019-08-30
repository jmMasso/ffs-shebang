# ffs-shebang
Anaconda Spyder Python package for taking in downloaded transaction files with conversion to mySQL runable script files.

  I. Purpose
     A.  To provide a means of obtaining personal financial data for storage and analysis within a Relational Data Base Management
         System.
     B.  To give depth to account download data in the form of personal customization of the data received from the financial account
         websites.
     C.  To give organization and usage of data over an extended period of time.

 II. Contents
     A.  Contains folder with all Family Finance package modules for going from point D to point X
     B.  

III. Requirements
     A.  Download of account files
         1. store file as .txt tab delimited
         2. insert header record with columns
            a. owner 
            b. bank
            c. type
               (1) debit, for bank accounts (checking and savings)
               (2) credit, for credit card accounts
            d. account
               (1) checking
               (2) savings
               (3) master card, visa card, ? card
         3. name file as
            a. 'FFS - ', to represent file Prefix naming convention
            b. 'ownerName - ', to represent who the file belongs to 
            c. 'account - ', 
               (1) type 'debit', account equals 'Checking' or 'Savings'
               (2) type 'credit', account equals 'crCard x', where x equals
                   (a) master, visa or ? (perferred to have ? as single word name)
                 
     B.  Creation of support files
         1.  owner/account MySQL create insert files
         2.  owner/account MySQL insert files
         3.  owner/account MySQL update files
         2.  payReimburse MySQL create insert files
     
     
     C.  Execution of Main by parameter values
         1.  file path - "C:/
         2.  sql Key Number - values '1', '2' or '3'
         3.  runNumber - 'n', incremented per run starting with '1'
         4.  owner/account run number - 'n', incremented per run starting with '1'
         5.  runYear - 'yyyy'
         6.  runRange - 'mm - mm', represents month range for data within transaction file 
         7.  runType - 'Debit'/'Credit'
         8.  runOwner - name indicated on input transaction file header
         9.  runAccount - 'Checking', 'Savings' or 'crCard ?
         10. runPrefix1 - 'FFS' can be changed to your preference 
         11. runPrefix2 - '' not used in system at this time
         
     
 IV. PipeLine
     A.  Download account files from Bank or Credit Card website
     B.  Modify download file to meet requirements
     C.  Modify main.py parameters to meet input and output output naming conventions
     D.  Verify accuracy of run by viewing the output transStudy file concentrating on Section I
         and Section II
     E.  Modify MySQL output insert files by changing 'now()' to now()
     F.  Copy MySQL .txt output files to .sql files 
     G.  Sign on to MySQL 
     H.  Run each .sql output script file
         

  V. Information
     A.  Features
     B.  Future Enhancements
