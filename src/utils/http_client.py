import aiohttp

from src.config import settings 


class HttpClient: 
    async def get_breeds_from_api(self) -> list[str]: 
        async with aiohttp.ClientSession() as session: 
            async with session.get(settings.BREED_API_URL) as req: 
                resp = await req.json()
                breeds = [] 
                for item in resp: 
                    breeds.append(item.get("name"))
                return breeds
