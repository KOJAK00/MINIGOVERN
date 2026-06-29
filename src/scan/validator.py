import httpx
from src.config import Config
REST_COUNTRIES_URL = 'https://countries.dev/countries'

async def validate_countries(values: list[str]) -> float:

    if not values:
        return 0

    try:

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(REST_COUNTRIES_URL,)
            response.raise_for_status()
            countries = response.json()
            valid_names = set()
            for country in countries:
                valid_names.add(country["name"].lower())

                if country.get("nativeName"):
                    valid_names.add(country["nativeName"].lower())
            valid = 0
            for value in values:
                if str(value).lower() in valid_names:
                    valid += 1
            return round(valid / len(values), 2)

    except Exception as e:
        print(e)
        return 0