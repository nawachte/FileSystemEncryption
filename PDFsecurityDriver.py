from SecurePDF import SecurePDF
import os
import sys
#
# pdf = SecurePDF('test', '1:2:3.pdf')
# pdf.encrypt()
# pdf.changeFile("1:2:3encrypted.pdf")
# pdf.decrypt()

inFolder = input("In folder name: ")
while inFolder not in os.listdir(os.getcwd()):
    print("\""+inFolder + "\" does not exist in the current directory.")
    inFolder = input("In folder name: ")
outFolder = input("Out folder name: ")
while outFolder not in os.listdir(os.getcwd()):
    print(inFolder + " does not exist in the current directory.")
    outFolder = input("Out folder name: ")
key_word = input("Key word: ")
confirm = "n"
while confirm != "y":
    confirm = input("Confirm that the key word is \""+key_word+"\" (y/n): ")
    if confirm != "y":
        key_word = input("Key word: ")
confirm = "n"
# e_or_d = ""
while confirm != "y":
    e_or_d = input("Do you want to encrypt(e) or decrypt(d) your files?: ")
    while (e_or_d != "e") and (e_or_d != "d"):
        print("Enter either \"e\" for encrypt or \"d\" for decrypt.")
        e_or_d = input("Do you want to encrypt(e) or decrypt(d) your files?: ")
    if e_or_d == "e":
        confirm = input("Confirm that you would like to ENCRYPT your files (y/n): ")
    else:
        confirm = input("Confirm that you would like to DECRYPT your files (y/n): ")

cwd = os.getcwd()
inFolder = cwd + "/" + inFolder
outFolder = cwd + "/" +outFolder
pdfS = SecurePDF(key_word)
pdfS.setInDir(inFolder)
pdfS.setOutDir(outFolder)
for file in os.listdir(inFolder):
    if file.endswith(".pdf"):
        pdfS.setFile(file)
        if e_or_d == "e":
            pdfS.encrypt()
        elif e_or_d == "d":
            success = pdfS.decrypt()
            if success == -1:
                sys.exit("Incorrect key given")
                # print("Incorrect key given.")
        else:
            #should never get here
            raise Exception("Encrypt / Decrypt not correctly set.")
    else:
        if file != ".DS_Store":
            print("File "+file+" is not a pdf. It will not be encrypted/decrypted.")

if e_or_d == "e":
    print("Encryption process complete.")
else:
    print("Decryption process complete.")
