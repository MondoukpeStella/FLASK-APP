import re
class UpdateForm :
    def  __init__(self,username,email) -> None:
        self.username = username
        self.email = email
        self.errors = {}
        
    def required(self,input) :
        if input.strip() == "" :
            return False
        else :
            return True
        
    def valid_email(self,input) :
        pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        if re.match(pattern, input) :
            return True
        else :
            return False
        
    def validate(self):
        if self.required(self.username) != True :
            self.errors['username'] = 'Empty username'
            
        if self.required(self.email) != True:
            self.errors['email'] = 'Empty email'
            
        if self.valid_email(self.email) !=True:
             self.errors['email'] = 'Invalid email'
             
    def is_valid(self):
        if len(self.errors) == 0:
            return True
        else :
            return False
            
            
        
        