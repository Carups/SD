
class Executor:
    '''
    Run commands one by one. Also transfer output from one to input other.
    After all commands print result of their work.
    '''
    def launch(self, comandsToRun):
        '''
        :param comandsToRun: array for Commands
        :return: string: result of proceeded command
        '''
        result = None
        for comand in comandsToRun:
            if result is not None:
                comand.argsFromInput.append(result)
            result = comand.run()
        return result
