import nltk
from nltk.corpus import wordnet as wn

# Download resources (just once)
nltk.download('wordnet')
nltk.download('omw-1.4')

def get_synsets(word):
    """Print all synsets for a given word with their definitions."""
    synsets = wn.synsets(word)
    for i, synset in enumerate(synsets):
        print(f"[{i}] {synset.name()}: {synset.definition()}")
    return synsets

def get_subclasses(synset):
    """Return the direct hyponyms (subclasses) of a given synset."""
    hyponyms = synset.hyponyms()
    if not hyponyms:
        print(f"{synset.name()} has no hyponyms.")
    else:
        for i, h in enumerate(hyponyms):
            print(f"\t[{i}] {h.name()}: {h.definition()}")
            get_subclasses(h)
        return hyponyms

word = "mail"
print(f"{'='*50}\nPrinting the sysntes for the word {word}:\n")
synsets = get_synsets(word)
loop = 1
for selected_synset in synsets:
    print(f"{'='*50}\n\tPrinting the sysntes for the word {selected_synset}:\n")
    hyponyms = get_subclasses(selected_synset)
