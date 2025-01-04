# many to many relationship 
# user - role. user has many roles example: admin, author, writer etc.
# roles has many users


# one to many realtionship between two table 
# user - posts(one to many)
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(200), nullable=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    posts = db.relationship('Post', backref="author", lazy=True)
    roles=db.relationship('Role', backref="user", secondary="user_role")



class Profile(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    bio=db.Column(db.String(200), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user=db.relationship('User', uselist=False, back_populates='profile')

# post
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    description=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# many to many 
# role table   
class Role(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)

# user-role table 
user_roles=db.Table('user_roles',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),primary_key=True),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id'),primary_key=True)
                    )

# create all table 
with app.app_context():
    #db.drop_all()
    db.create_all()


# how to add post
@app.route('/post-add')
def addPost():
    user=User.query.get(1)
    #post=Post(title='post title', description="post description"user_id=user.id)
    posts =[
         Post(title='post title1', description="post description1", author=user),
         Post(title='post title2', description="post description2", author=user),
         Post(title='post title4', description="post description4", author=user)
    ]
    for post in posts:
        db.session.add(post)


    db.session.commit()
    post=Post.query.all()
    return jsonify({'message':'post added successfully'})

# how to fetch posts
@app.route('/posts')
def getPosts():
    posts=Post.query.all()
    post_list=[]
    for post in posts:
        post_data={
            'id':post.id,
            'title':post.title,
            'description':post.description,
            'auther':post.author.name
        }
        post_list.append(post_data)
    return jsonify(post_list)

@app.route('/roles')
def getRoles():
    roles=Role.query.all()
    role_list=[]
    for role in roles:
        role_data={
            'id':role.id,
            'name':role.name,
            'user':[]
        }
        for user in role.user:
            user_data={
                'name':user.name,
            }
            role_data['users'].append(user_data)
        role_list.append(role_data)
    return jsonify(role_list)


# how to add user
@app.route('/user-add')
def addUser():
    user=User(name='Test user')
    profile=Profile(bio='test user profile')

    roles=[
        Role(name="Admin"),
        Role(name="Moderator"),
        Role(name="User")
    ]
    for role in roles:
        user.roles.append(roles)

    user.profile=profile
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'User added successfully'})

# how to fetch user
@app.route('/users')
def getUser():
    users=User.query.all()
    user_list=[]
    for user in users:
        user_data={
            'id':user.id,
            'name':user.name,
            'bio':user.profile.bio,
            'roles':[],
            'posts':[]
        }
        for post in user.posts:
            post_data={
                'title':post.title,
                'description':post.description,
            }
            user_data['posts'].append(post_data)

        for role in user.roles:
            role_data={
                'name':role.name,
            }
            user_data['roles'].append(role_data)
        
        user_list.append(user_data)
    return jsonify(user_list)

# how to fetch profile
@app.route('/profiles')
def getProfile():
    profiles=Profile.query.all()
    profile_list=[]
    for profile in profiles:
        profile_data={
            'id':profile.id,
            'bio':profile.bio,
            'user_name':profile.user.name
        }
        profile_list.append(profile_data)
    return jsonify(profile_list)
    

@app.route('/')
def index():
    return jsonify({'message':'home page'})

if __name__=='__main__':
    app.run(debug=True)