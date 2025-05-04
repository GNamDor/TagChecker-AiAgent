from HelperFunctions import get_sentences, preprocess_sentence, remove_slash, add_slash, regex_sort
 
sentences = get_sentences("Paragraph.txt")

def main():

    for sentence in sentences:

        # opening tags will be stored in stack and closing in queues
        stack_opening_tag = []

        # if a sentence is empty, skip
        if len(sentence) <1:
            continue

        # seperate tags from other strings
        sentence = preprocess_sentence(sentence)
        words = sentence.split(" ")

        #used https://regex101.com/ for testing
        #sort the words based on if its an opening or closing tag
        result = regex_sort(words, stack_opening_tag)
        print(result)

if __name__ == "__main__":
    main()