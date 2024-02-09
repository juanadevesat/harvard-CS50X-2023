# TODO

import cs50


# Main function
def main():
    text = cs50.get_string("Text: ")
    w = count_words(text)
    l = count_letters(text) * 100.0 / w
    s = count_sentences(text) * 100.0 / w
    index = round((0.0588 * l) - (0.296 * s) - 15.8)

    if (index < 1):
        print("Before Grade 1")

    elif (index > 16):
        print("Grade 16+")

    else:
        print(f"Grade {index}")


# Function to count letters in text
def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha() == True:
            letters += 1

    return letters


# Function to count words
def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i] == " " or text[i] == "   ":
            words += 1

    return words


# Function to count sentences
def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1

    return sentences


# Call main
main()