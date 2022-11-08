from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash # For validation messages
import re	# the regex module

from flask_app.models import dojoMember

# create a regular expression object that we'll use later  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')


# we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)  

class User:
    db_name = "martial_arts_project_schema" # schema name

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.account_type = data["account_type"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.dojoMembers = []

    # Add methods to create a new user and more!
    @classmethod
    def user_registration(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password, account_type)
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(account_type)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None # Return None if there isnt any user found
        else:
            return cls(results[0]) # Create User object

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0]) # Create User object

    #get get all users added by logged in user
    @classmethod
    def get_all_user_member(cls, data):
        #query to grab all dojoMembers with the user who added them 
        query = """
        SELECT * FROM users 
        JOIN dojoMembers 
        ON users.id = dojoMembers.user_id  
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results)==0:
            return None
        else:
            #create user obj 
            user_obj = cls(results[0])
            #loop through each of our dojoMembers 
            for this_member in results:
                #grab the member's info
                member_dictionary = {
                    "id": this_member["id"],
                    "first_name": this_member["first_name"],
                    "last_name": this_member["last_name"],
                    "age": this_member["age"],
                    "location": this_member["location"],
                    "martial_type": this_member["martial_type"],
                    "plan_type": this_member["plan_type"],
                    "date_received": this_member["date_received"],
                    "created_at": this_member["dojoMembers.created_at"],
                    "updated_at": this_member["dojoMembers.updated_at"],
                }
                #create the member obj 
                member_obj = dojoMember.DojoMember(member_dictionary)
                #link thi member to this user
                user_obj.dojoMembers.append(member_obj)

            #return this user the member linked
            return user_obj




    # Static method that validate logins and registrations!
    @staticmethod
    def validate_registration(user_data):
        is_valid = True
        #check if all fields have at least something in them 
        if len(user_data['first_name']) < 1 or len(user_data['last_name']) < 1 or len(user_data['email']) < 1 or  len(user_data["password"]) < 1:
            flash("Field can not be empy!", "register")
            is_valid = False
        # Check first and last name are greater than 3 characters
        if len(user_data["first_name"]) < 2:
            flash("First name must be 2 or more characters", "register")
            is_valid = False
        if len(user_data["last_name"]) < 2:
            flash("Last name must be 2 or more characters", "register")
            is_valid = False
        # Check email to make sure format matches
        if not EMAIL_REGEX.match(user_data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False

        # Make sure email isn't taken already
        data = {
            "email": user_data["email"]
        }
        does_user_exist = User.get_user_by_email(data)
        if does_user_exist != None:
            flash("Email already taken", "register")
            is_valid = False

        # Minimum eight characters, at least one letter and one number
        if not PASS_REGEX.match(user_data["password"]): 
            flash("Minimum eight characters, at least one letter and one number!", "register")
            is_valid = False
        # Password must be 8 or more characters
        if len(user_data["password"]) < 8:
            flash("Password must be 8 or more characters", "register")
            is_valid = False
        # Passwords must match
        if user_data["password"] != user_data["confirm_password"]:
            flash("Passwords don't agree", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user_data):
        #check if all fields have at least something in them 
        if len(user_data['email']) < 1 or  len(user_data["password"]) < 1:
            flash("Field can not be empy!", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']): 
            flash("Invalid login credentials", "login") # Intentionally vague - so hackers aren't tipped off
            return False # Stop immediately - no need to check the password

        # Check to see if the email can be found
        data = {
            "email": user_data["email"]
        }
        does_user_exist = User.get_user_by_email(data)
        if does_user_exist == None:
            flash("Invalid login credentials", "login") # Intentionally vague - so hackers aren't tipped off
            return False # Stop immediately - no need to check the password
        # If the email is found, then check the password
        if not bcrypt.check_password_hash(does_user_exist.password, user_data["password"]):
            flash("Invalid login credentials", "login") # Intentionally vague - so hackers aren't tipped off
            return False # Stop here
        # Return user object that we can use for session since the credentials are good
        return does_user_exist