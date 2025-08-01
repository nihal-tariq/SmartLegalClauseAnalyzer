from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Enhanced descriptive labels with clearer intent meaning
label_mapping = {
    "a request for the definition or meaning of a legal term or concept": "DefinitionQuery",
    "a request to locate, retrieve, or identify a specific clause in a legal document": "ClauseRetrieval",
    "a request to compare, contrast, or analyze two or more legal clauses or regulations": "ComparativeAnalysis"
}

# Descriptive labels used for classification
intents = list(label_mapping.keys())

# Prompt template to guide model
hypothesis_template = "The user's legal query is best categorized as {}."


def classify_intent(text):
    result = classifier(
        text,
        candidate_labels=intents,
        hypothesis_template=hypothesis_template
    )

    descriptive_label = result['labels'][0]
    confidence = result['scores'][0]

    # Map back to original intent name
    top_intent = label_mapping[descriptive_label]

    print(f"\nUser Input: {text}")
    print(f"Predicted Intent: {top_intent}")
    print(f"Confidence Score: {confidence:.4f}")

    return top_intent, confidence
