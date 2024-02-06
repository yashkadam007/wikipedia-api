from collections import Counter
from mediawiki import MediaWiki, PageError, DisambiguationError

def get_top_words(topic, n):
    wikipedia = MediaWiki()
    try:
        content = wikipedia.page(topic).content
    except PageError:
        return {"status": "error", "message": "Topic not found on Wikipedia"}
    except DisambiguationError as e:
        return {"status": "error", "message": f"DisambiguationError: {e.options}"}

    word_counts = Counter(word.lower() for word in content.split()) #convert all words to lower case so that same words in different case are considered same
    top_n_words = word_counts.most_common(n)

    return {
        "topic": topic,
        "top_n_words": top_n_words,
    }
