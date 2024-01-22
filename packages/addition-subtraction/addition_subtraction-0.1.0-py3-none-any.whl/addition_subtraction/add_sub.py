class AddSub:
    
    def __init__(self,method_val:int=1) -> None:
        if (type(method_val) != type(1)):
            self.method=1
            print('only integer elements accepted')
        elif ((method_val <= 1) and (method_val >= 0)):
            self.method = method_val
        else:
            self.method = 1
            print("Please enter a valid method by default addition operation has set")
        
    def operation(self,first_number:int=0,second_number:int=0)->int:
        if(self.method==0):
            return first_number-second_number
        elif(self.method==1):
            return first_number+second_number
    
    def change_method(self,method_val:int)->None:
        if(type(method_val)!=type(1)):
            print('only integer elements accepted, previous method has unchanged')
        elif((method_val<=1) and (method_val>=0)):
            self.method=method_val
        else:
            print("Please enter a valid method, previous method has unchanged")