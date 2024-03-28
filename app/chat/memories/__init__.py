from .sql_memory import build_memory
from .window_memory import window_bufer_memory_builder

memory_registry = {
    "sql_buffer": build_memory,
    "sql_window_buffer": window_bufer_memory_builder
}
