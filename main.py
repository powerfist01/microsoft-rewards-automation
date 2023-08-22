import os
import json
import time
import random
from tqdm import tqdm
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from dotenv import dotenv_values
env_vars = dotenv_values('.env')

import functions.functions as functions

# Download the Gutenberg corpus if not already downloaded
# import nltk
# nltk.download('gutenberg')
# nltk.download('punkt')

def generate_profiles_from_env():

    email_profile_paths = {}
    for _, (key, value) in enumerate(env_vars.items()):
        email_profile_paths[key] = value

    return email_profile_paths

def generate_random_sentence():

    # Load a corpus (in this case, we'll use the Gutenberg corpus)
    corpus = gutenberg.raw()

    # Tokenize the corpus into sentences
    sentences = sent_tokenize(corpus)
    random_sentence = random.choice(sentences)
    return str(random_sentence)[4:].capitalize().strip().replace('\n', ' ').replace('\r', ' ')

def run_script(profile_path):
    
    edge_options = Options()

    # Set the browser to retain cookies and session information
    edge_options.add_argument(f"--user-data-dir={profile_path}")
    edge_options.add_argument('--headless')

    driver = webdriver.Edge(options=edge_options)
    driver.get('https://bing.com')

    element = driver.find_element(By.ID, 'sb_form_q')

    random_sentence = generate_random_sentence()
    element.send_keys(random_sentence)
    element.submit()

    time.sleep(1)
    driver.quit()

def is_done_for_the_day(email):

    todays_log = functions.get_search_count_by_email(email)
    if(not todays_log): 
        return {'done': False, 'search_count': 0}

    search_count = todays_log[3] or 0
    if(search_count >= 32): 
        return {'done': True}

    return {'done': False, 'search_count': search_count}

if __name__ == '__main__':
    
    print('Get ready! It"s going to be a bumpy ride!\n')

    MICROSOFT_PROFILE_PATHS = generate_profiles_from_env()

    for email, config_path in MICROSOFT_PROFILE_PATHS.items():

        is_done = is_done_for_the_day(email)
        if(is_done['done']): continue

        search_count = is_done['search_count']
        if(search_count == 0): 
            functions.insert_search_count(email, search_count)

        print('For profile: ', email, f'{32 - search_count}' + ' searches remaining')
        for i in tqdm(range(32 - search_count)):
            run_script(config_path)
            search_count += 1
            functions.update_search_count(email, search_count)

    print('\nAll done for the day!')
