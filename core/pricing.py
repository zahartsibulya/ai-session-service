PRICING = {
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.00060},
    "gpt-4o": {"prompt": 0.00250, "completion": 0.01000},
    "gpt-3.5-turbo": {"prompt": 0.00050, "completion": 0.00150}
}

def is_model_supported(model_name: str) -> bool:
    return model_name in PRICING

def calculate_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    rates = PRICING.get(model_name)
    if not rates:
        return 0.0 
    
    input_cost = (prompt_tokens / 1000) * rates["input_price_per_1k"]
    output_cost = (completion_tokens / 1000) * rates["output_price_per_1k"]
    return input_cost + output_cost
