from Inventory import *
from Procurement import *
from HR import *
from Finance import *
from Sales import *

class Facade():
    def __init__(self):
        self.products = []
        self.suppliers = []
        self.stores = []        
        self.departments = []   
        self.staff = []    
        self.purchaseorders = []   
        self.sales = []
        
    def TriggerPurchaseOrder():
        