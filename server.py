from flask_app import app
from flask_app.controllers import users, dojoMembers # ALWAYS IMPORT YOUR CONTROLLERS!!!

if __name__ == "__main__":
    app.run(debug=True)
