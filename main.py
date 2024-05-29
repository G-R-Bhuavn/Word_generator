import wikipediaapi
from word_generator import word_access, looked_up , saved_list, print_saved_words, delete_saved, define_saved,save_word
from sql_link import create_connection, create_table, insert_word, indexing_list, retrieve_list
from search_word import search_value

# Create a Wikipedia object with a user agent string
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='python-requests/2.31.0'
)

# Define the topic you want to search for
topic = "Glossary_of_computer_science" 

# Fetch the page for the topic
page = wiki.page(topic)

# Check if the page exists
if page.exists():
    # Print the summary of the page
    print("Summary:")
    print(page.summary)

    # Collect all links
    word_list = list(page.links.keys())
    
    # Database operations
    database = 'glossary.db'
    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn)
        indexing_list(conn)
        insert_word(conn, word_list)
        #delete_all_entries(conn)
        #delete_unwanted_entries(conn,topic)
        
        continue_loop = True
        
        while continue_loop:
            print('\n1. Retrieve new word\n2. Search word\n3. Saved words\n4. Exit')
            value = input('Enter your choice: ')
            print(f'You entered: {value}')
            if value == '1':
                print('Retrieving new word...')
                word_access(conn, retrieve_list, looked_up)
            elif value == '2':
                print('Enter value to be searched')
                key = input()
                search_value(key)
                to_save = input("Enter 'Save' to save the searched word\nEnter 'No' to not save \n")
                if to_save.lower() == 'save':
                    save_word(saved_list,key)
                elif to_save.lower() == 'no':
                    continue
            elif value == '3':
                print("The saved words are : \n" )
                print_saved_words(saved_list)  
                if saved_list:
                    options = input("Define a word: Enter 'Define'\nDelete a word: Enter 'Delete'\nExit: Enter 'Exit'\n")
                    if options.lower() == 'define':
                        define_saved(saved_list)
                    elif options.lower() == 'delete':
                        delete_saved(saved_list)
                    elif options.lower() == 'exit':
                        continue
                
            elif value == '4':
               print("Exiting the loop.")
               continue_loop = False
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        
        conn.close()  # Ensure the connection is closed after the loop ends
    else:
        print("Error! Cannot create the database connection.")
else:
    print(f"Page '{topic}' does not exist on Wikipedia.")
