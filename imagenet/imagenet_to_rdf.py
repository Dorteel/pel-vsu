import nltk
from nltk.corpus import wordnet as wn
from rdflib import Graph, Namespace, Literal, RDF, RDFS, SKOS, URIRef
from rdflib.namespace import OWL

nltk.download("wordnet")
nltk.download("omw-1.4")

EX = Namespace("http://example.org/imagenet21k/")

def wnid_to_synset(wnid):
    try:
        pos = wnid[0]
        offset = int(wnid[1:])
        return wn.synset_from_pos_and_offset(pos, offset)
    except:
        return None

def add_synset_to_graph(g, synset, added):
    uri = EX[synset.name()]
    if uri in added:
        return uri  # Already processed

    g.add((uri, RDF.type, OWL.Class))
    g.add((uri, RDFS.label, Literal(synset.name().split('.')[0].replace("_", " "), lang="en")))
    g.add((uri, RDFS.comment, Literal(synset.definition(), lang="en")))

    for lemma in synset.lemma_names():
        label = lemma.replace("_", " ")
        if label.lower() != synset.name().split('.')[0]:
            g.add((uri, SKOS.altLabel, Literal(label, lang="en")))

    for ex in synset.examples():
        g.add((uri, EX.example, Literal(ex, lang="en")))

    added.add(uri)

    # Add hypernyms (superclasses)
    for parent in synset.hypernyms():
        parent_uri = add_synset_to_graph(g, parent, added)
        g.add((uri, RDFS.subClassOf, parent_uri))

    return uri

def create_hierarchical_kg(txt_file, output_file="imagenet21k.ttl"):
    g = Graph()
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)
    g.bind("owl", OWL)
    g.bind("ex", EX)

    missing = []
    total = 0
    added = set()

    with open(txt_file, "r") as f:
        wnids = [line.strip() for line in f if line.strip()]

    for wnid in wnids:
        total += 1
        synset = wnid_to_synset(wnid)
        if not synset:
            print(f"[WARN] Couldn't resolve {wnid}")
            missing.append(wnid)
            continue

        add_synset_to_graph(g, synset, added)

    g.serialize(destination=output_file, format="turtle")
    print(f"✅ Knowledge graph saved to '{output_file}'")

    print("\n📊 Conversion Summary")
    print(f"  Total WNIDs processed: {total}")
    print(f"  Successfully converted: {total - len(missing)}")
    print(f"  Failed to resolve: {len(missing)}")

    if missing:
        print("\n❌ Missing WNIDs:")
        for m in missing:
            print(f"  - {m}")

# Usage
create_hierarchical_kg("imagenet21k_wordnet_ids.txt")
