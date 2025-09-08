from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = numLetters(text)
    words = numWords(text)
    sentences = numSentences(text)

    # Compute the Coleman-Liau index
    avgLetters = letters / words * 100
    avgSentences = sentences / words * 100
    gradeLevel = 0.0588 * avgLetters - 0.296 * avgSentences - 15.8
    grade = round(gradeLevel)

    # Print the grade level
    if grade == 16 or grade > 16:
        print("Grade 16+")

    elif grade < 1:
        print("Before Grade 1")

    else:
        print(f"Grade {grade}")

# Return the number of letters in text


def numLetters(text):
    count = 0
    for i in range(len(text)):
        if (text[i].isalpha()):
            count += 1

    return count

# Return the number of words in text


def numWords(text):
    count = 1
    for i in range(len(text)):
        if (text[i] == " "):
            count += 1

    return count

# Return the number of sentences in text


def numSentences(text):
    count = 0
    for i in range(len(text)):
        if text[i] == "." or text[i] == "?" or text[i] == "!":
            count += 1

    return count


main()
