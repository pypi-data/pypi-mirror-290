from neuraltrust import (
    RagasContextRelevancy, RagasAnswerRelevancy, RagasAnswerCorrectness, 
    RagasAnswerSemanticSimilarity, RagasCoherence, RagasConciseness, 
    RagasContextPrecision, RagasContextRecall, RagasFaithfulness, 
    RagasHarmfulness, RagasMaliciousness
)
from neuraltrust.grounded.similarity import (
    CosineSimilarity, JaccardSimilarity, JaroWincklerSimilarity, 
    NormalisedLevenshteinSimilarity, SorensenDiceSimilarity
)
from neuraltrust.grounded.wrapper import AnswerSimilarity, ContextSimilarity

grounded_operations = {
    "AnswerSimilarity": AnswerSimilarity,
    "ContextSimilarity": ContextSimilarity,
}

ragas_operations = {
    "RagasContextRelevancy": RagasContextRelevancy,
    "RagasAnswerRelevancy": RagasAnswerRelevancy,
    "RagasAnswerCorrectness": RagasAnswerCorrectness,
    "RagasAnswerSemanticSimilarity": RagasAnswerSemanticSimilarity,
    "RagasCoherence": RagasCoherence,
    "RagasConciseness": RagasConciseness,
    "RagasContextPrecision": RagasContextPrecision,
    "RagasContextRecall": RagasContextRecall,
    "RagasFaithfulness": RagasFaithfulness,
    "RagasHarmfulness": RagasHarmfulness,
    "RagasMaliciousness": RagasMaliciousness
}

def get_evaluator(evaluator_type):
    if evaluator_type in grounded_operations:
        return grounded_operations[evaluator_type]
    elif evaluator_type in ragas_operations:
        return ragas_operations[evaluator_type]
    else:
        raise ValueError(f"Invalid evaluator type: {evaluator_type}")

def get_comparator(comparator_name):
    if comparator_name is None:
        raise ValueError("similarity_function is a required argument")
    comparators = {
        "CosineSimilarity": CosineSimilarity(),
        "NormalisedLevenshteinSimilarity": NormalisedLevenshteinSimilarity(),
        "JaroWincklerSimilarity": JaroWincklerSimilarity(),
        "JaccardSimilarity": JaccardSimilarity(),
        "SorensenDiceSimilarity": SorensenDiceSimilarity()
    }
    comparator = comparators.get(comparator_name, None)
    if comparator is None:
        raise NotImplementedError(f"Comparator {comparator_name} not implemented.")
    return comparator

def create_grounded_evaluator(grounded_eval_name, comparator, failure_threshold):
    grounded_evaluator_class = grounded_operations.get(grounded_eval_name, None)
    if grounded_evaluator_class is None:
        raise NotImplementedError(f"Grounded eval {grounded_eval_name} not implemented.")
    return grounded_evaluator_class(comparator=comparator, failure_threshold=failure_threshold)