from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
intents = ["DefinitionQuery", "ClauseRetrieval", "ComparativeAnalysis"]


def classify_intent(text):
    result = classifier(text, candidate_labels=intents)

    top_intent = result['labels'][0]
    confidence = result['scores'][0]

    print(f"\nUser Input: {text}")
    print(f"Predicted Intent: {top_intent}")
    print(f"Confidence Score: {confidence:.4f}")

    return top_intent, confidence
