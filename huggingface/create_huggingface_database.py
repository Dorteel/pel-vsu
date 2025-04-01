import csv
from huggingface_hub import HfApi
from transformers import AutoConfig

# Define tasks of interest
tasks = [
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

api = HfApi()

def get_models(task):
    """
    Fetch models from Hugging Face Hub for a specific task.
    """
    models = api.list_models(filter=task)
    return models

def get_model_info(model):
    """
    Extract model information: architecture, labels, etc.
    """
    try:
        config = AutoConfig.from_pretrained(model.modelId, trust_remote_code=True)
        labels = list(config.id2label.values()) if hasattr(config, "id2label") else []
    except Exception:
        labels = []

    return {
        "model_id": model.modelId,
        "task": model.pipeline_tag,
        "labels": "".join(str(labels)) if labels else ""
    }

def write_to_csv(models_info, filename="huggingface_models_all.csv"):
    """
    Write model information to CSV.
    """
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ["model_id", "task", "labels"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for info in models_info:
            writer.writerow(info)

if __name__ == '__main__':
    all_models_info = []

    for task in tasks:
        print(f"Fetching models for task: {task}...")
        models = get_models(task)
        num_models = sum(1 for _ in models)
        print(f"...found {num_models} models for {task}")
        i = 1
        models = get_models(task)
        for model in models:
            info = get_model_info(model)
            all_models_info.append(info)
            print(f"{task}: {i}/{num_models} model saved.")
            i += 1

    print(f"Total models processed: {len(all_models_info)}")
    write_to_csv(all_models_info)
    print("Model data saved to huggingface_models.csv")
