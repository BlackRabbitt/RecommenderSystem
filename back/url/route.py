class Routes:
    routeTable = {}

    @staticmethod
    def get(url, path):
        Routes.routeTable[url] = path

    @staticmethod
    def checkUrl(url):
        try:
            if Routes.routeTable[url]:
                return Routes.routeTable[url]
        except KeyError:
            return url