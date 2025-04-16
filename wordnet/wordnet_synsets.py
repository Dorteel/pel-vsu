import json
from nltk.corpus import wordnet as wn
from nltk import download

download('wordnet')
download('omw-1.4')

# Load objects list
with open("objects.json", "r") as f:
    objects = json.load(f)

def synset_info(synset):
    return {
        "synset": synset.name(),
        "definition": synset.definition()
    }

def suggest_synsets(label, max_results=1):
    label_clean = label.lower().replace(" / ", " ").replace("-", " ").replace("_", " ")
    words = label_clean.split()

    synsets = wn.synsets(label_clean)
    if not synsets and len(words) > 1:
        synsets = wn.synsets(words[-1])

    return [synset_info(s) for s in synsets[:max_results]]

# Phase 1: generate suggestions
synset_suggestions = {}
for obj in objects:
    print(f"Suggesting synsets for: {obj}")
    synset_suggestions[obj] = suggest_synsets(obj)

with open("objects_synsets.json", "w") as f:
    json.dump(synset_suggestions, f, indent=2)

print("Suggestions saved to 'objects_synsets.json'")
