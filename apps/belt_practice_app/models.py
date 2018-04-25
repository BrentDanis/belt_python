from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
    	# put validations here in Models
        results = {
            'status': False
        }
        #capture errors in dictonary
        errors = {};
        if len(postData['first_name']) < 2:
            errors['first_name'] = "At least 2 characters for First Name"
        if not postData['first_name'].isalpha:
            errors['first_name_alpha'] = "Letters Only for Names"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "At least 2 characters for Last Name"
        if not postData['last_name'].isalpha:
            errors['last_name_alpha'] = "Letters Only for Names"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Need proper email buddy!"
        if postData['birthday'] > time.strftime("%Y-%m-%d"):
            errors['bday'] = 'Must be born before yesterday, good try though.'
        if len(postData['password']) < 8:
            errors['password_length'] = "8 character min for Passwords"
        if postData['password'] != postData['conf']:
            errors['unmatched'] = "Try again - Passwords dont Match"
        results['errors'] = errors
        if len(errors) == 0:
            results['status'] = True
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            #create new user here ?? Print the results below as well
            results['newUser'] = self.create(
            	first_name=postData['first_name'],
            	last_name=postData['last_name'], 
            	email=postData['email'], 
            	password=hash_pw
            	)       
        print(results)
        return results
    def login_validator(self, postData):
    	# put validations here in Models
        results = {
            'status': False
        }
        #catpure errors in dictionary 
        errors = {};
        check_user = User.objects.filter(email = postData['email'])
        check_pass = postData['password']
        if not check_user:
            errors['noUser'] = "Email does not exits in our records. Please register above"    
        elif not bcrypt.checkpw(check_pass.encode(), check_user[0].password.encode()):
            errors['wrongPW'] = "Incorrect password"
        results['errors'] = errors
        if len(errors) == 0:
            results['status'] = True;
            results['user'] = check_user[0]
        return results
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #how to skip birthday validation - False and with default ----AAAHHHHHHH!!!!!!!!!!!!
    birthday = models.DateField(auto_now = False, auto_now_add = False, default= '1981-05-02')
    objects = UserManager()
    def __repr__(self):
        return self.first_name;

class quoteManager(models.Manager):
    def quote_validator(self, id, postData):
        results = {
            'status': False
        }
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name must be at least 3 letters long."
        if len(postData['content']) < 10:
            errors['quote'] = "Quote must be at least 10 characters long."
        results['errors'] = errors
        if len(errors) == 0:
            results['new_quote'] = self.create(
            	author=postData['author'], 
            	content=postData['content'], 
            	posted_by = User.objects.get(id = id)
            	) 
            results['status'] = True
        return results
#create function to favorite the book - will use Like on front end-will this like it??
    def faveQuote(self, id, postData):
        user = User.objects.get(id = id)
        quote = self.get(id = postData['this_quote'])
        quote.faved_by.add(user)
#cut and paste for unfaveQuote below: will use Drop on front end-will this drop it??
#i want to puke!!!
    def unfaveQuote(self, id, postData):
        user = User.objects.get(id = id)
        quote = self.get(id = postData['this_quote'])
        quote.faved_by.remove(user)
        

class Quote(models.Model):
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="quotes")
    faved_by = models.ManyToManyField(User, related_name="faves")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = quoteManager()
    def __str__(self):
        return self.author
