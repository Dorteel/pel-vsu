#!/bin/bash

# Create target directory
mkdir -p visual_genome && cd visual_genome

# Download images
# echo "Downloading images..."
wget -c https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip -O VG_100K.zip
wget -c https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip -O VG_100K_2.zip

# Download dataset components
echo "Downloading objects..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/objects.json.zip

echo "Downloading attributes..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/attributes.json.zip

echo "Downloading relationships..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/relationships.json.zip

echo "Downloading region descriptions..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/region_descriptions.json.zip

echo "Downloading image metadata..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/image_data.json.zip

echo "Downloading question answers..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/question_answers.json.zip

echo "Downloading object aliases..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/object_alias.txt

echo "Downloading relationship aliases..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/relationship_alias.txt

echo "Downloading object synsets..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/object_synsets.json.zip

echo "Downloading attribute synsets..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/attribute_synsets.json.zip

echo "Downloading relationship synsets..."
wget -c https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/relationship_synsets.json.zip

# Unzip all zip files
echo "Unzipping files..."
unzip -o VG_100K.zip
unzip -o VG_100K_2.zip
unzip -o objects.json.zip
unzip -o attributes.json.zip
unzip -o relationships.json.zip
unzip -o region_descriptions.json.zip
unzip -o image_data.json.zip
unzip -o question_answers.json.zip
unzip -o object_synsets.json.zip
unzip -o attribute_synsets.json.zip
unzip -o relationship_synsets.json.zip

echo "Download and extraction complete."
