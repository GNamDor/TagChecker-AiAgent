from HelperFunctions import get_sentences, preprocess_sentence,regex_sort, remove_slash, add_slash, output_processing
from collections import deque

def main():

    sentences = get_sentences("Paragraph.txt")

    for sentence in sentences:
        # opening tags will be stored in stack and closing in queues
        stack_opening_tag = []
        queue_closing_tag = deque()

        # if a sentence is empty, skip
        if len(sentence) <1:
            continue

        # seperate tags from other strings
        sentence = preprocess_sentence(sentence)
        words = sentence.split(" ")

        for word in words:
            #used https://regex101.com/ for testing
            #sort the words based on if its an opening or closing tag
            regex_sort(word, op_stack=stack_opening_tag, 
                             cl_queue=queue_closing_tag)

        smallest_stack_size = min(len(stack_opening_tag), len(queue_closing_tag))

        result = output_processing(smallest_stack_size, stack_opening_tag, queue_closing_tag)
        print(result)

if __name__ == "__main__":
    main()