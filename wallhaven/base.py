"""Base."""

import asyncio
import cgi
from collections import namedtuple
import os

import aiohttp
from lxml import html

from routing import router
from search import get_search_params
from user import User
from wallpaper import Wallpaper


Response = namedtuple(
    'Response',
    ['page', 'status', 'content_type', 'url']
)


class WallpaperIsBlocked(Exception):
    """Wallpaper is forbidden for unauthorized users."""
    pass


class WallpaperNotFound(Exception):
    """Wallpaper/image is not found."""
    pass


class UserNotFound(Exception):
    """User is not found."""
    pass


class Wallhaven:
    """Wallhaven client."""

    def __init__(self, username=None, password=None, headers=None, cookies=None):
        """Init."""
        self.username = username
        self.password = password
        self.headers = headers or {}
        self.cookies = cookies or {}

        if self.username and self.password:
            self.login(self.username, self.password)

    @asyncio.coroutine
    def get_token(self):
        """Get authentication token."""
        response = yield from self.get(router.base)
        tree = html.fromstring(response.page)
        element = tree.xpath('//*[@id="login"]/input')[0]
        token = element.attrib.get('value')
        return token

    @asyncio.coroutine
    def _login(self, username, password):
        """Coroutine which performs authentication request."""
        token = yield from self.get_token()

        payload = {
            '_token': token,
            'username': username,
            'password': password
        }

        response = yield from aiohttp.request('post', router.login, data=payload)
        cookies = response.cookies
        yield from response.release()

        if cookies:
            self.cookies = cookies

    def login(self, username, password):
        """Login to wallhaven."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._login(username, password))

    @asyncio.coroutine
    def read(self, response):
        """Read content according to the content-type."""
        content_type = None
        content = None

        if response.status == 200:
            content_type = response.headers.get('content-type')

            if content_type:
                content_type, _ = cgi.parse_header(content_type)

                if content_type == 'text/html':
                    content = yield from response.text()
                elif content_type in ('image/jpeg', 'image/png'):
                    content = yield from response.read()

        resp = Response(page=content,
                        status=response.status,
                        content_type=content_type,
                        url=response.url)

        yield from response.release()
        return resp

    @asyncio.coroutine
    def get(self, *args, **kwargs):
        """Coroutine which performs GET request."""
        response = yield from aiohttp.request('get', *args, **kwargs)
        return (yield from self.read(response))

    @asyncio.coroutine
    def get_page(self, url, sem=None, params=None):
        """Wrapper around 'self.get'. Returns page content. If 'sem' is defined
        then 'asyncio.Semaphore' will be used to limit simultaneous requests.
        """
        if not params:
            params = {}

        kwargs = {
            'cookies': self.cookies,
            'headers': self.headers,
            'params': params
        }

        if sem:
            with (yield from sem):
                resp = yield from self.get(url, **kwargs)
        else:
            resp = yield from self.get(url, **kwargs)

        return resp

    @asyncio.coroutine
    def get_pages(self, urls):
        """Get pages asyncronously."""
        sem = asyncio.Semaphore(4)
        tasks = [self.get_page(url, sem) for url in urls]
        return [(yield from f) for f in asyncio.as_completed(tasks)]

    def fetch(self, urls, params=None):
        """Performs GET request."""
        if isinstance(urls, (list, tuple)):
            task = self.get_pages(urls)
        else:
            task = self.get_page(urls, params=params)

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(task)

    def download(self, wallpapers, save_to=None):
        """Download wallpapers to specified directory."""
        if not save_to:
            save_to = os.getcwd()

        if not isinstance(wallpapers, (list, tuple)):
            wallpapers = [wallpapers]

        urls = [w.image_url for w in wallpapers]
        response = self.fetch(urls)

        for item in response:
            if item.status == 200:
                file_name = item.url.split('/')[-1]
                with open(os.path.join(save_to, file_name), 'wb') as f:
                    f.write(item.page)
            elif item.status == 404:
                raise WallpaperNotFound(item.url)

    def _get_wallpaper(self, response):
        """Get wallpaper."""
        if response.status == 200:
            return Wallpaper(response.page)
        elif response.status == 403:
            raise WallpaperIsBlocked(response.url)
        elif response.status == 404:
            raise WallpaperNotFound(response.url)

    def _get_user(self, response):
        """Get user."""
        if response.status == 200:
            return User(response.page)
        elif response.status == 404:
            raise UserNotFound(response.url)

    def wallpaper(self, wallpaper_id):
        """Get wallpaper."""
        response = self.fetch(router.wallpaper(wallpaper_id))
        return self._get_wallpaper(response)

    def user(self, username):
        """User."""
        response = self.fetch(router.user(username))
        return self._get_user(response)

    def search(self, route=None, count=None, **kwargs):
        """Search wallpapers."""
        if not route:
            route = router.search

        max_count = 24
        if not count:
            if self.cookies:
                max_count = 64
            count = max_count

        params = get_search_params(route, **kwargs)
        response = self.fetch(route, params=params)
        if 'user' in route and response.status == 404:
            raise UserNotFound(response.url)

        tree = html.fromstring(response.page)
        urls = [x.attrib['href'] for x in tree.find_class('preview')]

        if urls:
            response = self.fetch(urls[:count])
            return [self._get_wallpaper(item) for item in response]

        return []

    def user_uploads(self, username, count=None, **kwargs):
        """User uploads."""
        route = router.user_uploads(username)
        return self.search(route=route, count=count, **kwargs)

    def latest(self, count=None, **kwargs):
        """Latest wallpapers."""
        kwargs['sorting'] = 'date_added'
        kwargs['order'] = 'desc'
        return self.search(count=count, **kwargs)

    def random(self, count=None, **kwargs):
        """Random wallpapers."""
        kwargs['sorting'] = 'random'
        return self.search(count=count, **kwargs)
