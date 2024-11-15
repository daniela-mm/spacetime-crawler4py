from scraper import *
from Tokernizer import *
'''
    Grab all of the text from the valid urls. 
'''
unique_urls = dict()
subdomains = dict()
avoid_urls = set()
max_tot = ['', 0]

'''
def tokenizer():
  Insert definition for tokenizer 
    pass
'''

def insert_avoid(avoid):
    avoid_urls.add(avoid)

def uci_subdomain(sub_url):
    if (sub_url not in subdomains):
        #Append the subdomains to the url. 
        try: 
            subdomains[sub_url]
        except:
            subdomains[sub_url] = 1


def insert_unique(parsed):
    flag = False
    parsed._replace(fragment='').geturl()
    #Insert into the dictionary
    try:
        #Return True if the url is already in the dict. 
        unique_urls[parsed]
        flag = True
    except:
        #Return False if the url is NOT in the dict.
        unique_urls[parsed] = 1
        #Check if it is a unique page for the uci.edu subdomain
        try:
            subdomains[parsed.netloc.lower()] += 1
            if (subdomains[parsed.netloc.lower()] >= max_tot[1]):
                max_tot[0] = parsed.netloc.lower()
                max_tot[1] = subdomains[parsed.netloc.lower()] 
        except:
            pass
    return flag

def store_unique_urls_and_lengths():
    ''' Store unique URLs and their total lengths in a file. '''
    with open("unique_urls.txt", 'w', encoding='utf-8') as file:
        file.write(f"Unique URLS, {len(unique_urls)}\n")
        file.write(f"ICS Subdomains, {len(subdomains)}\n")
        file.write(f"Highest subdomain count: {max_tot}\n")
        file.write(f"Subdomain Dictionary:  {subdomains}\n")
        file.write(f"URLS to come back to: {len(avoid_urls)}\n")
        file.write(f"Top 50 common words: {top_fifty}\n")
        file.write(f"Longest File: {highest_count[0]}\n")
    
    print(f"Total unique URLs: {len(unique_urls)}, Subdomain: {len(subdomains)}")

# Example usage after the crawl
#store_unique_urls_and_lengths('unique_urls.txt')
