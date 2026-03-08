"""
Verification test for Task 2.1: Add engine parameter to _generate_gemini method

This test verifies that the _generate_gemini method now accepts an engine parameter
and correctly routes to the specified Gemini engine (Engine 1 or Engine 3).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.ai_engine import MultiEngineAIClient, AIEngine


def test_generate_gemini_accepts_engine_parameter():
    """Verify _generate_gemini method accepts engine parameter"""
    # Create a mock client
    with patch('src.services.ai_engine.genai') as mock_genai:
        # Setup mock client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client
        
        # Create AI client with mocked environment
        with patch.dict('os.environ', {
            'GEMINI_API_KEY': 'test_key_1',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_ENGINE3': 'test_key_3',
            'GEMINI_MODEL_ENGINE3': 'gemini-2.0-flash'
        }):
            ai_client = MultiEngineAIClient()
            
            # Verify both engines are initialized
            assert AIEngine.GEMINI in ai_client.engines
            assert AIEngine.GEMINI3 in ai_client.engines
            
            # Test calling _generate_gemini with AIEngine.GEMINI
            result1 = ai_client._generate_gemini(
                prompt="Test prompt",
                system_instruction="Test instruction",
                temperature=0.7,
                engine=AIEngine.GEMINI
            )
            
            assert result1['success'] is True
            assert result1['text'] == "Test response"
            assert result1['engine'] == 'gemini'
            
            # Test calling _generate_gemini with AIEngine.GEMINI3
            result2 = ai_client._generate_gemini(
                prompt="Test prompt",
                system_instruction="Test instruction",
                temperature=0.7,
                engine=AIEngine.GEMINI3
            )
            
            assert result2['success'] is True
            assert result2['text'] == "Test response"
            assert result2['engine'] == 'gemini'


def test_generate_gemini_uses_correct_client_for_engine():
    """Verify _generate_gemini uses the correct client based on engine parameter"""
    with patch('src.services.ai_engine.genai') as mock_genai:
        # Create two different mock clients
        mock_client_1 = Mock()
        mock_client_3 = Mock()
        
        mock_response_1 = Mock()
        mock_response_1.text = "Response from Engine 1"
        mock_client_1.models.generate_content.return_value = mock_response_1
        
        mock_response_3 = Mock()
        mock_response_3.text = "Response from Engine 3"
        mock_client_3.models.generate_content.return_value = mock_response_3
        
        # Setup genai.Client to return different clients
        def client_side_effect(api_key):
            if api_key == 'test_key_1':
                return mock_client_1
            elif api_key == 'test_key_3':
                return mock_client_3
            return Mock()
        
        mock_genai.Client.side_effect = client_side_effect
        
        with patch.dict('os.environ', {
            'GEMINI_API_KEY': 'test_key_1',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_ENGINE3': 'test_key_3',
            'GEMINI_MODEL_ENGINE3': 'gemini-2.0-flash'
        }):
            ai_client = MultiEngineAIClient()
            
            # Call with Engine 1
            result1 = ai_client._generate_gemini(
                prompt="Test",
                system_instruction=None,
                temperature=0.7,
                engine=AIEngine.GEMINI
            )
            
            # Verify Engine 1 client was used
            assert result1['text'] == "Response from Engine 1"
            assert mock_client_1.models.generate_content.called
            
            # Call with Engine 3
            result3 = ai_client._generate_gemini(
                prompt="Test",
                system_instruction=None,
                temperature=0.7,
                engine=AIEngine.GEMINI3
            )
            
            # Verify Engine 3 client was used
            assert result3['text'] == "Response from Engine 3"
            assert mock_client_3.models.generate_content.called


def test_generate_content_passes_engine_parameter():
    """Verify generate_content passes the correct engine parameter to _generate_gemini"""
    with patch('src.services.ai_engine.genai') as mock_genai:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client
        
        with patch.dict('os.environ', {
            'GEMINI_API_KEY': 'test_key_1',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_ENGINE3': 'test_key_3',
            'GEMINI_MODEL_ENGINE3': 'gemini-2.0-flash'
        }):
            ai_client = MultiEngineAIClient()
            
            # Mock _generate_gemini to track calls
            original_generate_gemini = ai_client._generate_gemini
            call_tracker = []
            
            def tracked_generate_gemini(prompt, system_instruction, temperature, engine):
                call_tracker.append(engine)
                return original_generate_gemini(prompt, system_instruction, temperature, engine)
            
            ai_client._generate_gemini = tracked_generate_gemini
            
            # Call generate_content (should use GEMINI first)
            result = ai_client.generate_content(
                prompt="Test prompt",
                system_instruction="Test instruction",
                temperature=0.7
            )
            
            # Verify the engine parameter was passed
            assert len(call_tracker) > 0
            assert call_tracker[0] == AIEngine.GEMINI
            assert result['engine_used'] == 'gemini'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
