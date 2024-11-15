import sys

'''

Tokernizer


@params: file path
@return: none
--> Tokenize method extracts the tokens from a file. 
--> A token is defined as any sequence of alphaneumeric characters.
--> In order to account for large files, the file is read line by line 
    and the tokens are yielded instead of stored in a list. 
--> Complexity: This results in a O(n) runtime complexity since it runs
    in linear time relative to the size of the input file. 
'''
top_fifty = [("", -1) for _ in range(50)]
highest_count = [(0, "")]


def tokenize():
    #In order to handle large files...
    #Step 1:read the file line by line
    try:
        with open("search_text.txt", 'r', encoding='utf-8') as file:
            for line in file:
                #Variable to store the valid alphanuermic sequences of each line
                valid = ""
                #normalize the line
                line = line.lower()
                #traverse the line character by character
                for letter in range(len(line)):
                    #If the character is an alphaneumeric character, add it to the sequence
                    if (ord(line[letter]) >= 97 and ord(line[letter]) <= 122) or (ord(line[letter]) >= 48 and ord(line[letter]) <= 57):
                        valid += line[letter]
                    else:
                        #Upon an invalid character,
                        #If the sequece is not empty, yield the sequence
                        if len(valid) >= 3:
                            yield valid
                            #Reset the sequence to empty
                            valid = ""
                #If there is a valid sequence, make sure to yield this value as well
                if len(valid) >= 3:
                    yield valid
    except Exception as e:
        print(f"An error occurred: {e}")

'''
@params: iterable containing tokens
@return: dictionary with key-value pair of {token, # of occurances}
--> Traverse the iterable containing the tokens and add to dictionary
--> Increase the count of each repeated token. 
--> Complexity: This results in a O(n) runtime complexity since it runs
    in linear time relative to the size of the number of tokens in the list. 
'''

def computeWordFrequencies(tokens):
    token_count = dict()
    for t in tokens:
        if t not in token_count:
            token_count[t] = 1
        else:
            token_count[t] += 1
    return token_count


'''
@params: dictionary of tokens
@return: none
--> Sorts the tokens in the dictionary in descending order
--> Prints sorted dictionry's key value pair as specified in the assignemnt description
--> Complexity: This results in a O(nlogn) runtime complexity due to the sorting function,
and is relative to the number of items in the dictionary of tokens. 
'''
def findMax(token_dict, url):
    #If it equals the key value, add to the count,
    #If it is greater than the key value, replace it 
    #If it is less than the key value, do nothing. 
    count = 0
    total_tokens = sum(token_dict.values())
    if (total_tokens > highest_count[0][0]):
        highest_count[0] = (total_tokens, url)
    top_50 = list()
    for token in sorted(token_dict.items(), key=lambda x:x[1], reverse=True):
        if count < 50:
            top_50.append((token[0], token[1]))
        count += 1
    #print(top_50)
    # Update top_fifty dictionary with the top 50
    #For each word
    for word,frequency in top_50:
        inserted = False
        #Check if it is greater than the current index. 
        for index in range(len(top_fifty)):
            #If the words match, add the frequencies. 
            if(top_fifty[index][0] == word):
                top_fifty[index] = (word, top_fifty[index][1] + frequency)
                inserted = True
                break
            #If the frequency is greater than the one right here, replace it. 
            elif (top_fifty[index][1] < frequency):
                # Insert at the current position
                top_fifty.insert(index, (word, frequency))
                # Remove the last element to maintain correct size of 50
                top_fifty.pop()
                inserted = True
                break
            elif(top_fifty[index][1] == frequency):
                if(index < 49):
                    top_fifty.insert(index + 1, (word, frequency))
                    # Remove the last element to maintain list size
                    top_fifty.pop()
                inserted = True
                break
         # If the word is not inserted yet and there's space, append it
        if not inserted:
            if len(top_fifty) < 50:
                top_fifty.append((word, frequency))


def analyze_file(url):
    #Extract the tokens from the current file
    token_list = tokenize()
    #Count the frequency of tokens
    freq_token = computeWordFrequencies(token_list)
    findMax(freq_token, url)
    #print the top 50 tokens

