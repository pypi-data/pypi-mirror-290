from generators import KnowledgeBase, generate_testset
import pandas as pd

# Load your data and initialize the KnowledgeBase
df = pd.read_csv("addresses.csv")

knowledge_base = KnowledgeBase.from_pandas(df)
knowledge_base.get_knowledge_plot()

testset = generate_testset(
    knowledge_base, 
    num_questions=10,
    agent_description="A customer support chatbot for company X", # helps generating better questions
)

testset.save("my_testset.jsonl")