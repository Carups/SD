from config import Config
from lexer import Lexer
from parser import Parser
from executor import Executor
from commands import Exit, Wc, Config, Echo, Pwd, Assignment, Cat, Grep
class Control:
    '''
    Wrap up on infinite loop
    '''
    def launch(self):
        '''
        Start of all program
        '''
        Config.listOfCommands = {"exit": Exit, "wc": Wc, "cat": Cat, "echo": Echo, "pwd": Pwd,
                                 "=": Assignment, "grep": Grep}
        while(Config.run):
            try:
                Config.lexer = Lexer()
                Config.parser = Parser()
                Config.executor = Executor()
                userInput = input()
                Config.lexer.launch(userInput)
                Config.parser.launch(Config.lexer.lexerOut)
                answer = Config.executor.launch(Config.parser.parserOut)
                if answer is not None:
                    print(answer, end="")
            except Exception as  e:
                print(str(e))


