import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def score_answer(expected: str, actual: str) -> float:
    llm = ChatOpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["expected", "actual"],
        template="""You are an impartial judge. Evaluate if the actual answer matches the core fact of the expected answer.
Expected: {expected}
Actual: {actual}
Respond with only '1' if it substantially matches, or '0' if it doesn't match or is incorrect/missing."""
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        response = chain.run(expected=expected, actual=actual).strip()
        return float(response)
    except Exception:
        return 0.0
