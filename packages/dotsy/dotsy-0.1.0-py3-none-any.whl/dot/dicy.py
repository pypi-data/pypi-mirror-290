class dicy(dict):
    """Dictionary which allows dot access of its items"""
    
    def __getattr__(self, name):
        if name in self:
            value = self[name]
            return value # dicto(value) if type(value) is dict else value # Removed: autoconversion to dicto causes a copy, preventing write access
        else:
            raise AttributeError("No such attribute: " + name)
    
    def __setattr__(self, name, value):
        self[name] = value
    
    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
    
    def __dir__(self):
        return list(self.__dict__.keys()) + list(self.keys())

