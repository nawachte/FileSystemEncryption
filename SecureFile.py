from Crypto.Cipher import AES

# key_word = input("Keyword: ")
# encrypt_or_decrypt = input("Encrypt(1) or decrpt(2): ")
# filename = input("file name: ")

class SecureFile:
    def __init__(self, key_word):
        if len(key_word) == 0:
            raise Exception("Invalid keyword")
        self.key_word = key_word
        self.filename = None
        self.inDir = None
        self.outDir = None

    def setOutDir(self, dirPath):
        self.outDir = dirPath+"/"

    def setInDir(self, dirPath):
        self.inDir = dirPath+"/"

    def setFile(self, newname):
        if (len(newname) == 0) or ("." not in newname):
            raise Exception("Invalid filename: "+newname)
        self.filename = newname

    def changeKeyword(self, newkey):
        self.key_word = newkey

    def produceIV(self):
        filename = self.filename.replace("ENCRYPTED", "")
        IV = ''
        if len(filename) >= 16:
            IV = filename[:16]
        else:
            while len(IV) < 16:
                IV += filename
            IV = IV[:16]
        return IV

    def produceKey(self):
        key = ''
        if len(self.key_word) >= 24:
            key = self.key_word[:24]
        else:
            while len(key) < 24:
                key += self.key_word
            key = key[:24]
        return key

    def padFile(self, filebytes):
        padbytes = 16 - len(filebytes)%16
        filebytes += b'\x00' * (padbytes-1) + padbytes.to_bytes(1, 'big')
        return filebytes

    def depadFile(self, filebytes):
        numblocks = int(len(filebytes)/16) + (1 if len(filebytes)%16 else 0)
        newplain = filebytes[:(numblocks-1)*16]
        padblock = filebytes[(numblocks-1)*16:]
        padbytes = int(padblock[-1:].hex(), 16)

        #validate padding
        if padbytes == 0 or padbytes > 16:
            return -1
        for b in padblock[16-padbytes : 15]:
            if b!= 0:
                return -1

        newplain += padblock[:-padbytes]
        return newplain

    def encrypt(self):
        if self.inDir == None:
            raise Exception("In directory not set.")
        if self.outDir == None:
            raise Exception("Out directory not set.")
        if self.filename == None:
            raise Exception("File name not set.")
        if "ENCRYPTED" in self.filename:
            print("file already encrypted")
            return

        file = open(self.inDir+self.filename, "rb")
        filebytes = file.read()
        file.close()

        aesObj = AES.new(self.produceKey(), AES.MODE_CBC, self.produceIV())
        filepadded = self.padFile(filebytes)
        encrypted = aesObj.encrypt(filepadded)

        newName = self.filename
        suffix = newName[newName.index("."):]
        newName = newName.replace(suffix, "ENCRYPTED"+suffix)
        newfile = open(self.outDir+newName, "wb")
        newfile.write(encrypted)
        newfile.close()

    def decrypt(self):
        if self.inDir == None:
            raise Exception("In directory not set.")
        if self.outDir == None:
            raise Exception("Out directory not set.")
        if self.filename == None:
            raise Exception("File name not set.")
        if "ENCRYPTED" not in self.filename:
            print("File is not encrypted: "+self.filename)
            return

        file = open(self.inDir+self.filename, "rb")
        filebytes = file.read()
        file.close()

        aesObj = AES.new(self.produceKey(), AES.MODE_CBC, self.produceIV())
        decrypted = aesObj.decrypt(filebytes)
        depadded = self.depadFile(decrypted)
        if depadded == -1:
            return -1

        newName = self.filename.replace("ENCRYPTED", "")
        newFile = open(self.outDir+newName, "wb")
        newFile.write(depadded)
        newFile.close()
