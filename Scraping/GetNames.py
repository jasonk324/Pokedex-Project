import requests
from bs4 import BeautifulSoup
from lxml import etree

class Pokemon:
    def __init__(self, pokedex_id="", name="", type="", top_image="", abilities=[], hidden_abilities="", gender_ratio="", evolution=[], generation_introducted="", catch_rate="", egg_group="", height="", weight="", EV_yield="", stats=[], generation_entries=[]):
        self.pokedex_id= pokedex_id
        self.name = name
        self.type = type
        self.top_image = top_image
        self.abilities = abilities
        self.hidden_abilities = hidden_abilities
        self.gender_ratio = gender_ratio
        self.evolution = evolution
        self.generation_introduced = generation_introducted
        self.catch_rate = catch_rate 
        self.egg_group = egg_group
        self.height = height
        self.weight = weight
        self.EV_yield = EV_yield
        self.stats = stats 
        self.generation_entries = generation_entries

    def __str__(self):
        return f"{self.pokedex_id} | {self.name}"

def get_types(pokemon):

    def multiple_types(parent_b):

        table_main = parent_b.find_next_sibling('table')
        tables = table_main.find_all('table')
            
        for table in tables:

            small = table.find_next_sibling('small')

            if small.text == "Charizard":
                links = table.find_all('a')

                for link in links:
                    if link.text != "Unknown":
                        print(link.text)

    response = requests.get(BASE_SEARCH_URL + pokemon.name)
    soup = BeautifulSoup(response.content, "html.parser")

    title_element = soup.find('a', title='Type')
    parent_b = title_element.find_parent('b')

    if parent_b:
        table = parent_b.find_next_sibling('table')

        if table:
            links = table.find_all('a')

            for link in links:
                if link.text != "Unknown":
                    print(link.text)
                    pokemon.abilities.append(link.text)
        else:
            multiple_types(parent_b)

    print(pokemon.name)
    print(pokemon.type)


# Looking to get all the pokemon names from this link
NAMES_URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"

# Insert these names into a base URL to collect the rest of the data
BASE_SEARCH_URL = "https://bulbapedia.bulbagarden.net/wiki/"


response = requests.get(NAMES_URL)
soup = BeautifulSoup(response.content, "html.parser")

# Starting a list to hold all the pokemon data
pokedex_data = list()

# Look for all tbody elements
tbody_elements = soup.find_all("tbody")

# Noticed that we need 9 generations and the first tbody is referring to a different box of information
for i in range(1, 10):

    # print("----" * 20)
    # print(tbody_elements[i])

    # Finding all the rows in the tbody
    tr_elements = tbody_elements[i].find_all("tr")

    # Looping through all the rows
    for tr in tr_elements:
        td_elements = tr.find_all("td")

        if len(td_elements) != 0:
            # print(td_elements[0])
            # Result:
            # <td rowspan="1" style="font-family:monospace,monospace">#0001</td>

            # print(td_elements[2])
            # Result: 
            # <td><a href="/wiki/Bulbasaur_(Pok%C3%A9mon)" title="Bulbasaur (Pokémon)">Bulbasaur</a><br/><small></small></td>

            pokemon_id = td_elements[0].text
            pokemon_name = td_elements[2].text

            if (pokemon_id != "") & (pokemon_name != ""):
                pokedex_data.append(Pokemon(pokedex_id=pokemon_id, name=pokemon_name))

for pokemon in pokedex_data:
    get_types(pokemon)