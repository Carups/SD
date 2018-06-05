from config import Config
from commands import Others

class Buffer:
    '''
    Class exist for purpose of polymorphism.
    Parser use it to keep some word.
    '''
    def __init__(self):
        self.value = ""

    def get(self):
        return self.value

    def put(self, value):
        self.value = value

    def clear(self):
        self.value = ""

    def add(self, char):
        self.value += char


class Parser:
    '''
    parser going to work after lexer just to
    split input string on sequence of commands
    bounded by pipeline
    '''
    def __init__(self):
        self.buf = Buffer()
        self.parserOut = []

    def launch(self, inputString):
        '''
        First phase: split by pipeline with consider of '' and ""
        Second phase: create commands from array of strings
        :param inputString:String
        :return: array of commands
        '''
        self.parserOut = []
        stringsSplitByPipe = []
        #flag for consideration of ''
        skip = False

        for char in inputString:
            if char == '\'':
                skip = not skip
            else:
                if not skip and char == '|':
                    stringsSplitByPipe.append(self.buf.get())
                    self.buf.clear()
                else:
                    self.buf.add(char)
        stringsSplitByPipe.append(self.buf.get())
        self.buf.clear()

        for each in stringsSplitByPipe:
            words = []
            self.buf.clear()
            runnable = True #if sequnce insade of '' it shold not interpritate
            openSpace = False #considering sequnce insade "" and ''
            def dump(isRunable):
                '''
                Just to eliminate extra code copy/paste
                '''
                words.append((isRunable, self.buf.get()))
                self.buf.clear()

            for char in each:
                if not openSpace:
                    if char.isspace():
                        dump(True)
                    else:

                        if char == "\"":
                            dump(True)
                            openSpace = True
                        else:
                            if char == '\'':
                                dump(True)
                                openSpace = True
                                runnable = False
                            else:
                                self.buf.add(char)
                else:
                    if char == '\'' or char == '\"':
                        dump(runnable)
                        runnable = True
                        openSpace = False
                    else:
                        self.buf.add(char)
            if openSpace:
                raise Exception("Wrong position of \"")
            dump(runnable)
            tmp = []
            for word in words:
                if word[1] != "":
                    tmp.append(word)
            words = tmp

            if len(words) > 0:
                if len(words) > 1 and words[1][1] == '=':
                    tmp = words[0]
                    words[0] = words[1]
                    words[1] = tmp

                if words[0][0] == 0:
                    raise Exception("Syntax error")
                if words[0][1] not in Config.listOfCommands:
                    unknownCommand = Others()
                    for word in words:
                        unknownCommand.argsFromInput.append(word[1])
                    self.parserOut.append(unknownCommand)
                else:
                    command = Config.listOfCommands[words[0][1]]()
                    for id in range(1, len(words)):
                        command.argsFromInput.append(words[id][1])
                    self.parserOut.append(command)
