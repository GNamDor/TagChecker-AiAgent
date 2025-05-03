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
    
def regex_sort(word, op_stack, cl_queue):
    '''
    use regex to compare if a Tag has <, /, A-Z and >, if so, store them either in
    stack or queue
    '''
    if re.match(r"<[A-Z]>", word):
        op_stack.append(word)
    elif re.match(r"<\/[A-Z]>", word):
        cl_queue.append(word)

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

def output_processing(smallest_stack_size, stack_op_tag, queue_cl_tag):
    '''
    loops over the smallest data structure and compares the last of a stack with
    the first of the queue.
    stack is used for the opening tags and queue for the closing tags

    when they are compared, if they don't match, exit the function. Else
    continue comparing until the smallest is exhausted.

    if stack is not empty, output message for stack - found # ...
    if if queue is not empty, output message for queue - Expected # ...
    if both are empty, output message - Correctly tagged paragraph
    '''
    for _ in range(smallest_stack_size):
        op = stack_op_tag.pop()
        cl = queue_cl_tag.popleft()
        
        if op != remove_slash(cl):
            return f'"Expected {add_slash(op)} found {cl}",'
    
    # if smallest was queue
    if len(stack_op_tag) > 0:
        return f'"Expected {add_slash(stack_op_tag.pop())} found #",'
    # if smallest with stack
    elif len(queue_cl_tag) > 0:
        return f'"Expected # found {queue_cl_tag.pop()}",'
    # if they are of equal size and items were same throughout
    else:
        return '"Correctly tagged paragraph",'