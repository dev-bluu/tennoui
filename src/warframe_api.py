from requests import request


class NonPlatformError(Exception):
    pass


def catch_status_code(f):
    def func(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()
    return func


class WarframeAPI:

    _platforms = ['pc', 'ps4', 'xb1', 'swi']

    def __init__(self, platform: str, session: request, language: str = 'en'):
        if platform not in self._platforms:
            raise NonPlatformError(platform)
        self.platform = platform
        self.language = language
        self.api = 'https://api.warframestat.us/{platform}'.format(platform=self.platform)
        self.session = session

    @catch_status_code
    def worldstate(self):
        response = self.session.get(self.api)
        return response

    @catch_status_code
    def alerts(self):
        response = self.session.get(self.api + "/alerts")
        return response

    @catch_status_code
    def arbitration(self):
        response = self.session.get(self.api + "/arbitration")
        return response

    @catch_status_code
    def cambion_status(self):
        response = self.session.get(self.api + "/cambionCycle")
        return response

    @catch_status_code
    def cetus_status(self):
        response = self.session.get(self.api + "/cetusCycle")
        return response

    @catch_status_code
    def conclave_challenges(self):
        response = self.session.get(self.api + "/cetusCycle")
        return response

    @catch_status_code
    def construction_progress(self):
        response = self.session.get(self.api + "/constructionProgress")
        return response

    @catch_status_code
    def darvo_deal(self):
        response = self.session.get(self.api + "/dailyDeals")
        return response

    @catch_status_code
    def earth_cycle(self):
        response = self.session.get(self.api + "/earthCycle")
        return response

    @catch_status_code
    def ongoing_events(self):
        response = self.session.get(self.api + "/events")
        return response

    @catch_status_code
    def fissures(self):
        response = self.session.get(self.api + "/fissures")
        return response

    @catch_status_code
    def darvo_flash_sale(self):
        response = self.session.get(self.api + "/flashSales")
        return response

    @catch_status_code
    def global_upgrades(self):
        response = self.session.get(self.api + "/globalUpgrades")
        return response

    @catch_status_code
    def invasions(self):
        response = self.session.get(self.api + "/invasions")
        return response

    @catch_status_code
    def kuva_nodes(self):
        response = self.session.get(self.api + "/kuva")
        return response

    @catch_status_code
    def news(self):
        response = self.session.get(self.api + "/news")
        return response

    @catch_status_code
    def nightwave(self):
        response = self.session.get(self.api + "/nightwave")
        return response

    @catch_status_code
    def persistent_enemy_data(self):
        response = self.session.get(self.api + "/persistentEnemies")
        return response

    @catch_status_code
    def riven_stats(self, query: str = None):
        if query:
            response = self.session.get(self.api + "/rivens/search/{query}".format(query=query))
        else:
            response = self.session.get(self.api + "/rivens")
        return response

    @catch_status_code
    def sentient_outpost(self):
        response = self.session.get(self.api + "/sentientOutposts")
        return response

    @catch_status_code
    def sanctuary_status(self):
        response = self.session.get(self.api + "/simaris")
        return response

    @catch_status_code
    def sortie(self):
        response = self.session.get(self.api + "/sortie")
        return response

    @catch_status_code
    def syndicate_nodes(self):
        response = self.session.get(self.api + "/syndicateMissions")
        return response

    @catch_status_code
    def worldstate_timestamp(self):
        response = self.session.get(self.api + "/timestamp")
        return response

    @catch_status_code
    def vallis_status(self):
        response = self.session.get(self.api + "/vallisCycle")
        return response

    @catch_status_code
    def void_trader(self):
        response = self.session.get(self.api + "/voidTrader")
        return response
