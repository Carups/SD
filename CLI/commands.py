import sys
import subprocess
from config import Config


class Token:
    '''
    Abstract class for diagram
    '''
    pass


class Arguments(Token): # not used but might be in next version
    pass


class Parametrs(Token): # not used but might be in next version
    pass


class Command(Token):
    '''
    Abstract class for commands
    All commands use string as interface for communication
    '''
    def __init__(self):
        self.argsFromInput = []
        self.paramsFromInput = []
        self.maxNumberOfArgs = 100
        self.minNumberOfArgs = 0
        self.listOfSupportedParam = {}

    def check(self):
        '''
        command check its parameters before launch
        '''
        if len(self.argsFromInput) > self.maxNumberOfArgs or len(self.argsFromInput) < self.minNumberOfArgs:
            raise Exception("Unsupported numbers of args for command {}".format(self.__class__.__name__))
        for param in self.paramsFromInput:
            if param not in self.listOfSupportedParam:
                raise Exception("Unsupported params for command {}".format(self.__class__.__name__))

    def run(self):
        raise Exception("Unimplemented Command")


class Exit(Command):
    def __init__(self):
        super(Exit, self).__init__()
        self.maxNumberOfArgs = 0
        self.minNumberOfArgs = 0


    def run(self):
        self.check()
        Config.run = False


class Cat(Command):
    '''
    Cat can only open files by relative name from current directory
    '''
    def __init__(self):
        super(Cat, self).__init__()

    def run(self):
        self.check()
        numberOfRow = 0
        outputString = ""

        for fileName in self.argsFromInput:
            file_in = open(Config.curDir + "/" + fileName, "r")
            for line in file_in.read().splitlines():
                numberOfRow = numberOfRow + 1
                outputString += '{0}. {1}\n'.format(numberOfRow, line)
            file_in.close()


        return outputString


class Wc(Command):
    '''
    Take string for evaluations
    '''
    def __init__(self):
        super(Wc, self).__init__()

    def run(self):
        self.check()
        numberOfLine, numberOfChar, numberOfByte = 0, 0, 0
        outputString = ""
        for text in self.argsFromInput:
            lineInFile = len(text.splitlines())
            wordInFile = len(text.split())
            charInFile = 0
            for each in text.split():
                charInFile += len(each)
            outputString += ("{} {} {}\n".format(lineInFile, wordInFile, charInFile))
            numberOfLine, numberOfChar, numberOfByte = numberOfLine + lineInFile, numberOfChar + wordInFile, numberOfByte + charInFile

        if len(self.argsFromInput) > 1:
            outputString += ("{} {} {} {}\n".format(numberOfLine, numberOfChar, numberOfByte, "total"))
        if outputString == '':
            outputString = "0 0 0\n"

        return outputString


class Echo(Command):
    '''
    Just remove '' and ""
    '''
    def run(self):
        self.check()
        output = ""
        for word in self.argsFromInput:
            output += word
            output += " "
        output += "\n"
        return output


class Pwd(Command):
    def __init__(self):
        super(Pwd, self).__init__()
        self.maxNumberOfArgs = 0
        self.minNumberOfArgs = 0

    def run(self):
        self.check()
        return Config.curDir + "\n"


class Assignment(Command):
    '''
    Always execute first.
    '''
    def __init__(self):
        super(Assignment, self).__init__()
        self.maxNumberOfArgs = 2
        self.minNumberOfArgs = 2

    def run(self):
        self.check()
        Config.variables[self.argsFromInput[0]] = self.argsFromInput[1]


class Others(Command):
    '''
    try subprocess for every not implemented comand
    '''
    def run(self):
        try:
            unknownOut = subprocess.check_output(self.argsFromInput)
        except:
            raise Exception("Error in unknown command")
        return unknownOut.decode()


