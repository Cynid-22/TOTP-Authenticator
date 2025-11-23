import ctypes
import sys

def secure_wipe_string(string_value):
    """
    Securely wipe a string from memory using ctypes.
    This overwrites the memory location with zeros before deletion.
    
    Note: Python strings are immutable, so this only works for the address
    of the string object, not all copies that may have been made.
    """
    if string_value is None:
        return
    
    try:
        # Get the address of the string object
        address = id(string_value)
        size = sys.getsizeof(string_value)
        
        # Overwrite memory with zeros
        ctypes.memset(address, 0, size)
    except Exception:
        # If wiping fails, continue silently
        # (Better to continue than crash)
        pass

def secure_wipe_list(list_value):
    """
    Securely wipe a list and its contents from memory.
    """
    if list_value is None or not isinstance(list_value, list):
        return
    
    try:
        # Wipe each item in the list
        for item in list_value:
            if isinstance(item, str):
                secure_wipe_string(item)
            elif isinstance(item, dict):
                secure_wipe_dict(item)
        
        # Clear the list
        list_value.clear()
        
        # Wipe the list object itself
        address = id(list_value)
        size = sys.getsizeof(list_value)
        ctypes.memset(address, 0, size)
    except Exception:
        pass

def secure_wipe_dict(dict_value):
    """
    Securely wipe a dictionary and its contents from memory.
    """
    if dict_value is None or not isinstance(dict_value, dict):
        return
    
    try:
        # Wipe each key and value
        for key, value in list(dict_value.items()):
            if isinstance(value, str):
                secure_wipe_string(value)
            elif isinstance(value, list):
                secure_wipe_list(value)
            elif isinstance(value, dict):
                secure_wipe_dict(value)
        
        # Clear the dictionary
        dict_value.clear()
        
        # Wipe the dict object itself
        address = id(dict_value)
        size = sys.getsizeof(dict_value)
        ctypes.memset(address, 0, size)
    except Exception:
        pass
