import json
import os
from typing import Dict, Optional, List, Any
import logging

logger = logging.getLogger(__name__)

MODES_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'agent', 'custom-modes.json')

_modes_cache: Optional[Dict[str, Dict[str, Any]]] = None

def load_modes() -> Dict[str, Dict[str, Any]]:
    """Loads custom mode definitions from the JSON file."""
    global _modes_cache
    if _modes_cache is not None:
        return _modes_cache

    try:
        if not os.path.exists(MODES_FILE_PATH):
            logger.warning(f"Custom modes file not found at {MODES_FILE_PATH}. No custom modes will be available.")
            _modes_cache = {}
            return _modes_cache

        with open(MODES_FILE_PATH, 'r') as f:
            data = json.load(f)
            modes_list = data.get("customModes", [])
            _modes_cache = {mode['slug']: mode for mode in modes_list if 'slug' in mode}
            logger.info(f"Loaded {len(_modes_cache)} custom modes.")
            return _modes_cache
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {MODES_FILE_PATH}. Invalid JSON format.", exc_info=True)
        _modes_cache = {}
        return _modes_cache
    except Exception as e:
        logger.error(f"Error loading custom modes from {MODES_FILE_PATH}: {e}", exc_info=True)
        _modes_cache = {}
        return _modes_cache

def get_mode_details(mode_slug: str) -> Optional[Dict[str, Any]]:
    """Retrieves the details for a specific mode slug."""
    modes = load_modes()
    return modes.get(mode_slug)

def get_all_modes() -> List[Dict[str, Any]]:
    """Returns a list of all loaded custom modes."""
    modes = load_modes()
    return list(modes.values())

# Pre-load modes on module import
load_modes()
