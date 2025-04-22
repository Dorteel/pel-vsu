import rdflib
from rdflib import Graph, Namespace, URIRef, RDFS
from nltk.corpus import wordnet as wn

# Namespaces
IMAGENET = Namespace("http://example.org/imagenet1k/")

# Load ImageNet-21k WordNet IDs
with open("imagenet/imagenet21k_wordnet_ids.txt", "r") as f:
    imagenet21k_ids = set(line.strip() for line in f if line.strip())

# Load existing RDF graph
g = Graph()
g.parse("imagenet1k_wordnet_classes.rdf", format="xml")

# Function to check if a synset (or its hyponyms) are in ImageNet-21k
def check_imagenet21k_presence(synset_id):
    # Normalize the synset ID
    if '-' in synset_id:
        base_id, pos = synset_id.split('-')
        formatted_id = f'n{base_id}'
    else:
        formatted_id = synset_id

    if formatted_id in imagenet21k_ids:
        return True

    try:
        offset = int(formatted_id[1:])  # skip the 'n'
        wn_pos = wn.NOUN  # Assume noun
        synset = wn.synset_from_pos_and_offset(wn_pos, offset)
        for hypo in synset.hyponyms():
            hypo_id = f"n{str(hypo.offset()).zfill(8)}"
            if hypo_id in imagenet21k_ids:
                return True
    except Exception as e:
        print(f"Warning: couldn't process synset {synset_id}: {e}")
    return False

# Update RDF graph
to_update = []
for s in g.subjects(RDFS.label, None):
    synset_id = str(s).split("/")[-1]  # Extract synset id from URI
    if check_imagenet21k_presence(synset_id):
        to_update.append(s)

for node_uri in to_update:
    g.add((node_uri, RDFS.comment, rdflib.Literal("Synset is part of ImageNet-21k.")))

# Save updated graph
g.serialize(destination="imagenet_combined_wordnet_classes.rdf", format="xml")

print("Graph updated: ImageNet-21k membership annotated without ridiculous parsing errors.")
