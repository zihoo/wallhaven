"""User profile."""

import json
from lxml import html


class User:
    """User profile."""

    def __init__(self, content):
        """Init."""
        self.tree = html.fromstring(content)
        self.info = self.get_info()

        for key, value in self.info.items():
            setattr(self, key, value)

    def get_username(self):
        """Username."""
        return self.tree.xpath('//*[@id="user"]/h1/a')[0].text

    def get_group(self):
        """Group."""
        return self.tree.xpath('//*[@id="user"]/h4')[0].text

    def get_profile_info(self):
        """Get profile info."""
        element = self.tree.xpath('//*[@id="profile-content"]/div[2]/div[1]')[0]
        dls = element.find_class('datalist')
        dl = dls[0].getchildren() + dls[1].getchildren()

        result = {}
        for param, value in (dl[i:i+2] for i in range(0, len(dl), 2)):
            name = param.text.replace(' ', '_').lower()
            childs = value.getchildren()

            if childs:
                stamp = childs[0].attrib.get('datetime')
                result[name] = stamp
            else:
                result[name] = value.text

        return result

    def get_info(self):
        """Get info."""
        return {
            'username': self.get_username(),
            'group': self.get_group(),
            **self.get_profile_info()
        }

    def json(self):
        """JSON."""
        return json.dumps(self.info)
