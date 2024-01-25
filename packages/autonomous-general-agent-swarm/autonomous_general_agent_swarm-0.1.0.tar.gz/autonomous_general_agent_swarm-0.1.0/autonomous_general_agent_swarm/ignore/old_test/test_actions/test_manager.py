import sys
import pytest
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from old_swarm.utils.actions.executor import execute_node
from old_swarm.core.node import Node
import asyncio

@pytest.mark.unit_test_actions
async def test_manager():
    node = Node(id=5, type='manager', data={'directive': "We need to automate real estate agents"})
    result = await execute_node(node)
    print(result)

# Run the main function
asyncio.run(test_manager())