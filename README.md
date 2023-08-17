# activitypub-redirector
Created for giving ability of basic activitypub connectivity to servers with whitelist based firewalls. As you can understand from repository name, it is just a redirector project, only functionality is restricted redirecting...
### Tutorial

`'/users/@username@example.org.json' => https://example.org/users/username.json`

`'/users/@username@example.org/outbox' => https://example.org/users/username/outbox?page=true`

`'/users/@username@example.org/followers.json' => https://example.org/users/username/followers.json`

`'/users/@username@example.org/following.json' => https://example.org/users/username/following.json`

### WARNING
By using official deployment, you are accepting that we do not have any responsibility on your usage.