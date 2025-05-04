'''
Functions used by TagChecker.py
'''
import re


def get_sentences(file_path):
    '''
    get sentences from txt file, split sentences based on if they have " and , 
    '''
    f = open(file_path)
    paragraph = f.read()
    return paragraph.strip().split('",')

def preprocess_sentence(text):
    '''
    add padding for all the tags using replace method
    '''
    insert_space = text.replace(">","> ")
    result = insert_space.replace("<", " <")
    return result
    

def remove_slash(word):
    '''
    convert a closing tag to an open tag
    useful for printing the output string
    '''
    return word[0]+word[2:]    

def add_slash(word):
    '''
    convert an open tag to a closing tag
    useful for printing the output string
    '''
    return word[0] + "/" + word[1:]   

def regex_sort(words, op_stack):
    '''
    use regex to compare if a Tag has <, /, A-Z and >, if so, store them either in
    stack or queue
    '''
    # for each word in a sentence
    for word in words:
        # opening tag match, then append
        if re.match(r"<[A-Z]>", word):
            op_stack.append(word)
        # closing tag match then decision process
        elif re.match(r"<\/[A-Z]>", word):
            # try to access last item
            if len(op_stack)<1:
                # if empty, then sentence is not correct, output statement
                return f'"Expected # found {word}",'
            # if tags match pop them and continue
            if op_stack[-1] == remove_slash(word):
                op_stack.pop()
            # if tags don't match then sentence is not correct, output statement
            else:
                return f'"Expected {add_slash(op_stack.pop())} found {word}",'
    # if stack was not completely popped, then unused closing tags are present
    if len(op_stack)>0:
        return f'"Expected {add_slash(op_stack.pop())} found #",'
    
    # if all conditions pass, then sentence is correctly tagged
    return 'Correctly tagged paragraph",'
