import wikipediaapi
#from word_generator import save_word ,saved_list

# Create a Wikipedia object with a user agent string
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='python-requests/2.31.0'
)

def search_value( key):
    # Search and allocate the page 
    page = wiki.page(key)

    def get_limited_summary(page, sentence_limit=2):
        # To split the summary to limited number and avoid lengthy outputs
        summary = page.summary
        sentences = summary.split('. ')
        limited_summary = '. '.join(sentences[:sentence_limit])
        if len(sentences) > sentence_limit:
            limited_summary += '...'
        return limited_summary

    if page.exists():
        print(get_limited_summary(page, sentence_limit=2))

        # To ask user for more info
        print('Detailed explanation :\t YES : 1 \t NO : 0')
        yesNo = input()

        if yesNo == '1':
            print('Detailed explanation:')
            print(page.summary)
        else:
            print('Exiting detailed explanation.')
    else:
        print(f"Page '{key}' does not exist on Wikipedia.")
