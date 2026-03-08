"""
Unit tests for Sarvam AI API request format verification
Tests Requirements 5.1-5.8 from multi-engine-ai-completion spec
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.services.ai_engine import MultiEngineAIClient, AIEngine


class TestSarvamAPIFormat:
    """Test suite for Sarvam AI API request format compliance"""
    
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
    
    def test_endpoint_url_correct(self, client):
        """
        Requirement 5.1: Verify endpoint URL is exactly 
        "https://api.sarvam.ai/v1/chat/completions"
        """
        assert AIEngine.SARVAM in client.engines
        config = client.engines[AIEngine.SARVAM]
        assert config['endpoint'] == 'https://api.sarvam.ai/v1/chat/completions'
    
    @patch('src.services.ai_engine.requests.post')
    def test_authorization_header_format(self, mock_post, client):
        """
        Requirement 5.2: Ensure Authorization header format is 
        "Bearer {api_key}" with space
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method
        client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify the call was made with correct headers
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Bearer test_api_key_123'
        assert headers['Authorization'].startswith('Bearer ')
        assert ' ' in headers['Authorization']  # Verify space after Bearer
    
    @patch('src.services.ai_engine.requests.post')
    def test_content_type_header(self, mock_post, client):
        """
        Requirement 5.3: Verify Content-Type header is "application/json"
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method
        client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify the call was made with correct headers
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        
        assert 'Content-Type' in headers
        assert headers['Content-Type'] == 'application/json'
    
    @patch('src.services.ai_engine.requests.post')
    def test_payload_required_fields(self, mock_post, client):
        """
        Requirement 5.4: Ensure payload includes all required fields: 
        model, messages, temperature, max_tokens
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method
        client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify the call was made with correct payload
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        assert 'model' in payload
        assert 'messages' in payload
        assert 'temperature' in payload
        assert 'max_tokens' in payload
        
        assert payload['model'] == 'sarvam-m'
        assert payload['temperature'] == 0.7
        assert payload['max_tokens'] == 4096
    
    @patch('src.services.ai_engine.requests.post')
    def test_messages_array_structure(self, mock_post, client):
        """
        Requirement 5.5: Verify messages array structure with role and content fields
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method
        client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify the call was made with correct message structure
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        messages = payload['messages']
        
        assert isinstance(messages, list)
        assert len(messages) >= 1
        
        for message in messages:
            assert 'role' in message
            assert 'content' in message
            assert isinstance(message['role'], str)
            assert isinstance(message['content'], str)
    
    @patch('src.services.ai_engine.requests.post')
    def test_system_instruction_message_order(self, mock_post, client):
        """
        Requirement 5.6: When system_instruction is provided, 
        add system message before user message
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method WITH system instruction
        client._generate_sarvam(
            'test prompt', 
            'You are a helpful assistant', 
            0.7
        )
        
        # Verify the call was made with correct message order
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        messages = payload['messages']
        
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[0]['content'] == 'You are a helpful assistant'
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == 'test prompt'
    
    @patch('src.services.ai_engine.requests.post')
    def test_no_system_instruction_single_message(self, mock_post, client):
        """
        Requirement 5.6 (variant): When system_instruction is NOT provided,
        only user message should be present
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method WITHOUT system instruction
        client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify the call was made with only user message
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        messages = payload['messages']
        
        assert len(messages) == 1
        assert messages[0]['role'] == 'user'
        assert messages[0]['content'] == 'test prompt'
    
    @patch('src.services.ai_engine.requests.post')
    def test_response_parsing_path(self, mock_post, client):
        """
        Requirement 5.8: Parse response from data['choices'][0]['message']['content']
        """
        # Mock successful response
        expected_text = 'This is the generated response'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': expected_text,
                        'role': 'assistant'
                    },
                    'finish_reason': 'stop'
                }
            ],
            'model': 'sarvam-m'
        }
        mock_post.return_value = mock_response
        
        # Call the method
        result = client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify response parsing
        assert result['success'] is True
        assert result['text'] == expected_text
        assert result['content'] == expected_text
        assert result['model'] == 'sarvam-m'
        assert result['engine'] == 'sarvam'
    
    @patch('src.services.ai_engine.requests.post')
    def test_complete_request_format_integration(self, mock_post, client):
        """
        Integration test: Verify complete request format with all requirements
        Requirements 5.1-5.7 combined
        """
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'test response'}}]
        }
        mock_post.return_value = mock_response
        
        # Call the method with all parameters
        client._generate_sarvam(
            prompt='Generate a blog post',
            system_instruction='You are a content writer',
            temperature=0.8
        )
        
        # Verify the complete request
        call_args = mock_post.call_args
        
        # Verify endpoint (5.1)
        assert call_args[0][0] == 'https://api.sarvam.ai/v1/chat/completions'
        
        # Verify headers (5.2, 5.3)
        headers = call_args[1]['headers']
        assert headers['Authorization'] == 'Bearer test_api_key_123'
        assert headers['Content-Type'] == 'application/json'
        
        # Verify payload (5.4, 5.5, 5.6)
        payload = call_args[1]['json']
        assert payload['model'] == 'sarvam-m'
        assert payload['temperature'] == 0.8
        assert payload['max_tokens'] == 4096
        assert len(payload['messages']) == 2
        assert payload['messages'][0] == {
            'role': 'system',
            'content': 'You are a content writer'
        }
        assert payload['messages'][1] == {
            'role': 'user',
            'content': 'Generate a blog post'
        }
        
        # Verify timeout
        assert call_args[1]['timeout'] == 30


class TestSarvamErrorHandling:
    """Test suite for Sarvam AI error handling"""
    
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
    def test_http_error_with_json_response(self, mock_logger, mock_post, client):
        """
        Requirement 1.2, 1.5, 6.3: Test error logging with JSON error response
        """
        import requests
        
        # Mock HTTP error with JSON response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'error': {
                'message': 'Invalid request format',
                'type': 'invalid_request_error'
            }
        }
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 400')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify error logging
        assert 'Sarvam AI HTTP 400' in str(exc_info.value)
    
    @patch('src.services.ai_engine.requests.post')
    @patch('src.services.ai_engine.logger')
    def test_http_error_with_text_response(self, mock_logger, mock_post, client):
        """
        Requirement 6.4: Test error logging with non-JSON error response
        """
        import requests
        
        # Mock HTTP error with text response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError('Not JSON')
        mock_response.text = 'Internal Server Error'
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP 500')
        mock_post.return_value = mock_response
        
        # Call should raise exception
        with pytest.raises(Exception) as exc_info:
            client._generate_sarvam('test prompt', None, 0.7)
        
        # Verify error contains status code and text
        assert 'Sarvam AI HTTP 500' in str(exc_info.value)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
