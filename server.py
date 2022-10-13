from flask_app import app

# # remember to import controllers
from flask_app.cotrollers import recipe_controller
from flask_app.cotrollers import user_controller

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)