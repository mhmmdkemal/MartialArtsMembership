from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # For validation messages
from flask_app.models import user

class DojoMember:
    db_name = "martial_arts_project_schema" # schema name

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.age = data["age"]        
        self.location = data["location"]
        self.martial_type = data["martial_type"]
        self.plan_type = data["plan_type"]
        self.date_received = data["date_received"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #class method that adds a member to the database
    @classmethod
    def add_member_to_db(cls, data):
        query = """INSERT INTO dojoMembers 
        (first_name, last_name, age , location , martial_type, plan_type, date_received, user_id, created_at, updated_at) 
        VALUES ( %(first_name)s, %(last_name)s, %(age)s , %(location)s , %(martial_type)s, %(plan_type)s , %(date_received)s , %(user_id)s, NOW() , NOW() );
        """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )


    #add a new dojoMember
    @classmethod
    def get_all_member(cls):
        #query to grab all dojoMembers with theuser who added them 
        query = """
        SELECT * FROM dojoMembers 
        JOIN users 
        ON dojoMembers.user_id = users.id ;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        #if we dont find any dojoMembers return an empty list 
        if len(results)==0:
            return []
        else:
            all_dojoMember_object = [] # this will hold Trails
            for dojoMember_dictionary in results:
                
                #create the dojoMember 
                dojoMember_obj = cls(dojoMember_dictionary)
                # Grab the user object 
                user_dictionary = {
                    "id": dojoMember_dictionary["users.id"],
                    "first_name": dojoMember_dictionary["users.first_name"],
                    "last_name": dojoMember_dictionary["users.last_name"],
                    "email": dojoMember_dictionary["email"],
                    "password": dojoMember_dictionary["password"],
                    "account_type": dojoMember_dictionary["account_type"],
                    "created_at": dojoMember_dictionary["users.created_at"],
                    "updated_at": dojoMember_dictionary["users.updated_at"],
                }

                # create user object 
                user_obj = user.User(user_dictionary)
                # Link this user to this dojoMemberi 
                dojoMember_obj.user = user_obj
                #add this dojoMember to the list of all dojoMember objects 
                all_dojoMember_object.append(dojoMember_obj)
            return all_dojoMember_object
    
    #get a single dojoMember for that user
    @classmethod
    def get_one_member(cls, data):
        #query to grab all dojoMembers with theuser who added them 
        query = """
        SELECT * FROM dojoMembers 
        JOIN users 
        ON dojoMembers.user_id = users.id 
        WHERE dojoMembers.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        #if we dont find any dojoMembers return an empty list 
        if len(results)==0:
            return None
        else:
            dojoMember_dictionary = results[0]
            #create the dojoMember 
            dojoMember_obj = cls(dojoMember_dictionary)
            # Grab the user object 
            user_dictionary = {
                "id": dojoMember_dictionary["users.id"],
                "first_name": dojoMember_dictionary["users.first_name"],
                "last_name": dojoMember_dictionary["users.last_name"],
                "email": dojoMember_dictionary["email"],
                "password": dojoMember_dictionary["password"],
                "account_type": dojoMember_dictionary["account_type"],
                "created_at": dojoMember_dictionary["users.created_at"],
                "updated_at": dojoMember_dictionary["users.updated_at"],
            }
            # create user object 
            user_obj = user.User(user_dictionary)
            # Link this user to this dojoMemberi 
            dojoMember_obj.user = user_obj
        return dojoMember_obj

    #class method to update a specific member
    @classmethod
    def update_member(cls, data):
        query= """
        UPDATE dojoMembers SET 
        first_name = %(first_name)s, 
        last_name = %(last_name)s, 
        age = %(age)s,
        location = %(location)s,
        martial_type = %(martial_type)s,
        plan_type = %(plan_type)s,
        date_received = %(date_received)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    #class method to delete a specfic member
    @classmethod
    def delete_member(cls, data):
        query="""DELETE FROM dojoMembers WHERE id = %(id)s"""
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Static method that validate logins and registrations!
    @staticmethod
    def validate_member(form_data):
        print(form_data)
        is_valid = True
        # #check if all fields have at least something in them 
        if len(form_data['first_name']) < 1 or len(form_data['last_name']) < 1 or len(form_data['age']) < 1:
            flash("Field can not be empy!", "register")
            is_valid = False
        # Check first and last name are greater than 3 characters
        if len(form_data["first_name"]) < 3:
            flash("First Name must be 5 or more characters")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last Name  must be 2 or more characters")
            is_valid = False
        if len(form_data["age"]) > 50:
            flash("age must be less than 50 characters")
            is_valid = False
        return is_valid