import sqlite3,wikipediaapi
#from word_generator import first_list

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
       # print(f'Connected to: {db_file}')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(''' 
                        CREATE TABLE IF NOT EXISTS Glossary_terms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        words TEXT NOT NULL)''')
        #print('Table created')
    except sqlite3.Error as e:
        print(e)

def insert_word(conn, word_list):
    try:
        cursor = conn.cursor()
        for word in word_list:
            cursor.execute('''INSERT INTO Glossary_terms(words) VALUES(?)''', (word,))
        conn.commit()
       # print('Data inserted')
    except sqlite3.Error as e:
        print(e)

def indexing_list(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_words on Glossary_terms(words)')#index created on the column name "words" of the db table Glossary_terms
        #print('index created')
    except sqlite3.Error as e:
        print(e)
        
def retrieve_list(conn):
    """Retrieve random words from the table."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Glossary_terms ORDER BY RANDOM()')
    return cursor.fetchall()
            
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='python-requests/2.31.0'
)


#def delete_all_entries(conn):
    #try:
        #cursor = conn.cursor()
        #cursor.execute('DELETE FROM Glossary_terms')
        #conn.commit()
        #print("All entries have been deleted.")
    #except sqlite3.Error as e:
        #print(e)


def is_related_to_topic(word, topic):
    # Fetch the page for the topic
    page = wiki.page(topic)
    
    # Check if the page exists
    if not page.exists():
        return False
    
    # Check if the word appears in the links of the topic page
    return word in page.links

def delete_unwanted_entries(conn, topic):
    cursor = conn.cursor()
    
    # Retrieve the list of words from the database
    cursor.execute("SELECT id, words FROM Glossary_terms")
    rows = cursor.fetchall()
    
    # Iterate through the rows and delete entries not related to the topic
    for row in rows:
        word_id, word = row
        if not is_related_to_topic(word, topic):
            # Delete the entry if the word is not related to the topic
            cursor.execute("DELETE FROM Glossary_terms WHERE id = ?", (word_id,))
            print(f"Deleted: {word}")
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor
    cursor.close()
