import re
class ArticleForm :
    def  __init__(self,title,body):
        self.title = title
        self.body = body
        self.errors = {}
        
    def required(self,input) :
        if input.strip() == "" :
            return False
        else :
            return True
        
    def validate(self):
        if self.required(self.title) != True :
            self.errors['title'] = 'Empty title of article'
            
        if self.required(self.body) != True:
            self.errors['body'] = 'Empty body of article'
             
    def is_valid(self):
        if len(self.errors) == 0:
            return True
        else :
            return False
            
            
        
        