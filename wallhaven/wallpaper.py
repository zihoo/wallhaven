"""Wallpaper."""

import json

from lxml import html


class Wallpaper:
    """Wallpaper."""

    def __init__(self, content):
        """Init."""
        self.tree = html.fromstring(content)
        self.info = self.get_info()

        for key, value in self.info.items():
            setattr(self, key, value)

    def get_source(self):
        """Get source."""
        element = self.tree.find_class('showcase-source')[0]
        child = element.getchildren()[0]
        return child.text

    def get_resolution(self):
        """Get resolution."""
        element = self.tree.find_class('showcase-resolution')[0]
        return element.text.replace(' ', '')

    def get_color_palette(self):
        """Get color palette."""
        element = self.tree.find_class('color-palette')[0]
        colors = element.getchildren()
        return [c.attrib['style'][17:] for c in colors]

    def get_tags(self):
        """Get tags."""
        element = self.tree.xpath('//*[@id="tags"]')[0]
        tags = []
        for item in element.getchildren():
            tag_id = item.attrib.get('data-tag-id')
            tag_alias = item.getchildren()[0].text
            tags.append((tag_id, tag_alias))
        return tags

    def get_purity(self):
        """Get purity."""
        element = self.tree.xpath('//*[@id="wallpaper-purity-form"]/fieldset')[0]
        childs = element.getchildren()

        for button, label in (childs[i:i+2] for i in range(0, len(childs), 2)):
            if button.attrib.get('checked'):
                return label.text
        return None

    def get_properties(self):
        """Get properties."""
        element = self.tree.xpath('//*[@id="showcase-sidebar"]/div/div[1]//dl')[0]
        childs = element.getchildren()
        result = {}

        for name, value in (childs[i:i+2] for i in range(0, len(childs), 2)):
            name = name.text.lower()

            if name == 'uploader':
                user, stamp = value.getchildren()
                result['user'] = user.text
                result['added'] = stamp.attrib.get('datetime')
            elif name == 'favorites':
                childs = value.getchildren()

                if childs:
                    value = childs[0]

                result[name] = value.text
            else:
                result[name] = value.text

        return result

    def get_image_url(self):
        """Get image url."""
        element = self.tree.xpath('//*[@id="wallpaper"]')[0]
        return 'http:{}'.format(element.attrib.get('src'))

    def get_url(self):
        """Get URL."""
        element = self.tree.xpath('//*[@id="wallpaper-short-url-copy"]')[0]
        return element.attrib.get('value')

    def get_info(self):
        """Get info."""
        return {
            'url': self.get_url(),
            'image_url': self.get_image_url(),
            'source': self.get_source(),
            'resolution': self.get_resolution(),
            'colors': self.get_color_palette(),
            'tags': self.get_tags(),
            'purity': self.get_purity(),
            **self.get_properties(),
        }

    def json(self):
        """JSON."""
        return json.dumps(self.info)
