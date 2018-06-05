import sys
import re
import subprocess
import argparse

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

class Grep(Command):
    """
    Find by regexp in text file. You should point out file relative directory
    Type string pattern last
    """
    def __init__(self):
        super(Grep, self).__init__()

    def run(self):
        linesAfter = 0
        lines = []
        pattern = ''

        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--whole", action="store_true", help = "Find only whole word")
        parser.add_argument("-i", "--insensitive", action="store_true", help = "Compare string case-insensitive")
        parser.add_argument("-A", "--After", type=int, help = "Print strings after concurrence")
        parser.add_argument("dir")
        parser.add_argument("pattern")

        try:
            args = parser.parse_args(self.argsFromInput)
        except:
            raise Exception("wrong argument syntax")
        with open(Config.curDir + "/" + args.dir, 'r') as f:
            lines = f.read().splitlines()
        pattern = args.pattern
        if args.After:
            linesAfter = args.After
        if args.whole:
            pattern = r'\W' + pattern + r'\W'
        pattern = '.*' + pattern + '.*'
        if args.insensitive:
            regexp = re.compile(pattern, flags=re.IGNORECASE)
        else:
            regexp = re.compile(pattern)

        res = ''
        for i in range(len(lines)):
            if regexp.match(lines[i]):
                res += ('\n'.join(lines[i:i + linesAfter + 1])) + '\n'

        return res


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


