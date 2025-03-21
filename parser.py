import re

class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.inFunction = False 
        self.beginCountingBrackets = False
        self.openTextBlock = False
        self.openImageBlock = False
        self.openTextInput = False
        self.foundText = []
        self.imageIds = []
        self.textPlaceholders = []
        self.functionName = ""
        self.needExpoFontMock = False

    
    def parseFile(self):
        with open(self.filename, 'r') as file:
            bracketCount = 0
            openBrackets = 0
            lookForOpenBracket = False
            currentLine = ""
            for line in file:
                # get the function name
                if "export default function" in line:
                    self.inFunction = True
                    self.beginCountingBrackets = True
                    startLine = line.find("export default function ")
                    endline = line.find("(")
                    self.functionName = line[startLine + len("export default function "):endline]
                    

                if "const" in line and "=>" in line:
                    lookForOpenBracket = True

                if "from 'react-native-vector-icons" in line:
                    self.needExpoFontMock = True

                if lookForOpenBracket or openBrackets != 0:
                    openBrackets += line.count("{")
                    openBrackets -=  line.count("}")

                    if openBrackets != 0:
                        lookForOpenBracket = False
                    if openBrackets < 0:
                        print("set 0")
                        openBrackets = 0

                if self.inFunction:
                    #check if the function is closed
                    bracketCount += line.count('{')
                    bracketCount -= line.count('}')
                    if bracketCount == 0:
                        self.inFunction = False

                    # get the text show on the screen
                    if openBrackets == 0 and not lookForOpenBracket:
                        match =  re.search("<ThemedText[^>]*>", line)
                        if match:
                            self.openTextBlock = True
                        if self.openTextBlock:
                            endLine = line.find("</ThemedText>")
                            if match:
                                startLine = line.find(match.group(0)) + len(match.group(0))
                                if currentLine != "" and line[startLine:endLine].strip() != "":
                                    currentLine = currentLine + "\\n"
                                currentLine = currentLine + line[startLine:endLine].strip()
                            else:
                                if currentLine != "" and line[:endLine].strip()!="":
                                    currentLine = currentLine + "\\n"
                                currentLine = currentLine + line[:endLine].strip()

                        if "</ThemedText>" in line:
                            self.openTextBlock = False
                            self.foundText.append(currentLine)
                            currentLine = ""
                    

                        # get images
                        if "<Image" in line:
                            self.openImageBlock = True
                        
                        if self.openImageBlock:
                            match = re.search(r'testID=(.*)', line)
                            if match:
                                self.imageIds.append(match.group(1).strip())

                            if "/>" in line:
                                self.openImageBlock = False

                        if "<TextInput" in line:
                            self.openTextInput = True
                        if self.openTextInput:
                            match = re.search(r'placeholder=(.*)', line)
                            if match:
                                self.textPlaceholders.append(match.group(1).strip())

                            if "/>" in line:
                                self.openTextInput = False



        
    def getFunctionInfo(self):
        self.parseFile()
        validText = []
        for text in self.foundText:
            if text != "":
                validText.append(text)
        
        return FunctionInfo(self.functionName, validText, self.imageIds, 
                            self.textPlaceholders, self.filename[7:], self.needExpoFontMock)





class FunctionInfo:
    def __init__(self, name:str, text, imageIds, textPlaceholders, filename, needExpoFontMock):
        self.name = name
        self.text = text
        self.images = imageIds
        self.textPlaceholders = textPlaceholders
        self.filename = filename
        self.needExpoFontMock = needExpoFontMock

    def getName(self):
        return self.name
    
    def getNameLower(self):
        return self.name.lower()
    
    def getText(self):
        return self.text
    
    def getImages(self):
        return self.images
    
    def getPlaceholders(self):
        return self.textPlaceholders
    
    def getExpoFontMock(self):
        return self.needExpoFontMock
    
    def getFileName(self):
        return self.filename.split(".")[0]