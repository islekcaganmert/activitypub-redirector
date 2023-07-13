from flask import Flask
import requests

app = Flask(__name__)

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
