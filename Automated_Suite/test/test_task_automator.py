import unittest
from task_automator import sched
from unittest.mock import patch
from apscheduler.schedulers.blocking import BlockingScheduler

class TestTaskAutomator(unittest.TestCase):

    @patch('apscheduler.schedulers.blocking.BlockingScheduler.start')
    def test_task_automator_success(self, mock_start):
        sched.start()
        mock_start.assert_called_once()

    @patch('apscheduler.schedulers.blocking.BlockingScheduler.start')
    def test_task_automator_failure(self, mock_start):
        mock_start.side_effect = Exception
        sched.start()
        mock_start.assert_called_once()

if __name__ == "__main__":
    unittest.main()