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

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)