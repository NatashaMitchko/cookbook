# Cookbook Flask-Redis

## Recipe Data Structure

```json
{
    "title": "Tumeric Chickpea Stew",
    "slug": "tumeric-chickpea-stew",
    "description": "go-to easy meal",
    "ingredients": ["tumeric", "chickpeas", "coconut milk"],
    "steps": ["chop", "sautee", "stew", "serve"],
    "tags": ["quick", "vegan", "dinner", "fall", "winter"],
    "status": "PUBLISHED",
}
```

recipe mgmt goes under `/admin`

## User Data Strucutre

```json
{
    "username": str
    "password": hash(str)
}
```

user mgmt will go under `/auth`