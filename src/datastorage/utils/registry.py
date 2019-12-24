class BaseRegistry:
    
    def __init__(self):
        self.registry = {}
        
    def register(self, item):
        raise NotImplementedError("Method register() is not implemented")
        
    def get(self, name):
        raise NotImplementedError("Method get() is not implemented")
    
    def remove(self, name):
        raise NotImplementedError("Method remove() is not implemented")
