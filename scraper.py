import re
from urllib.parse import urlparse, urldefrag, parse_qs
from bs4 import BeautifulSoup
from Content import *
from Analyze import *


def scraper(url, resp):
    '''
    #print("In scaper function.")
    store_unique_urls_and_lengths()
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]
    '''
    # Extract links from the response
    links = extract_next_links(url, resp)
    
    # Filter valid links and store unique URLs and their lengths
    valid_links = []
    for link in links:
        if is_valid(link):
            valid_links.append(link)
    store_unique_urls_and_lengths(link)  # Store unique link details
    return valid_links

def extract_next_links(url, resp):
    #print(f"Checking this link {url}")
    #DMM: Create an empty list to hold all the VALID urls in. 
    url_list = list()
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!

    #DMM:  Case 1: If raw-response if NOT empty (ie status code is 200): 
    if(resp.status == 200):
        try:
            print(f"The lenght of this response is {len(resp.raw_response.content)}")
            with open("response_length.txt", 'a', encoding='utf-8') as file:
                file.write(f"Length of {url}, {len(resp.raw_response.content)}\n")
            # Find all the links in the page
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            #Respect site's crawling policy. 
            soup_tags = soup.find("meta", attrs={"name": "robots"})
            if(soup_tags and soup_tags.get("content") == "noindex, nofollow"):
                insert_avoid(url)
                #Should return an empty list. 
                return url_list
            #STORE THE ORIGINAL TEXT
            textSoup = soup.get_text().lower()

            #REMOVE THE NAVIGATION BAR AND FOOTER OF THE SITES
            # Helps avoid pages with little addional info and helps gather more accurate data. 
            # Remove <nav> elements
            for nav in soup.find_all('nav'):
                nav.decompose()
            # Remove <footer> elements
            for footer in soup.find_all('footer'):
                footer.decompose()
            # Remove <div> elements with common navigation/footer classes
            for div in soup.find_all('div', class_=['navbar', 'footer', 'header', 'nav', 'site-footer', 'site-header']):
                div.decompose()
            pureSoup = soup.get_text().lower()

            print(f"COMPARING {textSoup == pureSoup}\n{textSoup}\n{pureSoup}")
            #Check if this page has any calendar-related traps. 
            if (check_calendar(pureSoup)):
                insert_avoid(url)
                return url_list
            #Check if this page is dead/low info
            print(f"searching {url} for dead content. \n")
            if (dead_site(pureSoup)):
                insert_avoid(url)
                #print(f"Dead/low content {url}\n")
                return url_list
            #If not a dead site, analyze the contents of the file:
            write_site(text, url)
            # Print out all the links found. 
            for link in soup.find_all('a'):
                #print(f"Found a link! {link.get('href')}")
                #Append the link to the list of links. 
                new_link = link.get('href')
                if((new_link not in unique_urls) and (new_link not in avoid_urls)):
                    #Only append unique URLS. 
                    url_list.append(link.get('href'))
        #Handle the case where something goes wrong
        except Exception as e:
            insert_avoid(url)
            with open("errors.txt", 'a', encoding='utf-8') as file:
                file.write(f"An error occurred: {str(e)}\n")
            return url_list
    else:
        #Add to the list of bad urls/urls to avoid if server response != 200
        insert_avoid(url)
        return url_list
        
    #Check the CONTENT of the html text for any calendars:
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    #print(f"URLS FOUND IN {url} {url_list}")
    return url_list

def is_valid(url):
    #print(f"Checking the urls found in URL {url}")
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url) #urlparse(url)
        subdomain = ''
        #DMM:  Defragment the URL before further processing: 
        if parsed.scheme not in set(["http", "https"]):
            insert_avoid(url)
            return False

        #Pattern to check url for dates
        pattern = (
        r"^(\d{4}-\d{2}-\d{2})$|"      # YYYY-MM-DD
        r"^(\d{2}/\d{2}/\d{4})$|"      # MM/DD/YYYY
        r"^(\d{2}-\d{2}-\d{4})$|"      # DD-MM-YYYY
        r"^(\d{2}/\d{4})$|"            # MM/YYYY
        r"^(\d{4}/\d{2})$|"            # YYYY/MM
        r"^/\d{4}/\d{2}/$"             # /YYYY/MM/
        r"^/page/\d$"
        )
        
        #Check that the urls are within the domain and paths.
        #CHECK A: Check that if the URL's domain is 'today.uci.edu)
        if re.match(r"^([a-z0-9_-]+\.)*(today.uci.edu)$", parsed.netloc.lower()):
            #Check that the path is  /department/information_computer_sciences/
            if( parsed.path.lower() != "/department/information_computer_sciences/"):
                insert_avoid(url)
                return False
        if not re.match(r"^([a-z0-9_-]+\.)*(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu)$", parsed.netloc.lower()):
            #print(f"{parsed} is NOT a VALID url\n")
            insert_avoid(url)
            return False
        #if ('events' in parsed.path.lower() or 'explore' in parsed.path.lower()):
            #return False

        '''
        if (re.search(pattern, parsed.path.lower())):
            print("URL HAS DATE FALSE")
            insert_avoid(url)
            return False
        '''

        #Avoid any login buttons. 
        if parsed.query: 
            if parse_qs(parsed.query).get("action"):
                insert_avoid(url)
                return False 
            '''
            if re.match(r"page_id=([^&]*)", parsed.query.lower()):
                return False
            '''
        #Check for comment and respond fragments that cause looping 
        #DMM: Check if there is HIGH text content;
        #Insert Implementation
        
        
        if ( re.match(r".*\.(css|js|bmp|gif|jpe?g|ico|heic|html|php"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())):
            #print (f'Valid URL {parsed}')
            return False
        #If it is in the correct domain and it satisfied all the other requirements, add to list of subdimains. 
        if (re.match(r"^([a-z0-9_-]+\.)*uci\.edu$", parsed.netloc.lower())):
            uci_subdomain(parsed.netloc.lower())
            #print(f"{parsed} added to subdomain. ")
        #print(f"Valid url : {url}")

        #If the url contains a fragment and we have already gone to the 
        #url and added it to unique url list, return False to avoid traps.
        if(parsed.fragment and insert_unique(parsed)):
            insert_avoid(url)
            return False
        #If there is no fragment, just add it to the unique list. 
        else:
            insert_unique(parsed)

        return True
        '''
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|html|heic)$", parsed.path.lower())
    '''
    except TypeError:
        print ("TypeError for ", parsed)
        raise
