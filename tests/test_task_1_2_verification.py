"""
Verification tests for Task 1.2: Enhance Sarvam AI error logging
Tests all sub-tasks explicitly:
- Catch requests.exceptions.HTTPError
- Attempt to parse JSON error response
- Log JSON error response if parsing succeeds
- Fall back to logging raw response text if JSON parsing fails
- Include HTTP status code in all error messages
"""

import pytest
from unittest.mock import Mock, patch
import requests
from src.services.ai_engine import MultiEngineAIClient, AIEngine


class TestTask1_2ErrorLogging:
    """Verification tests for Task 1.2 sub-tasks"""
    
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Set up mock environment variables"""
        monkeypatch.setenv('SARVAM_API_KEY', 'test_api_key_123')
        monkeypatch.setenv('SARVAM_MODEL', 'sarvam-m')
        monkeypatch.setenv('GEMINI_API_KEY', 'test_gemini_key')
        
    @pytest.fixture
    def client(self, mock_env):
        """Create a MultiEngineAIClient instance with mocked environment"""
        with patch('src.services.ai_engine.genai'):
            return MultiEngineAIClient()
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_1_catch_http_error(self, mock_logger, mock_post, client):
        """
        Sub-task 1: Verify that requests.exceptions.HTTPError is caught
        """
        # Mock HTTP error
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 400')
        mock_post.return_value = mock_response
        
        # Should catch HTTPError and raise our custom exception
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify it's our custom exception, not the raw HTTPError
        assert 'Sarvam AI HTTP' in str(exc_info.value)
        assert '400' in str(exc_info.value)
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_2_attempt_json_parsing(self, mock_logger, mock_post, client):
        """
        Sub-task 2: Verify that JSON error response parsing is attempted
        """
        # Mock HTTP error with JSON response
        mock_response = Mock()
        mock_response.status_code = 400
        error_json = {
            'error': {
                'message': 'Invalid request format',
                'type': 'invalid_request_error',
                'code': 'bad_request'
            }
        }
        mock_response.json.return_value = error_json
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 400')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception):
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify json() was called (attempt to parse)
        assert mock_response.json.called
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_3_log_json_error_response(self, mock_logger, mock_post, client):
        """
        Sub-task 3: Verify that JSON error response is logged if parsing succeeds
        """
        # Mock HTTP error with JSON response
        mock_response = Mock()
        mock_response.status_code = 400
        error_json = {
            'error': {
                'message': 'Invalid request format',
                'type': 'invalid_request_error'
            }
        }
        mock_response.json.return_value = error_json
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 400')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception):
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify logger.error was called with JSON error response
        error_calls = [call for call in mock_logger.error.call_args_list]
        assert len(error_calls) >= 1
        
        # Check that the error response was logged
        logged_messages = [str(call[0][0]) for call in error_calls]
        assert any('Sarvam AI error response' in msg for msg in logged_messages)
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_4_fallback_to_raw_text(self, mock_logger, mock_post, client):
        """
        Sub-task 4: Verify fallback to logging raw response text if JSON parsing fails
        """
        # Mock HTTP error with non-JSON response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError('Not valid JSON')
        mock_response.text = 'Internal Server Error - Service Unavailable'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 500')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception):
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify logger.error was called with raw text
        error_calls = [call for call in mock_logger.error.call_args_list]
        assert len(error_calls) >= 1
        
        # Check that the raw text was logged
        logged_messages = [str(call[0][0]) for call in error_calls]
        assert any('Sarvam AI error text' in msg for msg in logged_messages)
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_5_include_status_code_json_error(self, mock_logger, mock_post, client):
        """
        Sub-task 5a: Verify HTTP status code is included in error messages (JSON case)
        """
        # Mock HTTP error with JSON response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 401')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify status code is in the exception message
        error_message = str(exc_info.value)
        assert 'Sarvam AI HTTP 401' in error_message
        assert '401' in error_message
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_subtask_5_include_status_code_text_error(self, mock_logger, mock_post, client):
        """
        Sub-task 5b: Verify HTTP status code is included in error messages (text case)
        """
        # Mock HTTP error with text response
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.json.side_effect = ValueError('Not JSON')
        mock_response.text = 'Service Unavailable'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 503')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify status code is in the exception message
        error_message = str(exc_info.value)
        assert 'Sarvam AI HTTP 503' in error_message
        assert '503' in error_message
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_all_subtasks_integration(self, mock_logger, mock_post, client):
        """
        Integration test: Verify all sub-tasks work together
        """
        # Test with JSON error
        mock_response = Mock()
        mock_response.status_code = 400
        error_json = {'error': {'message': 'Bad Request', 'code': 'invalid_format'}}
        mock_response.json.return_value = error_json
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 400')
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify all requirements:
        # 1. HTTPError was caught (we got our custom exception)
        assert 'Sarvam AI HTTP' in str(exc_info.value)
        
        # 2. JSON parsing was attempted
        assert mock_response.json.called
        
        # 3. JSON error was logged
        error_calls = [str(call[0][0]) for call in mock_logger.error.call_args_list]
        assert any('Sarvam AI error response' in msg for msg in error_calls)
        
        # 4. Status code is included
        assert '400' in str(exc_info.value)
        
        # Reset mocks for text error test
        mock_logger.reset_mock()
        mock_post.reset_mock()
        
        # Test with text error
        mock_response2 = Mock()
        mock_response2.status_code = 500
        mock_response2.json.side_effect = ValueError('Not JSON')
        mock_response2.text = 'Internal Server Error'
        mock_response2.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 500')
        mock_post.return_value = mock_response2
        
        with pytest.raises(Exception) as exc_info2:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify fallback to text:
        # 1. HTTPError was caught
        assert 'Sarvam AI HTTP' in str(exc_info2.value)
        
        # 2. JSON parsing was attempted (and failed)
        assert mock_response2.json.called
        
        # 3. Raw text was logged
        error_calls2 = [str(call[0][0]) for call in mock_logger.error.call_args_list]
        assert any('Sarvam AI error text' in msg for msg in error_calls2)
        
        # 4. Status code is included
        assert '500' in str(exc_info2.value)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
