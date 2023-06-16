import argparse

class MY_argument():
    def __init__(self):
        super().__init__()
        self._argparser = argparse.ArgumentParser()

    def get_instance(self)->argparse.ArgumentParser:
        return self._argparser
    
    def get_value(self, key):
        args = self._argparser.parse_args()
        return getattr(args, key)
    
    def get_all_value(self):
        args = self._argparser.parse_args()
        return vars(args)