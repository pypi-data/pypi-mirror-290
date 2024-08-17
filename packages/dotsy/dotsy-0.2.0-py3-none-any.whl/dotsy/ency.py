
from dotsy import dicy

class Ency():
    """
    'Encyclopedia' of dicts/dicys whose items can be directly dot-accessed on this object. Can have any members and
    methods, but the dicys (or dicts) that are to be dot-accessed must have their names passed in to the
    super() constructor, after being assigned to member variables with those names.
    """
    
    def __init__(self, dict_names):  # Must be called AFTER all the dicts/dicys are initialized
        self.__dict_names__ = dict_names
        self.__initialized__ = True
    
    def __getattr__(self, name):
        def wrap(x):
            return x  # return Dicy(x) if type(x) is dict else x # Removed: autoconversion to dicy causes a copy, preventing write access

        # print(f"Get: {name}")
        if name == "__initialized__":  # Only reached if the variable wasn't defined yet, so we know the answer
            return False
        if name in self.__dict__.keys():
            return wrap(super().__getattribute__(name))
        
        for dn in self.__dict_names__:
            d = super().__getattribute__(dn)
            if name in d:
                return wrap(d[name])
        
        # If reaching this point, couldn't be found
        raise AttributeError("No such attribute: " + name)
    
    # Removed: autoconversion to dicy causes a copy, preventing write access
    # def __getattribute__(self, name):
    #     x = super().__getattribute__(name)
    #     if name != "__dict__" and type(x) is dict:
    #         x = Dicy(x)
    #     return x
    
    def __setattr__(self, name, value):
        # print(f"Set: {name}")
        if (not self.__initialized__) or name in self.__dict__.keys():  #
            super().__setattr__(name, value)
            return
        
        for dn in self.__dict_names__:
            d = super().__getattribute__(dn)
            if name in d:
                d[name] = value
                return
        
        # If reaching this point, couldn't be found
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        # print(f"Del: {name}")
        if name in ("__initialized__", "__dict_names__"):
            raise AttributeError("Cannot delete attribute: " + name)
        if name in self.__dict__.keys():
            # print("deleting attribute")
            super().__delattr__(name)
            return
        
        for dn in self.__dict_names__:
            d = super().__getattribute__(dn)
            if name in d:
                # print("deleting from dict")
                del d[name]
                return
        
        # If reaching this point, couldn't be found
        raise AttributeError("No such attribute: " + name)
    
    def __dir__(self):
        attribs = list(self.__dict__.keys())
        for dn in self.__dict_names__:
            d = super().__getattribute__(dn)
            attribs += list(d.keys())
        return attribs


    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
        #self.__initialized__ = True


# class custom_dotcontainer_example():
#     def __init__(self, dict1: Dicy = None, dict2: Dicy = None):
#         if dict1 is None:
#             dict1 = Dicy()
#         if dict2 is None:
#             dict2 = {}
#
#         self.dict1 = dict1.copy()
#         self.dict2 = dict2.copy()
#
#         self.__initialized__ = True  # Must be the FINAL line of init
#
#     def __getattr__(self, name):
#         if name == "__initialized__":  # Only reached if the variable wasn't defined yet, so we know the answer
#             return False
#         if name in self.__dict__.keys():
#             return super().__getattribute__(name)
#         elif name in self.dict1:
#             return self.dict1[name]
#         elif name in self.dict2:
#             return self.dict2[name]
#         else:
#             raise AttributeError("No such attribute: " + name)
#
#     def __setattr__(self, name, value):
#         if not self.__initialized__ or name in self.__dict__.keys():  #
#             super().__setattr__(name, value)
#         elif self.dict1 and name in self.dict1:
#             self.dict1[name] = value
#         elif self.dict2 and name in self.dict2:
#             self.dict2[name] = value
#         else:
#             super().__setattr__(name, value)
#
#     def __delattr__(self, name):
#         if name == "__initialized__":
#             raise AttributeError("Cannot delete attribute: " + name)
#         if name in self.__dict__.keys():
#             super().__delattr__(name)
#         elif name in self.dict1:
#             del self.dict1[name]
#         elif name in self.dict2:
#             del self.dict2[name]
#         else:
#             raise AttributeError("No such attribute: " + name)
#
#     def __dir__(self):
#         return list(self.__dict__.keys()) + list(self.dict1.keys()) + list(self.dict2.keys())

