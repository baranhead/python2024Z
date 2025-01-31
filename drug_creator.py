import pandas as pd
from bs4 import BeautifulSoup
import random
import time

if __name__ == "__main__":
    random.seed(time.time_ns())
    SIMULATION_SIZE = 1

    #extracting the database
    path = 'drugbank_partial.xml'
    with open(path, 'r') as file:
        data = file.read()
        soup = BeautifulSoup(data, 'xml')

    #extracting tags and deleting Drugbank ID
    tags = [tag.name for tag in soup.find('drugbank').find('drug').find_all(recursive=False)[3:]]
    drug_list = soup.find('drugbank').find_all('drug', recursive=False)


    print(f'Generating {SIMULATION_SIZE} drugs.')

    #creating SIMULATION_SIZE drugs
    for number in range(109, SIMULATION_SIZE+109):

        rand = random.randint(0, 99)
        new_drug = soup.new_tag('drug', type=drug_list[rand]['type'])
        drugbank_id = soup.new_tag('drugbank-id', primary="true")

        zeros = '0' * (5-len(str(number)))
        drugbank_id.append(f'DB{zeros}{number}')
        new_drug.append(drugbank_id)

        for tag in tags:
            rand = random.randint(0, 99)
            existing_content = drug_list[rand].find(tag, recursive=False)

            if existing_content is not None:
                new_tag = BeautifulSoup(str(existing_content), "xml").find(tag)
            else:
                new_tag = soup.new_tag(tag)

            new_drug.append(new_tag)

        soup.find('drugbank').append(new_drug)

    with open("drugbank_partial_and_generated.xml", "w", encoding="utf-8") as file:
        file.write(soup.prettify())  


