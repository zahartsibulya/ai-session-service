PRICING_RATES = {
    "gpt-4o-mini": {
        "input_price_per_1k": 0.00015,
        "output_price_per_1k": 0.00060,
    }
}

def calculate_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    rates = PRICING_RATES.get(model_name)
    if not rates:
        return 0.0 
    
    input_cost = (prompt_tokens / 1000) * rates["input_price_per_1k"]
    output_cost = (completion_tokens / 1000) * rates["output_price_per_1k"]
    return input_cost + output_cost
