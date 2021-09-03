import json
import sys
import os
class Configuration:
    _obj=None
    def __new__(cls):
        if Configuration._obj!=None:
            return Configuration._obj
        if os.path.isfile("server_conf.cfg")==False:
            print("Configuration file missing, refer documentation")
            sys.exit()
        try:
            with open("server_conf.cfg") as json_file:
                new_dict=json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            print("Contents of server_conf.cfg are not of JSON Type, refer documentation")
            sys.exit()
        Configuration._obj=super(Configuration,cls).__new__(cls)
        Configuration._obj.port=None
        Configuration._obj.has_exception=False
        Configuration._obj.exceptions=dict()
        if "port" in new_dict:
            Configuration._obj.port=new_dict["port"]
        return Configuration._obj
    def _validate_values(self):
        if Configuration._obj.port==None:
            Configuration._obj.exceptions["port"]=('V',"port entry is missing in configuration file, refer Documentation")
        elif isinstance(Configuration._obj.port,int)==False:
            Configuration._obj.exceptions["port"]=('T',f"port is of type {type(Configuration._obj.port)}, it should be of type {type(10)}")
        elif Configuration._obj.port<0 or Configuration._obj.port>49151:
            Configuration._obj.exceptions["port"]=('V',f"port number is {Configuration._obj.port}, it should be in range 0-49151")
        if len(Configuration._obj.exceptions)>0:
            Configuration._obj.has_exception=True
