


class Command_Dispatcher:
    """ An sophisticated, configurable and expanable implementation of a switch statement 
    
        This class does not allow direct instantiation of it since the sbuclass has to implement 
        the functions that will be called by this class.

        General Usage:

            mydisp = MySubClass({command / function pair dictionary}) Instantiates the class
            mydisp.execute(command, **kwargs)  Looks up the method to be executed and returns the output 
                                               from the method
    """
    functions = {}
    #
    # Over-riding the __new__ method provides capability to halt direct 
    # instantiation of the  class.  For this class it must be subclassed
    # in order to provide the functions that will be called.
    def __new__(cls, *args, **kwargs):
        if cls is Command_Dispatcher:
            raise TypeError("Command Dispatcher may not be instantiated")
        return object.__new__(cls)
    #
    # Allow instatiation to happen with or without the command :fucntion pair variable
    def __init__(self,entries=None):
        self.functions = entries
        return 
    #
    # Set the dictionary of command : function pairs   
    def set_commands(self,entries):
        """ Set ther functions dictionary

            The entries parameter is a diction consiting of key / value pairs that represent the command being 
            submitted (Key) and the function to execut that command (value)
        """
        self.functions = entries
        return

    def isvalid(self,query_command):
        """ Verify that a command exists.  

            query_command is a string containing the command
        """
        try:
            _ = self.functions [query_command]
            return True
        except:
            return False  

    def execute(self,query_command,**kwargs):
        """ Execute the requested command

            This method will look up the name of the function to execute based on the parameter query_command.  
            **kwargs is passed in to provide flexibility to programmers to provide the required parameters for 
            each command.
        """

        print (query_command)
        if self.isvalid(query_command):
            method_name = self.functions [query_command]
            method = getattr(self, method_name, lambda: "Invalid command")
            # Call the method as we return it
            #try:
            return method(**kwargs)
#           except:
#                raise UserWarning("Invalid function name. Command={} Function={}".format(query_command,self.functions [query_command]))
        else:
            raise KeyError('Invalid function specified.')    


#
#  Test harness
if __name__ == "__main__":
    #
    # Test to that direct instatiation of this class raise error
    myc = Command_Dispatcher({'IN':'infn','out':'outfn', 'info':'infofn'} )    

  