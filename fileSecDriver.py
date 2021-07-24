from SecureFile import SecureFile
import os
import sys

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

def encrypt_decrypt(cwd):
    inFolder = cwd + "/" + inFolder
    outFolder = cwd + "/" +outFolder
    fileS = SecureFile(key_word)
    fileS.setInDir(inFolder)
    fileS.setOutDir(outFolder)
    for file in os.listdir(inFolder):
        # if os.path.isdir(file):
        #     encrypt_decrypt(cwd+"/"+file)
        elif file != ".DS_Store":
            fileS.setFile(file)
            if e_or_d == "e":
                fileS.encrypt()
            elif e_or_d == "d":
                success = fileS.decrypt()
                if success == -1:
                    sys.exit("Incorrect key given")
                    # print("Incorrect key given.")
            else:
                #should never get here
                raise Exception("Encrypt / Decrypt not correctly set.")

encrypt_decrypt(os.getcwd())

if e_or_d == "e":
    print("Encryption process complete.")
else:
    print("Decryption process complete.")
