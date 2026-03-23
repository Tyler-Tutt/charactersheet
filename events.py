from enum import Enum

class PubSubTopic(str, Enum):
    """Event channels used for Flet's Pub/Sub system."""
    UI_ACTION = "ui_action"
    MODEL_UPDATED = "model_updated"
    EDIT_MODE_CHANGED = "edit_mode_changed"