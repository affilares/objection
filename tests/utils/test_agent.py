import os
import unittest
from unittest import mock

from objection.utils.agent import Agent


class TestAgent(unittest.TestCase):

    @unittest.skipUnless(os.path.exists('../objection/agent.js'), 'Requires compiled agent.')
    @mock.patch('objection.utils.agent.app_state')
    def test_agent_loads_from_disk_successfully_without_debug(self, mock_app_state):
        mock_app_state.should_debug.return_value = False

        agent = Agent()
        source = agent._get_agent_source()

        self.assertTrue(mock_app_state.should_debug.called)
        self.assertTrue('rpc.exports' in source)

    @unittest.skipUnless(os.path.exists('../objection/agent.js'), 'Requires compiled agent.')
    @mock.patch('objection.utils.agent.app_state')
    def test_agent_loads_from_disk_successfully_with_debug(self, mock_app_state):
        mock_app_state.should_debug.return_value = True

        agent = Agent()
        source = agent._get_agent_source()

        self.assertTrue(mock_app_state.should_debug.called)
        self.assertTrue('rpc.exports' in source)
        self.assertTrue('application/json;charset=utf-8;base64' in source.split(':')[-1])

    @mock.patch('objection.utils.agent.os')
    def test_agent_fails_to_load_throws_error(self, mock_os):
        mock_os.path.exists.return_value = False

        with self.assertRaises(Exception) as _:
            agent = Agent()
            agent._get_agent_source()
