from config import Config


class Lexer:
    '''
    You should first launch instance of lexer on inputString
    from console to proceed all occurrences of variables from environment.
    '''
    def __init__(self):
        self.Initilizate()

    def show(self):
        '''
        :return: result of last processed string by this instance
        '''
        return self.lexerOut

    def Initilizate(self):
        '''
        I am not sure that this method have right to exist but anyway.
        Set default state for instance of Lexer
        '''
        self.lexerOut = ""
        self.skipMode = False
        self.replaceMode = False
        self.curNameOfVariables = ""

    def launch(self, userInput):
        '''
        Take string and replace all occurrences of $name.
        name could include alphabet symbols, numbers, all kind of
        special symbols like !@#$%^&*())_+. Separator for name are
        space, ', '', $
        :param userInput: String
        :return: String
        '''
        self.Initilizate()
        for character in userInput:
            if self.skipMode:  # just skip everything inside of ' '
                if character == '\'':
                    self.skipMode = False

                self.lexerOut += character
                continue
            def dump():
                '''
                Service function. Change variable on it value.
                '''
                if self.curNameOfVariables in Config.variables:
                    self.lexerOut += Config.variables[self.curNameOfVariables]
                self.curNameOfVariables = ""
                self.replaceMode = False

            if not character.isspace():
                # get name of variable until next separator
                if self.replaceMode:
                    if character == '$':
                        dump()
                        self.replaceMode = True
                    else:
                        if character == '\'':
                            dump()
                            self.skipMode = True
                            self.lexerOut += character
                        else:
                            self.curNameOfVariables += character
                else:
                    if character == '$':
                        self.replaceMode = True
                    else:
                        if character == '\'':
                            self.skipMode = True
                        self.lexerOut += character
            else:
                if self.replaceMode:
                    dump()
                self.lexerOut += character
        if self.replaceMode:
            if self.curNameOfVariables in Config.variables:
                self.lexerOut += Config.variables[self.curNameOfVariables]
            self.replaceMode = False
        if self.skipMode:
            self.skipMode = False
            raise Exception("There is not closing '")

