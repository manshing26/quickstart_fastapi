import os

def build_structure(PWD):
    
    # tmp folder
    if not os.path.isdir(os.path.join(PWD,'tmp')):
        os.mkdir(os.path.join(PWD,'tmp'))
        
    if not os.path.isdir(os.path.join(PWD,'logs')):
        os.mkdir(os.path.join(PWD,'logs'))

    if not os.path.isdir(os.path.join(PWD,'config')):
        os.mkdir(os.path.join(PWD,'config'))
        
    return