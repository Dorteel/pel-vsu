import json
from nltk.corpus import wordnet as wn
from nltk import download

download('wordnet')
download('omw-1.4')

# Load your object set
with open("objects_synsets.json", "r") as f:
    objects = json.load(f)

def synset_info(synset):
    return {
        "synset": synset.name(),
        "definition": synset.definition(),
        "synonyms": list(set(lemma.name() for lemma in synset.lemmas()))
    }

def get_hypernym_chain(synset):
    chain = []
    current = synset
    while current.hypernyms():
        parent = current.hypernyms()[0]
        chain.append(synset_info(parent))
        current = parent
    return chain

def get_hyponym_tree(synset):
    children = synset.hyponyms()
    if not children:
        return []

    return [{
        **synset_info(child),
        "hyponyms": get_hyponym_tree(child)
    } for child in children]

def get_wordnet_info(label, synset):

    return {
        **synset_info(synset),
        "hypernyms": get_hypernym_chain(synset),
        "hyponyms": get_hyponym_tree(synset)
    }

# Now apply the function to each object
results = {}
for label, synset_list in objects.items():
    print(f"Processing: {label}")
    if not synset_list:
        results[label] = {"error": "no synset list found"}
        continue

    synset_name = synset_list[0]["synset"]
    try:
        synset = wn.synset(synset_name)
        wn_info = get_wordnet_info(label, synset)
        wn_info["rdfs:label"] = label
        results[label] = wn_info
    except Exception as e:
        results[label] = {"error": f"Failed to get synset for '{label}': {str(e)}"}

with open("als_objects_wordnet_full_tree.json", "w") as out_file:
    json.dump(results, out_file, indent=2)

print("Done. May your ontology overfloweth.")
