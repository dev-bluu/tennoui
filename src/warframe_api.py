import asyncio
import aiohttp

WARFRAME_API = 'https://api.warframestat.us'

class NonPlatformError(Exception):
    pass



class WarframeAPI:

    _platforms = ['pc', 'ps4', 'xb1', 'swi']

    def __init__(self, platform: str, language: str = 'en', loop=None):
        if platform not in self._platforms:
            raise NonPlatformError(platform)
        self.platform = platform
        self.language = language
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(loop=self._loop)

    async def _fetch(self, url):
        async with self.session.get(url) as response:
            resp = await response.json()
            return resp


    async def worldstate(self):
        url = WARFRAME_API + "/{platform}".format(platform=self.platform)
        return await self._fetch(url)
        # response = self.session.get(self.api)
        # return response

    async def alerts(self):
        url = WARFRAME_API + "/{platform}/alerts".format(platform=self.platform)
        return await self._fetch(url)

    async def arbitration(self):
        url = WARFRAME_API + "/{platform}/arbitration".format(platform=self.platform)
        return await self._fetch(url)

    async def cambion_status(self):
        url = WARFRAME_API + "/{platform}/cambionCycle".format(platform=self.platform)
        return await self._fetch(url)

    async def cetus_status(self):
        url = WARFRAME_API + "/{platform}/cetusCycle".format(platform=self.platform)
        return await self._fetch(url)

    async def conclave_challenges(self, query: str = None):
        url = WARFRAME_API + "/{platform}/conclaveChallenges".format(platform=self.platform)
        return await self._fetch(url)

    async def construction_progress(self):
        url = WARFRAME_API + "/{platform}/constructionProgress".format(platform=self.platform)
        return await self._fetch(url)

    async def darvo_deal(self):
        url = WARFRAME_API + "/{platform}/dailyDeals".format(platform=self.platform)
        return await self._fetch(url)

    async def earth_cycle(self):
        url = WARFRAME_API + "/{platform}/earthCycle".format(platform=self.platform)
        return await self._fetch(url)

    async def ongoing_events(self):
        url = WARFRAME_API + "/{platform}/events".format(platform=self.platform)
        return await self._fetch(url)

    async def fissures(self):
        url = WARFRAME_API + "/{platform}/fissures".format(platform=self.platform)
        return await self._fetch(url)

    
    async def darvo_flash_sale(self):
        url = WARFRAME_API + "/{platform}/flashSales".format(platform=self.platform)
        return await self._fetch(url)

    async def global_upgrades(self):
        url = WARFRAME_API + "/{platform}/globalUpgrades".format(platform=self.platform)
        return await self._fetch(url)

    async def invasions(self):
        url = WARFRAME_API + "/{platform}/invasions".format(platform=self.platform)
        return await self._fetch(url)

    async def kuva_nodes(self):
        url = WARFRAME_API + "/{platform}/kuva".format(platform=self.platform)
        return await self._fetch(url)

    async def news(self):
        url = WARFRAME_API + "/{platform}/news".format(platform=self.platform)
        return await self._fetch(url)

    async def nightwave(self):
        url = WARFRAME_API + "/{platform}/nightwave".format(platform=self.platform)
        return await self._fetch(url)

    async def persistent_enemy_data(self):
        url = WARFRAME_API + "/{platform}/persistentEnemies".format(platform=self.platform)
        return await self._fetch(url)

    async def riven_stats(self, query: str = None):
        if query:
            url = WARFRAME_API + "/{platform}/rivens/search/{query}".format(platform=self.platform, query=query)
        else:
            url = WARFRAME_API + "/{platform}/rivens".format(platform=self.platform)
        return await self._fetch(url)

    async def sentient_outpost(self):
        url = WARFRAME_API + "/{platform}/sentientOutposts".format(platform=self.platform)
        return await self._fetch(url)

    async def sanctuary_status(self):
        url = WARFRAME_API + "/{platform}/simaris".format(platform=self.platform)
        return await self._fetch(url)

    async def sortie(self):
        url = WARFRAME_API + "/{platform}/sortie".format(platform=self.platform)
        return await self._fetch(url)

    async def syndicate_nodes(self):
        url = WARFRAME_API + "/{platform}/syndicateMissions".format(platform=self.platform)
        return await self._fetch(url)

    async def worldstate_timestamp(self):
        url = WARFRAME_API + "/{platform}/timestamp".format(platform=self.platform)
        return await self._fetch(url)

    async def vallis_status(self):
        url = WARFRAME_API + "/{platform}/vallisCycle".format(platform=self.platform)
        return await self._fetch(url)

    async def void_trader(self):
        url = WARFRAME_API + "/{platform}/voidTrader".format(platform=self.platform)
        return await self._fetch(url)
