import re
class RegisterForm :
    def  __init__(self,username,email,password,password_conf):
        self.username = username
        self.email = email
        self.password = password
        self.password_conf = password_conf
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
            
        if self.required(self.password) != True :
            self.errors['password'] = 'Empty password'
            
        if self.required(self.password_conf) != True :
            self.errors['password_conf'] = 'Empty password_conf'
            
        if self.password != self.password_conf :
            self.errors['password_conf'] = "Password don't match"
            
        if self.valid_email(self.email) !=True:
             self.errors['email'] = 'Invalid email'
             
    def is_valid(self):
        if len(self.errors) == 0:
            return True
        else :
            return False
            
            
        
        