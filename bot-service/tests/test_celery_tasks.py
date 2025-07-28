import unittest
from unittest.mock import patch, MagicMock, AsyncMock

class TestCeleryTasks(unittest.TestCase):

    def test_run_analytics_task_direct_call(self):
        """Test that we can import the task function without connecting to Redis"""
        # Just test that the function exists and can be imported
        from app.tasks.analytics import run_analytics_task
        
        # Test that it's a Celery task
        assert hasattr(run_analytics_task, 'delay')
        assert hasattr(run_analytics_task, 'apply_async')
        
        # Test that the function name is correct
        assert run_analytics_task.name == "run_analytics_task"
