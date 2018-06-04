import os


class Config:
    curDir = os.getcwd()
    listOfCommands = None
    executor = None
    parser = None
    lexer = None
    variables = {}
    run = True
