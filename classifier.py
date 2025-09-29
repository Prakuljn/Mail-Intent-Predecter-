from transformers import pipeline

INTENTS = ["User Manual", "Product Info", "Installation"]

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def classify_email(text: str):
    result = classifier(text, INTENTS, multi_label=True)
    predictions = list(zip(result["labels"], result["scores"]))
    return predictions

def detect_intents(predictions, threshold=0.6):
    intents = [label for label, score in predictions if score >= threshold]
    if not intents:
        intents = [max(predictions, key=lambda x: x[1])[0]]
    return intents
