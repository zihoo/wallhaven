# Wallhaven API for Python

## Description

Study project made for learning asyncronous I/O and HTML parsing in Python. Implements API to **[Wallhaven](https://wallhaven.cc)**.

## Requirements

* Python 3.4 or later
* asyncio
* aiohttp
* lxml

## Quick guide

```python
from wallhaven.base import Wallhaven

# Init client
wh = Wallhaven()

# Get list of 'Wallpaper' objects
wallpapers = wh.search(query='nature')

# Download wallpapers to specified directory
wh.download(wallpapers, save_to='/tmp')
```

## Wallhaven object

### Initializing client

Client can be initialized with `wallhaven.base.Wallhaven`:

```python
from wallhaven.base import Wallhaven

wh = Wallhaven()
```

You can pass `username` and `password` to sign in:

```python
wh = Wallhaven(username='my_username', password='my_password')
```

You can also pass custom `cookies` and `headers`:

```python
wh = Wallhaven(headers={'User-Agent': 'wallhaven_bot'})
```

### Retriving single wallpaper

Wallpaper can be retrieved with `wallpaper()` method. It takes `wallpaper_id` and returns `Wallpaper` object.

```python
wallpaper = wh.wallpaper(333676)
```

### Retrieving user info

User info can be retrieved with `user()` method. It takes `username` and returns `User` object.

```python
user = wh.user('cwarck')
```

### Searching wallpapers

`Wallhaven` has few methods for searching wallpapers:

* `search()`: Base search endpoint.
* `latest()`: Search latest wallpapers.
* `random()`: Search random wallpapers.

Following arguments can be passed to these methods:

* `query`: Search keyword.
* `categories`: A dictionary with categories of wallpapers.
    * Choices: 
        * `general` 
        * `anime` 
        * `people`
    * Default: `{'general': True, 'anime': True, 'people': True}`
    * Usage: `categories={'anime': False}`
* `purity`: A dictionary with content purity settings.
    * Choices:
        * `sfw`
        * `sketchy`
        * `nsfw`
    * Default: `{'sfw': True, 'sketchy': False, 'nsfw': False}`
    * Usage: `purity={'sfw': False, 'sketchy': True}`
* `resolutions`: Wallpapers resolutions.
    * Default: `[]`
    * Usage: `resolutions=['1920x1080', '2560x1600']`
* `ratios`: Wallpapers ratios.
    * Default: `[]`
    * Usage: `ratios=['4x3']`
* `sorting`: Sorting of results.
    * Choices:
        * `'relevance'`
        * `'random'`
        * `'date_added'`
        * `'views'`
        * `'favourites'`
    * Default: `'relevance'`
    * Usage: `sorting='views'`
* `order`: Ordering of results.
    * Choices:
        * `desc`
        * `asc`
    * Default: `desc`
    * Usage: `order='asc'`
* `page`: Page number.
    * Default: `1`
    * Usage: `page=2`   
* `count`: Number of wallpapers in result list.
    * Choices:
        * `24`: for all users.
        * `32`: for auhorized users.
        * `64`: for auhorized users.
    * Default: `24` if not signed in. Else `64`.
    * Usage: `count=10`

Examples:

```python
# Basic search
women = wh.search(
    query='women', 
    categories={'general': False},
    purity={'sketchy': True},
    resolutions=['2560x1600'],
)

# Random wallpapers
random = wh.random(resolutions=['1920x1080', count=1]

# Latest wallpapers
latest = wh.latest(count=10)
```

### Searching user uploads

You can search uploads of specific user with `Wallhaven.user_uploads()`. It takes `username` and following search params: 

* `purity`
* `page`
* `count`

### Downloading wallpapers

Wallpapers can be downloaded with `download()` method. It takes following arguments:

* `wallpapers`: List of `Wallpaper` objects, or single `Wallpaper`.
* `save_to`: Directory to save images. Default is current directory.

## Wallpaper object

Wallpaper is implemented with `wallhaven.wallpaper.Wallpaper`. 

All information about wallpaper is stored in `info`. It is a dictionary with following items:

* `added`
* `category`
* `colors`
* `favourites`
* `image_url`
* `purity`
* `resolution`
* `size`
* `source`
* `tags`
* `url`
* `user`
* `views`

All listed items are also available as `Wallpaper` attributes. `Wallpaper` can be also JSON-serialized with `json()` method.

## User object

User is implemented with `wallhaven.user.User`.

All information about user is stored in `info`. It is a dictionary with following items:

* `favorites`
* `forum_posts`
* `group`
* `joined`
* `last_active`
* `profile_comments`
* `profile_views`
* `subscribers`
* `uploads`
* `username`
* `wallpapers_flagged`
* `wallpapers_tagged`

All listed items are also available as `User` attributes. `User` can be also JSON-serialized with `json()` method.
