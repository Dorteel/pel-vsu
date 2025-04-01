import json
import zipfile
import os
from collections import Counter

# Path to the Visual Genome dataset directory
VG_DIR = "visual_genome"

# Synset files (filename, label)
SYNSET_FILES = [
    ("object_synsets.json.zip", "object"),
    ("attribute_synsets.json.zip", "attribute"),
    ("relationship_synsets.json.zip", "relationship"),
]

# Function to load JSON from a zip file
def load_json_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        json_filename = zf.namelist()[0]
        with zf.open(json_filename) as f:
            return json.load(f)

# Dictionary to store synset stats
synset_summary = {}

for filename, syn_type in SYNSET_FILES:
    path = os.path.join(VG_DIR, filename)
    if not os.path.exists(path):
        print(f"File not found: {filename}")
        continue

    print(f"Loading {filename}...")
    data = load_json_from_zip(path)

    # Extract synsets and names
    synsets = [entry['synsets'] for entry in data if 'synsets' in entry]
    flat_synsets = [syn for sublist in synsets for syn in sublist]  # Flatten list
    synset_counter = Counter(flat_synsets)

    # Summary for this synset type
    synset_summary[syn_type] = {
        'unique_synsets': len(synset_counter),
        'most_common': synset_counter.most_common(5),
        'example_synsets': flat_synsets[:5]
    }

# Print summary
print("\n=== Synset Summary ===")
for syn_type, stats in synset_summary.items():
    print(f"\n{syn_type.capitalize()} Synsets:")
    print(f"  Unique synsets     : {stats['unique_synsets']}")
    print(f"  Most common synsets: {stats['most_common']}")
    print(f"  Example synsets    : {stats['example_synsets']}")
