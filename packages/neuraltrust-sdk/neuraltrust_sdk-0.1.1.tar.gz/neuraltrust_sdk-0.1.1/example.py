import os

from api_keys.neuraltrust_api_key import NeuralTrustApiKey
from api_keys.openai_api_key import OpenAiApiKey
from evals.evaluation_set import EvaluationSet
from generators import KnowledgeBase
import pandas as pd

NeuralTrustApiKey.set_key(os.getenv('NEURALTRUST_API_KEY'))
OpenAiApiKey.set_key(os.getenv('OPENAI_API_KEY'))


df = pd.read_csv("addresses.csv")
knowledge_base = KnowledgeBase.from_pandas(df)

eval = EvaluationSet(
    id="addresses_eval_45bc15",
    # name='addresses eval', 
    # description='evaluating addresses', 
    # system_prompt="You are a chatbot that answers questions about a addresses", 
    # scheduler="0 0 * * *",
    # testset_id="none_testset_ga32kv",
    create_testset=True, 
    num_questions=5,
    knowledge_base=knowledge_base
)

eval.run()