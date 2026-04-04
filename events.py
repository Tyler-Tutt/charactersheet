from enum import StrEnum

class PubSubTopic(StrEnum):
    """Allowed values of Topics for Event-channels (Radio Frequencies) of Flet's PubSub system.
    Flet passes 2 things for a PubSub: Topic & Message. This is the TOPIC.
    """
    UI_ACTION = "ui_action"
    MODEL_UPDATED = "model_updated"
    EDIT_MODE_CHANGED = "edit_mode_changed"

class UIAction(StrEnum):
    """Allowed values of Actions that a View (UI) can request the Controller to perform.
    Flet passes 2 things for a PubSub: Topic & Message. This is the 'action' within the MESSAGE (The Message is a dictionary).
    """
    UPDATE_HEADER = "update_header"
    TOGGLE_PROFICIENCY = "toggle_proficiency"
    UPDATE_ABILITY = "update_ability"
    ADD_ITEM = "add_item"
    TOGGLE_ATTUNEMENT = "toggle_attunement"