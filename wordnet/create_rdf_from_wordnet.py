import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS

# Load the enriched WordNet JSON file
with open("als_objects_wordnet_full_tree.json", "r") as f:
    data = json.load(f)

# Define the namespace for your ontology
ORKA = Namespace("https://w3id.org/def/orka#")
WN = Namespace("http://wordnet-rdf.princeton.edu/wn30/")

graph = Graph()
graph.bind("orka", ORKA)
graph.bind("skos", SKOS)
graph.bind("rdfs", RDFS)

def create_concept(uri, syn_data):
    graph.add((uri, ORKA.hasWordNetSynset, Literal(syn_data["synset"])))
    graph.add((uri, RDFS.comment, Literal(syn_data["definition"])))
    graph.add((uri, RDFS.label, Literal(syn_data["synonyms"][0])))
    for synonym in syn_data["synonyms"]:
        graph.add((uri, SKOS.altLabel, Literal(synonym.replace('_', ' '))))

def walk_subclasses(parent_uri, hyponyms):
    for child in hyponyms:
        child_uri = URIRef(ORKA + child["synset"])
        create_concept(child_uri, child)
        graph.add((child_uri, RDFS.subClassOf, parent_uri))
        walk_subclasses(child_uri, child.get("hyponyms", []))

for label, concept in data.items():
    if "error" in concept:
        continue

    main_uri = URIRef(ORKA + concept["synset"])
    create_concept(main_uri, concept)

    # Hypernyms as rdfs:subClassOf links
    last_uri = main_uri
    for hyp in concept["hypernyms"]:
        hyp_uri = URIRef(ORKA + hyp["synset"])
        create_concept(hyp_uri, hyp)
        graph.add((last_uri, RDFS.subClassOf, hyp_uri))
        last_uri = hyp_uri

    # Hyponym tree
    walk_subclasses(main_uri, concept.get("hyponyms", []))

# Save the graph
graph.serialize("als_objects.rdf", format="turtle")
print("RDF graph saved as als_objects.rdf")
