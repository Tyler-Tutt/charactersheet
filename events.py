from enum import Enum

class PubSubTopic(str, Enum):
    """Allowed Values (Topics) of Event-channels (Radio Frequencies) for Flet's Pub/Sub system."""
    UI_ACTION = "ui_action"
    MODEL_UPDATED = "model_updated"
    EDIT_MODE_CHANGED = "edit_mode_changed"

class UIAction(str, Enum):
    """Allowed Actions that a View (UI) can request the Controller to perform."""
    UPDATE_HEADER = "update_header"
    TOGGLE_PROFICIENCY = "toggle_proficiency"
    UPDATE_ABILITY = "update_ability"
    ADD_ITEM = "add_item"
    TOGGLE_ATTUNEMENT = "toggle_attunement"