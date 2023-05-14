from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.edge.options import Options

from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
import random

# Download the Gutenberg corpus if not already downloaded
# nltk.download('gutenberg')
# nltk.download('punkt')

# Load a corpus (in this case, we'll use the Gutenberg corpus)
corpus = gutenberg.raw()

# Tokenize the corpus into sentences
sentences = sent_tokenize(corpus)

def generate_random_sentence():
    # Choose a random sentence from the corpus

    random_sentence = random.choice(sentences)
    return str(random_sentence).capitalize().strip().replace('\n', ' ').replace('\r', ' ')

def run_script():
    
    profile_path = '/home/sujeet/.config/microsoft-edge/Default-Test-Profile'

    edge_options = Options()

    # Set the browser to retain cookies and session information
    # edge_options.add_argument(f"user-data-dir={profile_path}")
    edge_options.add_argument(f"--user-data-dir={profile_path}")

    driver = webdriver.Edge(options=edge_options)
    driver.get('https://bing.com')

    element = driver.find_element(By.ID, 'sb_form_q')

    element.send_keys(generate_random_sentence())
    element.submit()

    time.sleep(5)
    driver.quit()

if __name__ == '__main__':

    for i in range(30):
        print(f"Running script {i+1} times")
        run_script()