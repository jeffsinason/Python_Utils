import json
from flatten_dict import flatten, unflatten


class json_configuration:

    filename = ''
    configuration= {"none" : "empty"}
    loaded = False
    modified = False

    def __init__(self,file_name=""):
        if file_name:
            self.filename = file_name
            with open(self.filename) as config_file:
                self.configuration = json.load(config_file)
                self.loaded = True
        return        

    def load_config(self, file_name):
        self.filename = file_name
        with open(self.filename) as config_file:
            self.configuration = json.load(config_file)
            self.loaded = True
        return        

    def save_config(self):

        with open(self.filename, "w") as write_file:
            outconfig = json.dumps(self.configuration, indent=4)
            write_file.write(outconfig)
            

    #
    # Will return the entity specified with the path
    # Could return direct value of directory entry or a dictionary if there are children to the path specified
    # depending on the level the path was ed to
    def get(self, path):

        if not self.loaded:
            raise ConfigNotLoaded("Configuration file not loaded.")


        keys = path.split(':')
        flat =  flatten(self.configuration)
    
        #
        # Build the key to get to the value
        wlist = []
        for key in keys:
            wlist.append(key)

        try:
            #try to get a direct value.  If we get an exception we will try to get a dictionary object.
            # if no exception then a bottom lever value was found and returned
            return_val =  flat[tuple(wlist)]
            return return_val
        except  KeyError:  
            #
            # When here got a keyerror so see if the path has children and build a return dictionary
            return_val = {}
            for key in flat:
                print (type(key), key)
                countNode = 0
                matchcount = 0
                for node in key:
                    if countNode < len(wlist):
                        if node == wlist[countNode] :
                            matchcount += 1
                            print (matchcount,  node, wlist[countNode])
                    else:
                        #
                        # Check for add to new dictionary to be returned
                        if matchcount == len(wlist):
                            templist = wlist.copy()
                            templist.append(node)
                            return_val[ node ] = flat[tuple(templist)]

                    countNode += 1

                    print (node)

        return return_val
    #
    # Add a value to the configration file.
    # The path is the full path down to the specific key for the value ( must be unique to add)
    # if a dictionary is passed in as the value it is added as the next level of the configuration
    def add(self, path,  value):

        if not self.loaded:
            raise ConfigNotLoaded("Configuration file not loaded.")

        keys = path.split(':')
        flat =  flatten(self.configuration)

        wlist = []
        for key in keys:
            wlist.append(key)

        #
        # if the key already exist raise a key error
        if flat.get(tuple(wlist), None):
            raise KeyError("Key already exists Key={}",wlist)

        flat[ tuple(wlist)] = value

        self.configuration = unflatten(flat)    
        self.modified = True
        self.save_config()
        return

    #
    # will update the configuration
    # If a single value is sent in it updates the specific element specified in the path
    # If a dictionary is sent in it updates all of the elements under path contained 
    #   in the dictionary
    def update(self, path, value):

        if not self.loaded:
            raise ConfigNotLoaded("Configuration file not loaded.")

        keys = path.split(':')

        flat =  flatten(self.configuration)

        wlist = []
        for key in keys:
            wlist.append(key)

        #
        # If a dictionary was passed in update all values contained in the dictionary
        # are updated in the configuration
        if not isinstance(value,dict):  
            flat[ tuple(wlist)] = value
        else:
            for key in value:
                listkey = wlist.copy()
                listkey.append(key)
                flat[ tuple(listkey)] = value[key]    

        self.configuration = unflatten(flat)    
        self.modified = True
        self.save_config()
        return
    
    #
    # Deletes an entry from the configuration file
    # Only bottom level items can be deleted

    def delete(self, path):

        if not self.loaded:
            raise ConfigNotLoaded("Configuration file not loaded.")

        keys = path.split(':')

        flat =  flatten(self.configuration)                
        
        wlist = []
        for key in keys:
            wlist.append(key)
        
        del flat[tuple(wlist)]

        self.configuration = unflatten(flat)    
        self.modified = True
        self.save_config()
        return




class Error(Exception):
    pass

class ConfigNotLoaded(Error):

    def __init__(self,  message):
        self.message = message


#
# Test Harness
if __name__ == "__main__":
    myc = json_configuration ('testconfig.json')
    myc.update("testdel:secondlevel:thirdlevel", {"val1": 1141, "val2":2252,"val3":3363})
    print(type(myc.get("testdel:secondlevel:thirdlevel")),myc.get("testdel:secondlevel:thirdlevel"))
    #
    #
    #myc.update("deep:deeper:deepest", {"val1": {"emb1": 1,"emb2":2,"emb3":3}, "val2":2252,"val3":3363})
    ret_val =myc.get("deep:deeper:deepest:val1")
    print (type(ret_val), ret_val)