import logging
import os.path
import json

from utils import var_path

l = logging.getLogger(__name__)

class Configuration(object):
    def __init__(self):
        self.path = var_path('config.json')
        if not os.path.exists(self.path):
            self.data = {}
        else:
            try:
                with open(self.path) as f:
                    self.data = json.load(f)
            except ValueError:
                l.error("Failed to load configuration file.  Using empty one "+
                        "instead.")
                self.data = {}
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
    def __getitem__(self, k):
        return self.data[k]
    def __setitem__(self, k, v):
        self.data[k] = v
        self.save()
    def __delitem__(self, k):
        del self.data[k]
        self.save()
    def __contains__(self, k):
        return k in self.data
