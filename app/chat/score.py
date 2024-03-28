import random
from app.chat.redis import client


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(f"Scoring conversation {conversation_id} with score {score}")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)


def weighted_random_component_by_score(component_type: str, component_registry: dict[str, str]) -> str:
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError(f"Invalid component type: {component_type}")

    values = client.hgetall(f"{component_type}_score_values")
    counts = client.hgetall(f"{component_type}_score_counts")
    names = component_registry.keys()

    means_scores = {}
    for name in names:
        means_scores[name] = max(
            int(values.get(name, 1)) / int(counts.get(name, 1)), 0.1)

    total = sum(means_scores.values())
    random_value = random.uniform(0, total)
    accumulator = 0
    for name, score in means_scores.items():
        accumulator += score
        if accumulator >= random_value:
            return name


def get_scores():
    aggregate_scores = {
        "llm": {},
        "retriever": {},
        "memory": {}
    }

    for component_type in aggregate_scores.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        for name in values.keys():
            aggregate_scores[component_type][name] = [
                int(values.get(name, 1)) / int(counts.get(name, 1))]

    return aggregate_scores
