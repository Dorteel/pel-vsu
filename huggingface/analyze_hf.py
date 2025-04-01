import pandas as pd
import ast

# Load model data
hf_data = pd.read_csv('huggingface_models_all.csv')

# Safely parse stringified label lists
def parse_labels(label_str):
    if pd.isna(label_str):
        return []
    try:
        return ast.literal_eval(label_str)
    except (ValueError, SyntaxError):
        return []

# Add parsed_labels column
hf_data['parsed_labels'] = hf_data['labels'].apply(parse_labels)

# Tasks to include in the LaTeX table
latex_tasks = [
    "image-classification",
    "image-segmentation",
    "image-to-text",
    "object-detection",
    "video-classification",
    "zero-shot-classification",
    "zero-shot-image-classification",
    "zero-shot-object-detection",
    "visual-question-answering"
]

# Prepare LaTeX-ready stats
latex_rows = []
for task in latex_tasks:
    group = hf_data[hf_data['task'] == task]

    total_models = len(group)

    # Filter models that have at least 1 label
    group_filtered = group[group['parsed_labels'].apply(lambda x: len(x) > 0)]
    num_filtered = len(group_filtered)

    # Count all unique labels across filtered models
    all_labels = []
    for labels in group_filtered['parsed_labels']:
        all_labels.extend(labels)
    unique_labels = set(all_labels)

    # Average number of labels per filtered model
    avg_labels = (
        sum(len(labels) for labels in group_filtered['parsed_labels']) / num_filtered
        if num_filtered > 0 else 0
    )

    latex_rows.append([
        task.replace("-", " ").title(),  # Prettify for LaTeX
        total_models,
        num_filtered,
        len(unique_labels),
        round(avg_labels, 1)
    ])

# Output for LaTeX
print("\\begin{tabular}{||l|l|c|c|c||}")
print("\\textbf{Task Type} & Models & Filtered models & Semantic labels & Avg. Label per model \\\\")
for row in latex_rows:
    print(f"{row[0]} & {row[1]} & {row[2]} & {row[3]} & {row[4]} \\\\")
print("\\end{tabular}")
