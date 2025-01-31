import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import networkx as nx
import matplotlib.pyplot as plt
import sys
import pandas as pd
import uvicorn
import random
import time
from fastapi import FastAPI, HTTPException
import os

#function drawing a synonym graph
def draw_synonym_graph(given_id, df_synonyms):
    row = df_synonyms.loc[df_synonyms['Drugbank ID'] == given_id]

    if row.empty:
        print(f"No data found for DrugBank ID: {given_id}")
        return
    
    synonyms = row['Synonyms'].values[0]

    G = nx.Graph()
    G.add_node(given_id, color='red', size=5000)

    for synonym in synonyms:
        G.add_node(synonym, color='lightblue', size=2000)
        G.add_edge(given_id, synonym)

    node_colors = [G.nodes[node].get('color', 'black') for node in G.nodes]
    node_sizes = [G.nodes[node].get('size', 3000) for node in G.nodes]

    pos = {}
    pos[given_id] = (0, 0)
    num_synonyms = len(synonyms)
    radius = 1.5

    for i, synonym in enumerate(synonyms):
        angle = 2 * math.pi * i / num_synonyms
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pos[synonym] = (x, y)

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=node_colors,
        node_size=node_sizes
    )
    nx.draw_networkx_edges(G, pos, edge_color='gray')

    for node, (x, y) in pos.items():
        font_size = 10
        plt.text(
            x, y, node,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=font_size,
            bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3')
        )

    plt.title(f"Graph of Synonyms for: {given_id}")
    plt.axis('off')
    plt.show()

#function drawing a bipartite graph
def draw_pathway_graph(df_interactions):
    G = nx.Graph()  
    for _, row in df_interactions.iterrows():
        pathway = row['Pathway']
        drugs = row['Interactions'] 

        G.add_node(pathway, bipartite=0)    

        for drug in drugs:
            G.add_node(drug, bipartite=1)
            G.add_edge(pathway, drug)   

    pos = nx.drawing.layout.bipartite_layout(G, nodes=[n for n, d in G.nodes(data=True) if d['bipartite'] == 0])    

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=['lightblue' if d['bipartite'] == 0 else 'lightgreen' for n, d in G.nodes(data=True)],
        node_size=1000,
        edge_color='gray'
    )   

    plt.title("Bipartite Graph of Pathways and Drug Interactions")
    plt.show()

#function drawing a histogram of interactions
def draw_hist_interactions(drug_pathway_hist_dict, names):

    #printing the drug_pathwat_hist_dict
    #print(drug_pathway_hist_dict)

    drugs = [key[names] for key in drug_pathway_hist_dict.keys()]
    values = drug_pathway_hist_dict.values()

    plt.figure(figsize=(10, 10))
    plt.bar(drugs, values, color='blue')
    plt.xlabel('Drug')
    plt.ylabel('Pathway interactions count')
    plt.title('Histogram of interactions')
    plt.xticks(rotation=90, ha='right')
    plt.show()

#function drawing a pie chart for cellular location
def draw_cellular_location_pie_chart(cellular_location_dict):
    proteins = list(cellular_location_dict.keys())
    values = list(cellular_location_dict.values())

    plt.figure(figsize=(10, 10))
    plt.title('Pie chart of protein targets cellular locations')
    
    colors, _ = plt.pie(values, labels=None)

    total = sum(values)
    percentages = [f"{(value / total) * 100:.2f}%" for value in values]
    legend_labels = [f"{protein} ({percentage})" for protein, percentage in zip(proteins, percentages)]

    plt.legend(colors, legend_labels, title="Cellular Locations", loc="center left", bbox_to_anchor=(0.9, 0.5))
    plt.show()

