from swarm.utils.file_utils import get_json_data

def get_default_action_tree():
    '''
    Get the default action tree.

    Returns:
        - action_tree (dict): The default action tree.
    '''
    return get_json_data('actions', 'action_space.json')

def get_default_memory_tree():
    '''
    Get the default memory tree.

    Returns:
        - memory_tree (dict): The default memory tree.
    '''
    return get_json_data('memory', 'memory_space.json')