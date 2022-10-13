from pprint import pprint
from flask_app import flash
from flask_app.cofig.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User

DATABASE = 'recipes'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.user = data['user']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __repr__(self):
        return f'<Recipe: {self.setup}>'

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 2:
            flash('name must be at least two characters.', 'name')
            is_valid = False
        if len(form['description']) < 2:
            flash('Descrtiption must be at least two characters.', 'description')
            is_valid = False
        if len(form['instructions']) < 10:
            flash('instructions must be at least two characters.', 'instructions')
            is_valid = False
        if not form['under_30']:
            flash('Please select yes or no.', 'under_30')
            is_valid = False
        if not form['date_made']:
            flash('Please enter release date.', 'date_made')
            is_valid = False
        return is_valid

    # create a recipe
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s);'
        recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        return recipe_id

    # find all recipes (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from recipes;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        recipes = []
        for result in results:
            user_data = {
                'id': result['user_id']
            }
            user = User.find_by_id(user_data)
            recipe_data = {
                'id': result['id'],
                'name': result['name'],
                'description': result['description'],
                'instructions': result['instructions'],
                'under_30': result['under_30'],
                'date_made': result['date_made'],
                'user_id': result['user_id'],
                'user': user,
                'created_at': result['created_at'],
                'updated_at': result['updated_at']
            }
            recipe = Recipe(recipe_data)
            recipes.append(recipe)
        return recipes

    # find one recipe by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    # find one recipe by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user_data = {
            'id': results[0]['user_id']
        }
        user = User.find_by_id(user_data)
        recipe_data = {
            'id': results[0]['id'],
            'name': results[0]['name'],
            'description': results[0]['description'],
            'instructions': results[0]['instructions'],
            'under_30': results[0]['under_30'],
            'date_made': results[0]['date_made'],
            'user_id': results[0]['user_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'user': user,

        }
        recipe = Recipe(recipe_data)
        return recipe

    # update one recipe by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one recipe by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True