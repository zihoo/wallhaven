"""Routing."""

import os


class Router:
    """URL manager."""

    base = 'https://alpha.wallhaven.cc'
    favorites = os.path.join(base, 'favorites')
    latest = os.path.join(base, 'latest')
    random = os.path.join(base, 'random')
    search = os.path.join(base, 'search')
    login = os.path.join(base, 'auth', 'login')

    def favorite(self, favorite_id):
        """Favorite page."""
        return os.path.join(self.base, 'favorites', favorite_id)

    def wallpaper(self, wallpaper_id):
        """Wallpaper page."""
        return os.path.join(self.base, 'wallpaper', str(wallpaper_id))

    def image(self, image_name):
        """Image page."""
        return os.path.join(self.base, 'wallpapers', 'full', image_name)

    def user(self, username):
        """User profile."""
        return os.path.join(self.base, 'user', username)

    def user_uploads(self, username):
        """User uploads."""
        return os.path.join(self.base, 'user', username, 'uploads')


router = Router()
