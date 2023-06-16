import logging
import os.path as path
from util.Config import MY_config
from util.Datetime import get_date

def get_logger(my_config:MY_config)->logging.Logger:
    '''
    level = {
        'D':debug,
        'I':Info,
        'W':Warning,
        'E':Error,
    }
    '''
    level = my_config.get_string('Log', 'level')
    all_level = {
        'D':logging.DEBUG,
        'I':logging.INFO,
        'W':logging.WARNING,
        'E':logging.ERROR,
    }
    filtered_level = all_level[level] if level in all_level.keys() else logging.DEBUG
    
    formatter = logging.Formatter(
        fmt='%(asctime)s %(name)-9s %(levelname)-7s %(message)s',
        datefmt=r'%d-%m-%Y %H:%M:%S',
    )
    
    logging.captureWarnings(True)
    my_logger = logging.getLogger(my_config.get_string('Extra', 'username'))
    my_logger.setLevel(filtered_level)
    
    # console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(filtered_level)
    console_handler.setFormatter(formatter)
    
    # file
    filename = path.join(my_config.get_string("Extra", "PWD"),'logs',f'{get_date()}.log')
    file_handler = logging.FileHandler(
        filename=filename,
        mode='a',
        encoding=None,
        delay=False
        )
    file_handler.setLevel(filtered_level)
    file_handler.setFormatter(formatter)
    
    my_logger.addHandler(console_handler)
    my_logger.addHandler(file_handler)
    my_logger.propagate = False
        
    return my_logger
