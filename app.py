from mastodon import Mastodon
from flask import Flask
import requests
import re
import os

app = Flask(__name__)

@app.route('/user/<username>.json')
def instance_user(username):
    return requests.get(f"https://{username.split('@')[2]}/user/{username.split('@')[1]}.json").json()

@app.route('/post/<id>.json')
def instance_post(id):
    return requests.get(f"https://{id.split('@')[2]}//{id.split('@')[1]}.json").json()

@app.route('/search/<key>.json')
def instance_search(key):
    return requests.get(f"https://{key.split('@')[2]}//{key.split('@')[1]}.json").json()

@app.route('/article/<id>.json')
def instance_article(id):
    return requests.get(f"https://{id.split('@')[2]}//{id.split('@')[1]}.json").json()

@app.route('/communities/<name>.json')
def instance_communities(name):
    return requests.get(f"https://{name.split('@')[2]}//{name.split('@')[1]}.json").json()

@app.route('/users/<username>.json')
def userpage(username):
    return requests.get(f"https://{username.split('@')[2]}/users/{username.split('@')[1]}.json").json()

@app.route('/users/<username>/outbox')
def outbox(username):
    return requests.get(f"https://{username.split('@')[2]}/users/{username.split('@')[1]}/outbox?page=true").json()

@app.route('/users/<username>/followers.json')
def followers(username):
    return requests.get(f"https://{username.split('@')[2]}/users/{username.split('@')[1]}/followers.json").json()

@app.route('/users/<username>/following.json')
def following(username):
    return requests.get(f"https://{username.split('@')[2]}/users/{username.split('@')[1]}/following.json").json()

@app.route('/search/<instance>/<key>')
def search(instance,key):
    data = []
    try:
        for account in Mastodon(access_token=os.getenv('MASTODON_KEY'),api_base_url='https://mastodon.social').account_search(key):
            if not re.sub(r"https:\/\/([\w\.]+)\/@(\w+)", r"@\2@\1", account['url']) == account['url']:
                data.append({"username":account['username'],"email":'activitypub:::'+re.sub(r"https:\/\/([\w\.]+)\/@(\w+)", r"@\2@\1", account['url']),"status":'',"biography":'',"tokens":0,"badges":[],"plus":False})
    except: pass
    return {'results':data}

@app.route('/docs')
def docs():
    return '''
        <h1>activitypub-redirector</h1>
        <p>Created for being an API gives ability of basic activitypub connectivity to servers with whitelist based firewalls. This can be used as API. As you can understand from repository name, it is just a redirector project, only functionality is restricted redirecting...</p>
        <h3>Tutorial</h3>
        <p>'/users/@username@example.org.json' => https://example.org/users/username.json</p>
        <p>'/users/@username@example.org/outbox' => https://example.org/users/username/outbox?page=true</p>
        <p>'/users/@username@example.org/followers.json' => https://example.org/users/username/followers.json</p>
        <p>'/users/@username@example.org/following.json' => https://example.org/users/username/following.json</p>
        <h3>WARNING</h3>
        <p>By using official deployment, you are accepting that we do not have any responsibility on your usage...</p>
    '''

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
