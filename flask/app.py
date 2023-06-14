from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@mysql.default:3306/myapp'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    short_bio = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, short_bio):
        self.name = name
        self.email = email
        self.short_bio = short_bio

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = []
    for user in users:
        results.append({'id': user.id, 'name': user.name, 'email': user.email, 'short_bio': user.short_bio})
    return {'users': results}

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    short_bio = request.json['short_bio']
    new_user = User(name, email, short_bio)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'User created successfully'}

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return {'id': user.id, 'name': user.name, 'email': user.email, 'short_bio': user.short_bio}
    return {'message': 'User not found'}, 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found'}, 404

    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    user.short_bio = request.json.get('short_bio', user.short_bio)
    db.session.commit()
    return {'message': 'User updated successfully'}

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found'}, 404

    db.session.delete(user)
    db.session.commit()
    return {'message': 'User deleted successfully'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')

# if __name__ == '__main__':
#     db.create_all()
#     app.run(host='0.0.0.0')
