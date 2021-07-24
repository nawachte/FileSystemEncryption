from SecureFile import SecureFile
import os
import sys

'''
For entering arguments through the command line:
python3 fileSecDriver.py <inFolder> <outFolder> <keyword> <e/d(encryption or decryption)>
'''

inFolder = None
outFolder = None
keyword = None
e_or_d = None

if len(sys.argv) < 2:
    inFolder = input("In folder name: ")
    while inFolder not in os.listdir(os.getcwd()):
        print("\""+inFolder + "\" does not exist in the current directory.")
        inFolder = input("In folder name: ")
    outFolder = input("Out folder name: ")
    while outFolder not in os.listdir(os.getcwd()):
        print(outFolder + " does not exist in the current directory.")
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

else:
    try:
        inFolder = sys.argv[1]
        outFolder = sys.argv[2]
        key_word = sys.argv[3]
        e_or_d = sys.argv[4]
        # print(os.listdir(os.getcwd()))
        if inFolder not in os.listdir(os.getcwd()):
            raise Exception(inFolder+ " does not exist in the current working directory.")
        if outFolder not in os.listdir(os.getcwd()):
            raise Exception(outFolder+ " does not exist in the current working directory.")
        if e_or_d != "e" and e_or_d != "d":
            raise Exception("Argument #4 must either be \"e\" for encryption or \"d\" for decryption.")
    except Exception as e:
        print()
        print(e)
        print()
        print("Command line arguments should be in the following format:")
        print("python3 fileSecDriver.py <inFolder> <outFolder> <keyword> <e/d(encryption or decryption)>")
        print()
        sys.exit(1)

fileS = SecureFile(key_word)

def encrypt_decrypt(inFolder, outFolder):
    fileS.setInDir(inFolder)
    fileS.setOutDir(outFolder)
    for file in os.listdir(inFolder):
        if os.path.isdir(inFolder+"/"+file):
            # save in and out folders
            inFolderSave = inFolder
            outFolderSave = outFolder
            # create outFolder sub directory if necessary
            if file not in os.listdir(outFolder):
                os.mkdir(outFolder+"/"+file)
            encrypt_decrypt(inFolder+"/"+file, outFolder+"/"+file)
            inFolder = inFolderSave
            outFolder = outFolderSave
            fileS.setInDir(inFolder)
            fileS.setOutDir(outFolder)
        elif file != ".DS_Store":
            fileS.setFile(file)
            if e_or_d == "e":
                fileS.encrypt()
            elif e_or_d == "d":
                success = fileS.decrypt()
                if success == -1:
                    sys.exit("Incorrect key given")
            else:
                #should never get here
                raise Exception("Encrypt / Decrypt not correctly set.")

encrypt_decrypt(os.getcwd()+"/"+inFolder, os.getcwd()+"/"+outFolder)

if e_or_d == "e":
    print("Encryption process complete.")
else:
    print("Decryption process complete.")
