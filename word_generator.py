import wikipediaapi 
from search_word import search_value

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='python-requests/2.31.0'
)
# List of pre-processing wordsz
#first_list = []

# List of already checked words
looked_up = []

# List to save the Words
saved_list = []

def check_word(looked_up, word):
    return word in looked_up

def get_limited_summary(word, sentence_limit=2):
    page = wiki.page(word)  # Fetch the Wikipedia page corresponding to the word
    if page.exists():
        summary = page.summary
        sentences = summary.split('. ')
        limited_summary = '. '.join(sentences[:sentence_limit])
        if len(sentences) > sentence_limit:
            limited_summary += '...'
        return limited_summary
    else:
        return f"Page '{word}' does not exist on Wikipedia."

def save_word(saved_list, word):
    save = input("Enter 'save' to save the word: \nEnter 'No' to not save the word: \n")
    if save.lower() == 'save':
        saved_list.append(word)
        print(f"Word '{word}' saved.")
    elif save.lower() == 'no':
        print(f"Word '{word}' not saved.")

def delete_saved(saved_list):
    delete = input("Enter 'Yes' to delete the word in saved list:\nEnter 'No' to not delete :\n")
    if delete.lower() == 'yes':
        print_saved_words(saved_list)
        num = input("Enter the serial num of the word to delete :\n")
        try:
            index = int(num) - 1
            if 0 <= index < len(saved_list):
                deleted_word = saved_list.pop(index) 
                print(f"Deleted {deleted_word}")
            else :
                print("Invalid serial number")
                delete_saved(saved_list)
        except ValueError:
            print("Enter a valid number")
            delete_saved(saved_list) 
    elif delete.lower() == 'no':
         print("Let's continue.")


def print_saved_words(saved_list):
    if not saved_list:
        print("The list is empty")
    else:
        for i, word in enumerate(saved_list, start=1):
            print(f"{i}. {word}")

def define_saved(saved_list):
    print_saved_words(saved_list)
    num = input("Enter the serial num of the word to define :\n")
    try:
        index = int(num) - 1
        if 0<= index < len(saved_list):
            word = saved_list[index]
            print(f"{word}:")
            search_value(word) 
        else :
            print("Invalid serial number")
            define_saved(saved_list)
    except ValueError:
            print("Enter a valid number") 
   

def word_access(conn, retrieve_list, looked_up):
    retrieved_words = retrieve_list(conn)
    for row in retrieved_words:
        word = row[1]  # Assuming the word is in the second column
        if not check_word(looked_up, word):
            print(word)
            print(get_limited_summary(word, sentence_limit=2))
            print('Detailed explanation :\t YES : 1 \t NO : 0')
            yesNo = input()

            if yesNo == '1':
                print('Detailed explanation:')
                # Fetch the Wikipedia page corresponding to the word
                page = wiki.page(word)
                if page.exists():
                    print(page.summary)
                    save_word(saved_list,word)
                    print("Let's move to the next word ")
                else:
                    print(f"Page '{word}' does not exist on Wikipedia.")
            else:
               save_word(saved_list,word)
               print("Let's move to the next word ")
            
            looked_up.append(word)
            user_input = input("Press Enter to retrieve the next word or type 'exit' to stop: ")
            if user_input.lower() == 'exit':
                break


