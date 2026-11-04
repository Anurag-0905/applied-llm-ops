import os 
from dotenv import load_dotenv
from langchain.messages import HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

load_dotenv(override=True)

def llm():
    return ChatOpenAI(model=os.environ["MODEL"], base_url=os.environ["BASE_URL"],
                 api_key=os.environ["API_KEY"], temperature=0, max_tokens=1500)

SYSTEM = ("You are BankAssist, NorthWind Bank's assistant. Branches are open 10am to 4pm Monday to Friday" 
          "and 10am to 1pm on Saturdays. Homeloan rates: 8.5% floating 9% fixed. Answer in 2-3 sentences.")
def chain(llm):
    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM), ("human", "{question}")])
    return prompt | llm | StrOutputParser()

RATE_CARD = {
    ("home_loan", "floating"): 8.5,
    ("home_loan", "fixed"): 9.0,
    ("personal_loan", "fixed"): 10.5,
}
FOIR_LIMIT = 0.50

@tool(parse_docstring=True)
def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> int:
    """Exact monthly EMI for a loan. Use only when customer asks for its purpose.

    Args:
        principal (float): The loan amount.
        annual_rate (float): Annual interest rate in percentage.
        tenure_months (int): Loan tenure in months (e.g., 240).
    """
    r = annual_rate / 12 / 100
    n = tenure_months
    return round(principal * r * (1 + r) ** n / ((1 + r) ** n - 1))

@tool(parse_docstring=True)
def get_rate(product: str, rate_type: str):
    """Rates from RATE_CARD. Use only when customer asks for its purpose.

    Args:
        product (str): The loan product, e.g., 'home_loan'.
        rate_type (str): The type of rate, e.g., 'floating' or 'fixed'.
    """
    rate = RATE_CARD.get((product, rate_type))
    if rate is None:
        have = ", ".join(f"{p} {t}" for p, t in RATE_CARD)
        raise ValueError(f"no rate for {product} {rate_type}; the card has: {have}")
    return rate


@tool(parse_docstring=True)
def check_eligibility(monthly_income: float, existing_emi: float, proposed_emi: float):
    """FOIR rule: (existing + proposed EMI) / monthly income must be at most FOIR_LIMIT.

    Args:
        monthly_income (float): The customer's monthly income.
        existing_emi (float): The customer's existing EMI.
        proposed_emi (float): The proposed EMI.
    """
    foir = (existing_emi + proposed_emi) / monthly_income
    return {"foir": round(foir, 3), "limit": FOIR_LIMIT, "eligible": foir <= FOIR_LIMIT}

TOOLS = {"calculate_emi": calculate_emi, "get_rate": get_rate, "check_eligibility": check_eligibility}

def ask(llm_with_tools, question: str, x_steps: int = 3) -> str:
    messages = [SystemMessage(SYSTEM), HumanMessage(question)]
    
    for step in range(1, x_steps + 1):
        ai = llm_with_tools.invoke(messages)
        messages.append(ai)
        
        if not ai.tool_calls:              # the model answered in words - we are done
            return ai.content
            
        for call in ai.tool_calls:         # call["name"], call["args"] (a dict), call["id"]
            print(f"  step {step}: {call['name']}({call['args']})")
            messages.append(TOOLS[call["name"]].invoke(call))   # returns a ToolMessage with the SAME id
            
    return "(stopped: step cap reached)"
# -------------------------------------------------------------------------------------------- testing the chain and tools
def _step(n, fn):
    try:
        print(f"STEP {n}:", fn())
    except NotImplementedError as e:
        print(f"STEP {n}: not done yet ({e})")
        return False
    return True


def main():
    state = {}

    def s1():
        state["llm"] = llm()
        return state["llm"].invoke("Say hello in five words.").content

    def s2():
        return chain(state["llm"]).invoke({"question": "What are your branch timings on Saturday?"})

    def s3():
        emi = calculate_emi.invoke({"principal": 2500000, "annual_rate": 8.5, "tenure_months": 240})
        return f"{emi}   {'OK' if emi == 21696 else 'WRONG - expected 21696'}"

    def s4():
        return ask(state["llm"].bind_tools(list(TOOLS.values())),
                   "What is the EMI on a 25 lakh home loan at 8.5% for 20 years?")

    def s5():
        if "get_rate" not in TOOLS:
            raise NotImplementedError("TODO 5, optional stretch")
        return ask(state["llm"].bind_tools(list(TOOLS.values())),
                   "What would my EMI be on a 30 lakh home loan at your floating rate, over 15 years?")

    if _step(1, s1):
        _step(2, s2)
    _step(3, s3)
    if "llm" in state:
        _step(4, s4)
        _step(5, s5)


if __name__ == "__main__":
    main()
