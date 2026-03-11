import os

class NLUConfig:
    def __init__(self):
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      self.train_data_path = os.path.join(BASE_DIR, "data", "ChatData.txt")
      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    nc=NLUConfig()
    print(nc.train_data_path)
