"""Search params."""


class ValueOrDefaultParameter:
    """Simple search parameter.
    Returns defined value or default value.
    """

    default = None

    def __init__(self, val):
        """Init."""
        self.value = self.default
        if val:
            self.value = val


class SelectOrDefaultParameter:
    """Select search parameter.
    Returns value from predefined list of choices or default value.
    """

    choices = ()
    default = None

    def __init__(self, val):
        """Init."""
        self.value = self.default
        if val and val in self.choices:
            self.value = val


class ListParameter:
    """List parameter.
    Returns list of items from list of choices as a string or None.
    """

    def __init__(self, vals):
        """Init."""
        value = None
        if vals:
            if all(val in self.choices for val in vals):
                value = ','.join(vals)
            else:
                raise ValueError

        self.value = value


class BinaryParameter:
    """
    Binary parameter. Returns binary sum of elements weights.
    """

    def get_binary(self, weights):
        """Get binary string."""
        return bin(sum(x[0] for x in weights if x[1]))[2:].zfill(3)


class Query(ValueOrDefaultParameter):
    """Search query."""

    name = 'q'
    default = None


class Categories(BinaryParameter):
    """Categories to include."""

    name = 'categories'

    def __init__(self, general=True, anime=True, people=True):
        """Init."""
        weights = ((4, general),
                   (2, anime),
                   (1, people))
        self.value = self.get_binary(weights)


class Purity(BinaryParameter):
    """Content purity."""

    name = 'purity'

    def __init__(self, sfw=True, sketchy=False, nsfw=False):
        """Init."""
        weights = ((4, sfw),
                   (2, sketchy),
                   (1, nsfw))
        self.value = self.get_binary(weights)


class Resolutions(ListParameter):
    """Wallpapers resolutions."""

    name = 'resolutions'
    choices = ('1024x768', '1280x800', '1366x768', '1280x960',
               '1440x900', '1600x900', '1280x1024', '1600x1200',
               '1680x1050', '1920x1080', '1920x1200', '2560x1440',
               '2560x1600', '3840x1080', '5760x1080', '3840x2160')


class Ratios(ListParameter):
    """Wallpapers ratios."""

    name = 'ratios'
    choices = ('4x3', '5x4', '16x9', '16x10', '21x9', '32x9', '48x9')


class Sorting(SelectOrDefaultParameter):
    """Sorting of result list."""

    name = 'sorting'
    choices = ('relevance', 'random', 'date_added', 'views', 'favorites')
    default = 'relevance'


class Order(SelectOrDefaultParameter):
    """Ordering of result list."""

    name = 'order'
    choices = ('asc', 'desc')
    default = 'desc'


class Page(ValueOrDefaultParameter):
    """Page number."""

    name = 'page'
    default = 1


def get_search_params(route, **kwargs):
    """Returns dict with search params according to the route."""
    if 'search' in route:
        params = (
            Query(kwargs.get('query')),
            Categories(**kwargs.get('categories', {})),
            Purity(**kwargs.get('purity', {})),
            Resolutions(kwargs.get('resolutions', [])),
            Ratios(kwargs.get('ratios', [])),
            Sorting(kwargs.get('sorting')),
            Order(kwargs.get('order')),
            Page(kwargs.get('page'))
        )
    elif 'user' in route:
        params = (
            Purity(**kwargs.get('purity', {})),
            Page(kwargs.get('page'))
        )

    return {p.name: p.value for p in params if p.value}
