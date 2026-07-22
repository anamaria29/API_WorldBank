import requests

BASE_URL = "https://api.worldbank.org/v2"

INDICATORS = {
    "population": "SP.POP.TOTL",
    "gdp": "NY.GDP.MKTP.CD",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "life_expectancy": "SP.DYN.LE00.IN"
}

def get_countries():
    """
    Obtiene únicamente países.
    """

    url = f"{BASE_URL}/country?format=json&per_page=300"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()[1]

    countries = []

    for country in data:

        if country["region"]["value"] != "Aggregates":

            countries.append({
                "id": country["id"],
                "name": country["name"]
            })

    countries.sort(key=lambda c: c["name"])

    return countries

def get_indicator(country_code, indicator_code):
    """
    Obtiene el último valor disponible para un indicador.
    """

    url = (
        f"{BASE_URL}/country/{country_code}/indicator/"
        f"{indicator_code}?format=json&per_page=100"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if len(data) < 2:
        return None

    for record in data[1]:

        if record["value"] is not None:

            return {
                "year": record["date"],
                "value": record["value"]
            }

    return None

def get_country_summary(country_code):
    """
    Obtiene un resumen de indicadores para un país.
    """

    country_info = requests.get(
        f"{BASE_URL}/country/{country_code}?format=json"
    ).json()[1][0]

    summary = {
        "country": country_info["name"]
    }

    for name, indicator in INDICATORS.items():

        summary[name] = get_indicator(country_code, indicator)

    return summary