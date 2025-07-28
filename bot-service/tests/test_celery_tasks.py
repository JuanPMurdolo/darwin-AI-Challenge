import unittest
from unittest.mock import patch, MagicMock, AsyncMock

class TestCeleryTasks(unittest.TestCase):

    def test_run_analytics_task_direct_call(self):
        """Test that we can import the task function without connecting to Redis"""
        from app.tasks.analytics import run_analytics_task
        
        assert hasattr(run_analytics_task, 'delay')
        assert hasattr(run_analytics_task, 'apply_async')
        
        assert run_analytics_task.name == "run_analytics_task"
