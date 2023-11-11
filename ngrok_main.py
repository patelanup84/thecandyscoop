from flask import Flask, render_template
from google.cloud import datastore

app = Flask(__name__)
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)

# Initialize the Google Datastore client
datastore_client = datastore.Client()

# Function to get posts from Datastore
def get_posts(limit=9, category=None):
    query = datastore_client.query(kind='Post')
    if category:
        query.add_filter('category', '=', category)
    query.order = ['-created_at']  # Assuming you have a 'created_at' property
    results = list(query.fetch(limit=limit))
    return results

# Function to get the three most recent posts for the footer
def get_recent_posts(limit=3):
    return get_posts(limit)

# Function to get team members from Datastore
def get_team_members():
    query = datastore_client.query(kind='TeamMember')
    query.order = ['name']
    results = list(query.fetch())
    return results

@app.route('/')
def home():
    posts = get_posts()
    recent_posts = get_recent_posts()
    return render_template('index.html', posts=posts, recent_posts=recent_posts, hero_image='https://fakeimg.pl/1920x800', hero_text='Welcome to MySite!')

@app.route('/about')
def about():
    team_members = get_team_members()
    recent_posts = get_recent_posts()
    return render_template('about.html', team_members=team_members, recent_posts=recent_posts, hero_image='https://fakeimg.pl/1920x800', hero_text='About Us')

@app.route('/category/<category_name>')
def category(category_name):
    posts = get_posts(category=category_name)
    recent_posts = get_recent_posts()
    hero_image = f'images/hero-{category_name}.jpg'  # Assuming you have a hero image for each category
    hero_text = f'{category_name} Category'  # Custom hero text for each category
    return render_template('category.html', posts=posts, recent_posts=recent_posts, hero_image='https://fakeimg.pl/1920x800', hero_text=hero_text, category_name=category_name)

@app.route('/post/<int:post_id>')
def post(post_id):
    key = datastore_client.key('Post', post_id)
    post = datastore_client.get(key)
    recent_posts = get_recent_posts()
    if not post:
        return 'Post not found', 404
    return render_template('post.html', post=post, recent_posts=recent_posts, hero_image='https://fakeimg.pl/1920x800', hero_text=post['title'])

# Add more routes for additional pages if needed

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)