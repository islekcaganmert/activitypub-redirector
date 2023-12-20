from mastodon import Mastodon
from flask import Flask, request
import requests
import json
import re
import os

app = Flask(__name__)

def get_aas(domain):
    aas_data = requests.post('https://serveraas.pythonanywhere.com/protocols/aas/get', data={'domain':domain})
    if aas_data.status_code == 200: return aas_data.content.decode('UTF-8')
    else: return domain

@app.route('/user/<username>.json')
def instance_user(username):
    webfinger = requests.get(f"https://{get_aas(username.split('@')[2])}/.well-known/webfinger?resource=acct:{username.removeprefix('@')}").json()
    link = ''
    for i in webfinger['links']:
        if i['type'] == 'application/activity+json':
            link = i['href']
    return requests.get(link).json()

@app.route('/post/<id>.json')
def instance_post(id):
    return json.loads(requests.get(f"https://{get_aas(id.split('@')[1])}//{id.split('@')[0]}.json").content)

@app.route('/search/<key>.json')
def instance_search(key):
    return json.loads(requests.get(f"https://{get_aas(key.split('@')[1])}//{key.split('@')[0]}.json").content)

@app.route('/article/<id>.json')
def instance_article(id):
    return json.loads(requests.get(f"https://{get_aas(id.split('@')[1])}//{id.split('@')[0]}.json").content)

@app.route('/communities/<name>.json')
def instance_communities(name):
    return json.loads(requests.get(f"https://{get_aas(name.split('@')[1])}//{name.split('@')[0]}.json").content)

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

@app.route('/mastodon/status/<username>')
def mastodon_status(username):
    data = []
    try:
        mastodon_account = Mastodon(access_token=os.getenv('MASTODON_KEY'),api_base_url='https://mastodon.social').account_search(username)
        if username == re.sub(r"https:\/\/([\w\.]+)\/@(\w+)", r"@\2@\1", mastodon_account[0]['url']):
            return {'results':Mastodon(access_token=os.getenv('MASTODON_KEY'),api_base_url='https://mastodon.social').account_statuses(mastodon_account[0]['id'])}
        else: return {'results':[]}
    except: return {'results':[]}

@app.route('/.well-known/nodeinfo/<instance>.json')
def nodeinfo(instance):
    return requests.get(f"https://{instance}/.well-known/nodeinfo/2.0.json").json()

@app.route('/nodeinfo/2.0/<instance>.json')
def nodeinfo2(instance):
    return requests.get(f"https://{instance}/nodeinfo/2.0.json").json()

@app.route('/other_ends/<id>', methods=['GET','POST'])
def other_ends(id):
    if request.method == 'GET':
        r = requests.get(id.replace('%5C','/').replace('\\','/'))
    elif request.method == 'POST':
        r = requests.post(id.replace('%5C','/').replace('\\','/'), data=request.form)
    else:
        return 500
    try:
        return r.json()
    except:
        return r.content

@app.route('/other_ends', methods=['POST'])
def other_ends_p(id):
    if [i for i in request.form] == ['URL']:
        r = requests.get(request.form['URL'])
    else:
        d = {}
        for i in request.form:
            if i != 'URL':
                d.update({i: request.form[i]})
        r = requests.post(request.form['URL'], data=request.form)
    try:
        return r.json()
    except:
        return r.content

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
