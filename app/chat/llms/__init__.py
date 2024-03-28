from functools import partial
from .chatopenai import build_llm

llm_registry = {
    "gtp-4": partial(build_llm, model_name="gpt-4"),
    "gtp-3.5-turbo": partial(build_llm, model_name="gpt-3.5-turbo")
}
