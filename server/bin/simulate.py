

import requests
import os
import random
from starlette.config import environ


# set test config

environ["DB_NAME"] = "baking_db_test_int_" + \
    str(int(random.random() * 1000000))
environ["DB_CONN_STR"] = "mongodb://baking-mongo:CS8kyisdLwXjNxmL0OKLcA2vJGlJcPft9sPs8k1dUcaI2QCGo3nsme64snV5YSgThLDoTiNsjDnGACDbDWCrIA==@baking-mongo.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@baking-mongo@"

environ["DB_USER"] = "postgres"
environ["azure_storage_connection_string"] = ""

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()
# print (WORDS)
TOTAL_RECIPES = 50

# URL = "http://localhost:8888"
URL = "https://service.baking.reubinoff.com"

def get_types():
    from baking.routers.ingredients.enums import IngrediantType
    TYPES = list(map(str, IngrediantType))
    return TYPES

def get_words(num_of_words):
    return ' '.join([WORDS[random.randint(0, len(WORDS) - num_of_words)].decode() for i in range(num_of_words)])

def create_recipes():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    content = []
    with open(current_directory+'/test_a.jpeg', 'rb') as f:
        content.append(f.read())
    with open(current_directory+'/test_b.jpeg', 'rb') as f:
        content.append(f.read())

    files = [{'file': ("image.jpeg", content[0])},
             {'file': ("image.jpeg", content[1])}]
    for i in range(1, TOTAL_RECIPES):
        p = []
        for j in range(1, random.randint(2, 5)):
            ingredients = []
            for k in range(1, random.randint(2, 3)):
                type = get_types()[random.randint(0, len(get_types())-1)]
                ingredients.append( {
                    "name": f"i_{get_words(random.randint(1,3))}_{k}",
                    "quantity": random.randint(1, 1000),
                    "units": "Grams",
                    "type": type,
                })
            steps = []
            for k in range(1, random.randint(2, 3)):
                steps.append({
                    "name": f"step_{get_words(random.randint(1,3))}_{k}",
                    "description": get_words(random.randint(1, 90)),
                    "duration_in_seconds": random.randint(10, 10000),
                })
            p.append({
                "name": f"procedure_{i}_{j}",
                "description": get_words(random.randint(1, 10)),
                "order": j,
                "ingredients": ingredients,
                "steps": steps
                })
            
        aaa = {
            "name": get_words(2),
            "description": get_words(10),
            "procedures": p
        }
        
        t = requests.post(f"{URL}/recipe", json=aaa)
        print(t.status_code)


    t = requests.get(
        f"{URL}/recipe?page=1&itemsPerPage=199")

    ids = [t["id"] for t in t.json()["items"]]
    print(t.status_code)
    index = 0
    for i in ids:
        index+=1
        if index%3 == 0:
            continue
        t = requests.post(
            f"{URL}/recipe/{i}/img", files=files[random.randint(0, 1)])
        
        print(t.status_code)


def delete_all_recipes():
    t = requests.get(
        f"{URL}/recipe?page=1&itemsPerPage=199")

    ids = [t["id"] for t in t.json()["items"]]
    print(t.status_code)
    for i in ids:
        t = requests.delete(f"{URL}/recipe/{i}")
        print(t.status_code)
    print(t.status_code)

if __name__ == "__main__":
    delete_all_recipes()
    create_recipes()