#function drawing a pie chart for certain groups of drugs
def draw_group_pie_chart(approved_cnt, withdrawn_cnt, experimental_cnt, vet_approved_cnt):
    plt.figure(figsize=(10, 10))

    values = [approved_cnt, withdrawn_cnt, experimental_cnt, vet_approved_cnt]
    plt.title('Pie chart of the number of drugs in a certain group')
    
    colors, _, _  = plt.pie(values, labels=None, autopct='%1.1f%%')

    legend_labels = [f'approved: {approved_cnt}', f'withdrawn: {withdrawn_cnt}', f'experimental/investigational: {experimental_cnt}', f'vet approved: {vet_approved_cnt}']

    plt.legend(colors, legend_labels, title="Groups of drugs", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.show()

#function used to get a number of pathway interactions from API
def get_pathway_interactions_from_api(drug_pathway_hist_dict):
    app = FastAPI()

    @app.post("/pathway_interactions/")
    async def pathway_interactions(request: dict):

        drugbank_id = request.get("Drugbank ID")

        if not drugbank_id:
            raise HTTPException(status_code=400, detail="Missing 'Drugbank ID'")

        if drugbank_id not in drug_pathway_hist_dict:
            raise HTTPException(status_code=404, detail="Drugbank ID not found")

        return drug_pathway_hist_dict[drugbank_id]

    '''
    {
    "Drugbank ID": "DB00001"
    }
    http://127.0.0.1:8000/docs
    '''
    uvicorn.run(app)

#function analyzing a single gene
def analyze_gene(drug):
    coding_gene = drug.find('polypeptide')
    if coding_gene == None:
        print('The chosen drug does not contain a polypeptide')
        return
    
    gene_name = drug.find('gene-name').text.strip()
    print(f"Analyzing {gene_name} gene.")

    drug_interactions_content = drug.find('drug-interactions')
    df_interactions = pd.DataFrame({
        'Drugbank ID': [],
        'Name': [],
        'Description': []

    })

    if drug_interactions_content != None:
        drug_interactions_list = drug_interactions_content.find_all('drug-interaction')

        for inter in drug_interactions_list:
            drugbank_id = inter.find('drugbank-id').text.strip()
            name = inter.find('name').text.strip()
            description = inter.find('description').text.strip()

            df_interactions.loc[len(df_interactions)] = {'Drugbank ID': drugbank_id, 'Name': name, 'Description': description}

        print(f"This gene interacts with {len(drug_interactions_list)} drugs")
        print(df_interactions)
        df_interactions.to_csv('lmao.csv', index=False)
    else:
        print(f"{drug} gene does not interact with any drugs")

    drug_products_content = drug.find('products')
    country_dict = {}
    labeller_dict = {}
    if drug_products_content != None:
        drug_products_list = drug_products_content.find_all('product')

        for prod in drug_products_list:
            country = prod.find('country').text.strip()
            labeller = prod.find('labeller').text.strip()

            if country not in country_dict:
                country_dict[country] = 1
            else:
                country_dict[country] += 1

            if labeller not in labeller_dict:
                labeller_dict[labeller] = 1
            else:
                labeller_dict[labeller] += 1

        plt.figure(figsize=(10, 10))

        plt.subplot(1, 2, 1)
        values = labeller_dict.values()
        legend_labels = labeller_dict.keys()
        plt.title(f'Pie chart of product labellers for {gene_name} gene')
        colors, _, _  = plt.pie(values, labels=None, autopct='%1.1f%%')
        plt.legend(colors, legend_labels, title="Product labeller names", loc="upper left", bbox_to_anchor=(-0.35, 1.22))


        plt.subplot(1, 2, 2)
        countries = country_dict.keys()
        values = country_dict.values()
        plt.bar(countries, values, color='blue')
        plt.xlabel('Country')
        plt.ylabel('Number of products')
        plt.title(f'Histogram of number of products containing {gene_name} gene by country')
        plt.xticks(rotation=45, ha='right')

        plt.show()

    else:
        print(f"{gene_name} is not contained in any products")

#function creating the df_info dataframe
def create_df_info(drug_list):
    drugbank_id_list = []
    drug_name_list = []
    type_list = []
    description_list = []
    state_list = []
    indication_list = []
    mechanism_list = []
    food_interactions_list = []


    for drug in drug_list:
        drugbank_id_list.append(drug.find('drugbank-id', attrs={'primary': 'true'}).text.strip())
        drug_name_list.append(drug.find('name').text.strip())
        type_list.append(drug['type'])
        description_list.append(drug.find('description').text.strip())
        state_list.append(drug.find('state').text.strip())
        indication_list.append(drug.find('indication').text.strip())
        mechanism_list.append(drug.find('mechanism-of-action').text.strip())

        temp_list = [interaction.text for interaction in drug.find('food-interactions').find_all('food-interaction')]
        if len(temp_list) > 0:
            food_interactions_list.append(temp_list)
        else:
            food_interactions_list.append(None)

    df_info = pd.DataFrame({
        'Drugbank ID': drugbank_id_list,
        'Name': drug_name_list,
        'Type': type_list,
        'Description': description_list,
        'State': state_list,
        'Indication': indication_list,
        'Mechanism': mechanism_list,
        'Food interactions': food_interactions_list,
    })

    #printing the first dataframe df_info
    #print(df_info)
    
    return df_info, drugbank_id_list, drug_name_list

#function creating the df_synonyms graph and drawing a graph for a given Drugbank ID
def create_df_synonyms_draw_graph(drug_list, drugbank_id_list, GIVEN_ID):
    synonyms_list = []
    for drug in drug_list:
        synonyms_text = drug.find('synonyms')
        if synonyms_text == None:
            continue

        all_synonyms_list = synonyms_text.find_all('synonym')
        if len(all_synonyms_list) == 0:
            continue

        synonyms = [synonym.text.strip() for synonym in all_synonyms_list]
        synonyms_list.append(synonyms)

    df_synonyms = pd.DataFrame({
        'Drugbank ID': drugbank_id_list,
        'Synonyms': synonyms_list
    })

    #drawing a graph for a given Drugbank ID
    draw_synonym_graph(GIVEN_ID, df_synonyms)

#function creating the df_products dataframe
def create_df_products(drug_list, drugbank_id_list):
    product_name_list = []
    drugbank_id_product_list = []
    labeller_list = []
    ndc_code_list = []
    dosage_form_list = []
    route_list = []
    strength_list = []
    country_list = []
    source_list = []

    for drug, drugbank_id in zip(drug_list, drugbank_id_list):
        products_text = drug.find('products')

        if products_text == None:
            continue

        products_list = products_text.find_all('product')

        if len(products_list) == 0:
            continue
        
        for product in products_list:
            drugbank_id_product_list.append(drugbank_id)
            product_name_list.append(product.find('name').text.strip())
            labeller_list.append(product.find('labeller').text.strip())
            country = product.find('country').text.strip()
            country_list.append(country)

            if country == 'US':
                ndc_code_list.append(product.find('ndc-product-code').text.strip())
            else:
                ndc_code_list.append('No information')

            dosage_form_list.append(product.find('dosage-form').text.strip())
            route_list.append(product.find('route').text.strip())
            strength_list.append(product.find('strength').text.strip())
            source_list.append(product.find('source').text.strip())

    df_products = pd.DataFrame({
        'Drugbank ID': drugbank_id_product_list,
        'Name': product_name_list,
        'Labeller': labeller_list,
        'National Drug Code': ndc_code_list,
        'Dosage form': dosage_form_list,
        'Route': route_list,
        'Strength': strength_list,
        'Country': country_list,
    })

    #printing the df_products dataframe
    #print(df_products)
    return df_products

#function creating the df_pathways dataframe
def create_df_pathways(drug_list, drug_name_list, drugbank_id_list):
    drugbank_id_pathway_list = []
    pathway_name_list = []
    pathway_interactions_list = []
    drug_pathway_hist_dict = {}
    for drug_text, drug_name, drugbank_id in zip(drug_list, drug_name_list, drugbank_id_list):

        if drug_name not in drug_pathway_hist_dict:
            drug_pathway_hist_dict[(drugbank_id, drug_name)] = 0

        pathways_text = drug_text.find('pathways')

        if pathways_text == None:
            continue

        pathways_list =  pathways_text.find_all('pathway')

        for pathway in pathways_list:
            pathway_name_list.append(pathway.find('name').text.strip())
            drugs = pathway.find('drugs').find_all('drug')
            interactions = []

            for drug in drugs:
                temp = (drug.find('drugbank-id').text.strip(), drug.find('name').text.strip())
                interactions.append(temp)

                if temp in drug_pathway_hist_dict:
                    drug_pathway_hist_dict[temp] += 1
                
            pathway_interactions_list.append(interactions)
        
        if len(pathways_list):
            drugbank_id_pathway_list.append(drugbank_id)

    df_pathways = pd.DataFrame({
        'Drugbank ID': drugbank_id_pathway_list,
        'Pathway': pathway_name_list,
    })

    #printing the df_pathways dataframe
    print(f"The total number of all the pathways is {df_pathways['Pathway'].size}.\n")
    print(df_pathways)

    return pathway_name_list, pathway_interactions_list, drug_pathway_hist_dict

#function creating the df_interactions dataframe and drawing a graph
def create_df_interactions_draw_graph(pathway_name_list, pathway_interactions_list):
    df_interactions = pd.DataFrame({
        'Pathway': pathway_name_list,
        'Interactions': pathway_interactions_list,
    })

    #printing the df_interactions dataframe
    #print(df_interactions)

    draw_pathway_graph(df_interactions)

#function creating the df_targets dataframe
def create_df_targets (drug_list):
    target_drugbank_id_list = []
    target_source_list = []
    target_external_id_list = []
    target_polypeptide_name_list = []
    target_coding_gene_name_list = []
    target_coding_gene_id_list = []
    target_chromosome_number_list = []
    target_cellular_location_list = []

    cellular_location_dict = {}

    for drug_text in drug_list:
        targets_text = drug_text.find('targets', recursive=False)

        if targets_text == None:
            continue

        target_list = targets_text.find_all('target')

        if len(target_list) == 0:
            continue

        for target_text in target_list:
            polypeptide_text = target_text.find('polypeptide', attrs={'id': True, 'source': True})
            if polypeptide_text != None:
                target_drugbank_id_list.append(target_text.find('id').text.strip())
                target_source_list.append(polypeptide_text.get('source'))
                target_external_id_list.append(polypeptide_text.get('id'))
                target_polypeptide_name_list.append(polypeptide_text.find('name').text.strip())
                target_coding_gene_name_list.append(polypeptide_text.find('gene-name').text.strip())
                target_chromosome_number_list.append(polypeptide_text.find('chromosome-location').text.strip())

                temp = polypeptide_text.find('cellular-location').text
                if temp == '':
                    target_cellular_location_list.append(None)
                    if 'No information' not in cellular_location_dict:
                        cellular_location_dict['No information'] = 1
                    else:
                        cellular_location_dict['No information'] += 1
                else:
                    target_cellular_location_list.append(temp)
                    if temp not in cellular_location_dict:
                        cellular_location_dict[temp] = 1
                    else:
                        cellular_location_dict[temp] += 1

                ex_indentifiers = polypeptide_text.find('external-identifiers').find_all('external-identifier')
                ga_id = None
                for ex in ex_indentifiers:
                    if ex.find('resource').text == 'GenAtlas':
                        ga_id = ex.find('identifier').text
                target_coding_gene_id_list.append(ga_id)

    df_targets = pd.DataFrame({
        "Target Drugbank ID": target_drugbank_id_list,
        "External source": target_source_list,
        "Target external ID": target_external_id_list,
        "Polypeptide": target_polypeptide_name_list,
        "Coding gene": target_coding_gene_name_list,
        "Coding gene ID":  target_coding_gene_id_list,
        "Chromosome number": target_chromosome_number_list,
        "Cellular location": target_cellular_location_list,
    })

    #printing protein targets dataframe
    #print(df_targets)
    return cellular_location_dict

def create_df_group_draw_chart(drug_list):
    approved_cnt = 0
    withdrawn_cnt = 0
    experimental_cnt = 0
    vet_approved_cnt = 0
    app_not_wit_cnt = 0

    for drug in drug_list:
        groups_text = drug.find('groups')
        app = 0
        wit = 0

        if groups_text != None:
            groups = groups_text.find_all('group')

            if len(groups) == 0:
                continue

            for group in groups:
                group_name = group.text.strip()
                if group_name == 'approved':
                    approved_cnt += 1
                    app = 1
                elif group_name == 'withdrawn':
                    withdrawn_cnt += 1
                    wit = 1
                elif group_name == 'experimental' or group_name == 'investigational':
                    experimental_cnt += 1
                elif group_name == 'vet_approved':
                    vet_approved_cnt += 1

            if app == 1 and wit == 0:
                app_not_wit_cnt += 1

    df_group = pd.DataFrame({
        'Approved': [approved_cnt],
        'Withdrawn': [withdrawn_cnt],
        'Experimental': [experimental_cnt],
        'Vet approved': [vet_approved_cnt],
    })

    #printing the df_group dataframe
    #print(df_group)

    draw_group_pie_chart(approved_cnt, withdrawn_cnt, experimental_cnt, vet_approved_cnt)
    print(f"The number of approved, but not withrdawn drugs is: {app_not_wit_cnt}")

#function creating drug interactions dataframe
def create_drug_interactions_df(drug_list):
    interactions_drugbank_list = []
    interactions_description_list = []
    interactions_id_list = []
    interactions_name_list = []

    for i, drug in enumerate(drug_list, 0):
        interactions_text = drug.find('drug-interactions')

        if interactions_text != None:
            interactions_list = interactions_text.find_all('drug-interaction')
            if len(interactions_list) == 0:
                continue
            for interaction in interactions_list:
                interactions_drugbank_list.append(drugbank_id_list[i])
                interactions_id_list.append(interaction.find('drugbank-id').text.strip())
                interactions_name_list.append(interaction.find('name').text.strip())
                interactions_description_list.append(interaction.find('description').text.strip())
                


    drug_interactions_df = pd.DataFrame({
        'Drugbank ID': interactions_drugbank_list,
        'Interacting drug ID': interactions_id_list,
        'Interacting drug name': interactions_name_list,
        'Interaction description': interactions_description_list
    })

    #printing the drug interactions dataframe
    #print(drug_interactions_df)

def extract_drugs(PATH, NAMES):
    if PATH == 'drugbank_partial_and_generated.xml':
        NAMES = 0

    if os.path.exists(PATH):
        with open(PATH, 'r') as file:
            data = file.read()
            soup = BeautifulSoup(data, 'xml')
    else:
        print("XML file not found")
        return None
    
    
    drug_text = soup.find('drugbank')
    if (drug_text == None):
        return None
    else:
        return drug_text.find_all('drug', recursive=False)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    #extracting data
    PATH = 'drugbank_partial.xml'
    NAMES = 1
    drug_list = extract_drugs(PATH, NAMES)

    #task 1
    #NOTE: needed for the other tasks
    df_info, drugbank_id_list, drug_name_list = create_df_info(drug_list)

    #task 2
    GIVEN_ID = 'DB00001'
    create_df_synonyms_draw_graph(drug_list, drugbank_id_list, GIVEN_ID)

    #task 3
    df_products = create_df_products(drug_list, drugbank_id_list)

    #task 4
    #NOTE: needed for tasks 5, 6, 15 
    pathway_name_list, pathway_interactions_list, drug_pathway_hist_dict = create_df_pathways(drug_list, drug_name_list, drugbank_id_list)

    #task 5
    create_df_interactions_draw_graph(pathway_name_list, pathway_interactions_list)

    #task 6
    draw_hist_interactions(drug_pathway_hist_dict, NAMES)

    #task 15
    get_pathway_interactions_from_api({key[0]: value for key, value in drug_pathway_hist_dict.items()})

    #task 7
    #NOTE: needed for task 8
    cellular_location_dict = create_df_targets(drug_list)

    #task 8
    draw_cellular_location_pie_chart(cellular_location_dict)

    #task 9
    create_df_group_draw_chart(drug_list)

    #task 10
    create_drug_interactions_df(drug_list)

    #task 11 - analyzing a single gene
    random.seed(time.time_ns())
    rand = random.randint(0, len(drug_list)-1)
    analyze_gene(drug_list[rand])