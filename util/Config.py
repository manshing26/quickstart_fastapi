import os
from getpass import getuser
from configparser import ConfigParser
from util.Argument import MY_argument

class MY_config:
    
    def __init__(self, my_argument:MY_argument, PWD:str):
        Cfilename = os.path.splitext(my_argument.get_value('config'))[0]
        path_file = os.path.join(PWD,'config',f'{Cfilename}.ini')
        assert os.path.exists(path_file), f'{path_file} not exist'
        
        self._configparser = ConfigParser()
        self._configparser.read(path_file)
        
        self._configparser.extra = {}
        self._configparser.add_section('Extra')
        
        # setup 'Extra'
        self.put_value_in_extra('PWD', PWD)
        self.put_value_in_extra('username', getuser())
        
        args = my_argument.get_all_value()
        for key in args:
            self.put_value_in_extra(key, args[key])
        
    def __get_value(self,section:str, key:str):
        assert self._configparser.has_section(section), f'No section "{section}"'
        assert self._configparser.has_option(section, key)
        
        return self._configparser.get(section, key)
    
    def get_string(self,section:str, key:str)->str:
        return str(self.__get_value(section, key))
    
    def get_int(self,section:str, key:str)->int:
        return int(self.__get_value(section, key))
    
    def put_value_in_extra(self, key:str, value:str)->bool:
        self._configparser['Extra'][key] = str(value)
        return True
    
    def put_value(self, section:str, key:str, value:str)->bool:
        assert self._configparser.has_section(section), f'No section "{section}"'
        self._configparser[section][key] = str(value)
        return True