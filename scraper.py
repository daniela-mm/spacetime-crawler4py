import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def scraper(url, resp):
    print("In scaper function.")
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
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
        # Find all the links in the page
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Print out all the links found. 
        for link in soup.find_all('a'):
            print(link.get('href'))
            #Append the link to the list of links. 
            url_list.append(link)
    #DMM: Case 2: If raw response IS empty:
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return url_list

def is_valid(url):
    #DMM: Create a list of valid domains. 
    valid_domains = [".ics.uci.edu/", ".cs.uci.edu/", "informatics.uci.edu", ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        #DMM:  Defragment the URL before further processing: 
        parsed = parsed.split('#')[0]
        if parsed.scheme not in set(["http", "https"]):
            return False
        #Check that the urls are within the domain and paths.
        if (parsed.netloc not in  valid_domains):
            print(f"{parsed} URL is NOT in the domain. ")
            return False
        #DMM: Check if there is HIGH text content;
        #Insert Implementation
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
