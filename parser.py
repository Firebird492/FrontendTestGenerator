import re

class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.inFunction = False 
        self.beginCountingBrackets = False
        self.openTextBlock = False
        self.foundText = []
        self.functionName = ""

    
    def parseFile(self):
        with open(self.filename, 'r') as file:
            bracketCount = 0
            currentLine = ""
            for line in file:
                if "export default function" in line:
                    self.inFunction = True
                    self.beginCountingBrackets = True
                    startLine = line.find("export default function ")
                    endline = line.find("(")
                    self.functionName = line[startLine + len("export default function "):endline]

                if self.inFunction:
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
                            #self.foundText.append(line[startLine:endLine].strip())
                        else:
                            if currentLine != "" and line[:endLine].strip()!="":
                                currentLine = currentLine + "\\n"
                            currentLine = currentLine + line[:endLine].strip()
                            #self.foundText.append(line[:endLine].strip())

                    if "</ThemedText>" in line:
                        self.openTextBlock = False
                        self.foundText.append(currentLine)
                        currentLine = ""
                    if "{" in line:
                        bracketCount += 1
                    if "}" in line:
                        bracketCount -= 1
                        if bracketCount == 0:
                            self.inFunction = False
        
    def getFunctionInfo(self):
        self.parseFile()
        validText = []
        for text in self.foundText:
            if text != "":
                validText.append(text)
        return FunctionInfo(self.functionName, validText)





class FunctionInfo:
    def __init__(self, name:str, text):
        self.name = name
        self.text = text

    def getName(self):
        return self.name
    
    def getNameLower(self):
        return self.name.lower()
    
    def getText(self):
        return self.text