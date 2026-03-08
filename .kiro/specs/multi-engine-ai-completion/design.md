# Design Document: Multi-Engine AI Completion

## Overview

This design addresses two critical issues preventing full functionality of the multi-engine AI system in the Ashoka platform:

1. **Sarvam AI 400 Error**: The Sarvam AI engine returns HTTP 400 Bad Request errors due to incorrect API request format
2. **Incomplete Gemini Engine 3**: The backup Gemini engine cannot be used because the `_generate_gemini` method lacks an engine parameter to differentiate between Gemini Engine 1 and Engine 3

The system implements a three-tier fallback architecture: Gemini (primary) → Sarvam AI (secondary) → Gemini Engine 3 (tertiary). When one engine fails, the system automatically attempts the next available engine, ensuring high availability for AI-powered content generation.

### Design Goals

- Fix Sarvam AI request format to match API specification
- Enable Gemini Engine 3 as a functional backup engine
- Maintain backward compatibility with existing code
- Provide comprehensive error logging for debugging
- Ensure seamless fallback between all three engines

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                   MultiEngineAIClient                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Engine Initialization Layer               │    │
│  │  _init_gemini()  _init_sarvam()  _init_gemini3()  │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Engine Registry                        │    │
│  │  engines = {                                        │    │
│  │    AIEngine.GEMINI: {client, model, type}          │    │
│  │    AIEngine.SARVAM: {api_key, model, endpoint}     │    │
│  │    AIEngine.GEMINI3: {client, model, type}         │    │
│  │  }                                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Generation Orchestration                  │    │
│  │         generate_content(prompt, ...)               │    │
│  │                                                      │    │
│  │  For each engine in priority order:                │    │
│  │    1. Check if engine is available                 │    │
│  │    2. Route to appropriate generator               │    │
│  │    3. Return on success                            │    │
│  │    4. Log and continue on failure                  │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │            Engine-Specific Generators               │    │
│  │                                                      │    │
│  │  _generate_gemini(prompt, ..., engine)             │    │
│  │    ├─ Routes to Gemini Engine 1 or 3               │    │
│  │    └─ Uses google-genai SDK                        │    │
│  │                                                      │    │
│  │  _generate_sarvam(prompt, ...)                     │    │
│  │    ├─ Formats request per Sarvam API spec          │    │
│  │    └─ Uses requests library                        │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Fallback Flow

```
User Request
     │
     ▼
┌─────────────────┐
│ generate_content│
└────────┬────────┘
         │
         ▼
    ┌────────────────────┐
    │ Try Gemini Engine 1│
    └────────┬───────────┘
             │
        Success? ──Yes──> Return Result
             │
            No
             │
             ▼
    ┌────────────────────┐
    │ Try Sarvam AI      │
    └────────┬───────────┘
             │
        Success? ──Yes──> Return Result
             │
            No
             │
             ▼
    ┌────────────────────┐
    │ Try Gemini Engine 3│
    └────────┬───────────┘
             │
        Success? ──Yes──> Return Result
             │
            No
             │
             ▼
    ┌────────────────────┐
    │ Raise Exception    │
    │ (All engines failed)│
    └────────────────────┘
```

## Components and Interfaces

### 1. MultiEngineAIClient

The main orchestrator class that manages multiple AI engines and handles fallback logic.

**Key Responsibilities:**
- Initialize available AI engines
- Maintain engine registry and priority order
- Route requests to appropriate engines
- Handle fallback logic
- Aggregate error information

**Public Interface:**

```python
class MultiEngineAIClient:
    def __init__(self):
        """Initialize all available AI engines"""
        
    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        preferred_engine: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate content using available engines with fallback
        
        Returns:
            {
                'success': True,
                'text': str,
                'content': str,
                'model': str,
                'engine': str,
                'engine_used': str
            }
        """
        
    def is_available(self) -> bool:
        """Check if any engine is available"""
        
    def get_available_engines(self) -> List[str]:
        """Get list of available engine names"""
```

### 2. Engine Initialization Methods

Each engine has a dedicated initialization method that sets up the client and stores configuration.

**_init_gemini() - Gemini Engine 1**

```python
def _init_gemini(self):
    """
    Initialize primary Gemini engine
    
    Environment Variables:
        GEMINI_API_KEY: API key for Gemini
        GEMINI_MODEL: Model name (default: gemini-2.0-flash)
    
    Stores in engines[AIEngine.GEMINI]:
        - client: genai.Client instance
        - model: model name
        - type: 'gemini'
    """
```

**_init_sarvam() - Sarvam AI Engine**

```python
def _init_sarvam(self):
    """
    Initialize Sarvam AI engine
    
    Environment Variables:
        SARVAM_API_KEY: API key for Sarvam AI
        SARVAM_MODEL: Model name (default: sarvam-m)
    
    Stores in engines[AIEngine.SARVAM]:
        - api_key: API key
        - model: model name
        - type: 'sarvam'
        - endpoint: 'https://api.sarvam.ai/v1/chat/completions'
    """
```

**_init_gemini3() - Gemini Engine 3 (Backup)**

```python
def _init_gemini3(self):
    """
    Initialize backup Gemini engine
    
    Environment Variables:
        GEMINI_ENGINE3: API key for backup Gemini
        GEMINI_MODEL_ENGINE3: Model name (default: gemini-2.0-flash)
    
    Stores in engines[AIEngine.GEMINI3]:
        - client: genai.Client instance
        - model: model name
        - type: 'gemini'
    """
```

### 3. Engine-Specific Generators

**_generate_gemini() - Modified to Support Both Gemini Engines**

```python
def _generate_gemini(
    self,
    prompt: str,
    system_instruction: Optional[str],
    temperature: float,
    engine: AIEngine  # NEW PARAMETER
) -> Dict[str, Any]:
    """
    Generate content using Gemini (Engine 1 or Engine 3)
    
    Args:
        prompt: User prompt
        system_instruction: Optional system instruction
        temperature: Sampling temperature
        engine: Which Gemini engine to use (AIEngine.GEMINI or AIEngine.GEMINI3)
    
    Returns:
        {
            'success': True,
            'text': str,
            'content': str,
            'model': str,
            'engine': 'gemini'
        }
    
    Implementation:
        1. Retrieve config from self.engines[engine]
        2. Extract client and model from config
        3. Combine system_instruction and prompt
        4. Call client.models.generate_content()
        5. Return formatted response
    """
```

**_generate_sarvam() - Fixed Request Format**

```python
def _generate_sarvam(
    self,
    prompt: str,
    system_instruction: Optional[str],
    temperature: float
) -> Dict[str, Any]:
    """
    Generate content using Sarvam AI with correct API format
    
    Args:
        prompt: User prompt
        system_instruction: Optional system instruction
        temperature: Sampling temperature
    
    Returns:
        {
            'success': True,
            'text': str,
            'content': str,
            'model': str,
            'engine': 'sarvam'
        }
    
    Request Format (Fixed):
        POST https://api.sarvam.ai/v1/chat/completions
        Headers:
            Authorization: Bearer {api_key}
            Content-Type: application/json
        Body:
            {
                "model": str,
                "messages": [
                    {"role": "system", "content": str},  # if system_instruction
                    {"role": "user", "content": str}
                ],
                "temperature": float,
                "max_tokens": int
            }
    
    Response Parsing:
        text = response.json()['choices'][0]['message']['content']
    
    Error Handling:
        - Catch HTTPError
        - Attempt to parse JSON error response
        - Fall back to raw text if JSON parsing fails
        - Log HTTP status code and error details
        - Raise exception with formatted error message
    """
```

## Data Models

### Engine Configuration

```python
# Gemini Engine Configuration
{
    'client': genai.Client,      # SDK client instance
    'model': str,                 # Model name (e.g., 'gemini-2.0-flash')
    'type': 'gemini'              # Engine type identifier
}

# Sarvam Engine Configuration
{
    'api_key': str,               # API key for authentication
    'model': str,                 # Model name (e.g., 'sarvam-m')
    'type': 'sarvam',             # Engine type identifier
    'endpoint': str               # API endpoint URL
}
```

### Generation Response

```python
{
    'success': bool,              # Always True for successful responses
    'text': str,                  # Generated text content
    'content': str,               # Same as text (for compatibility)
    'model': str,                 # Model name used
    'engine': str,                # Engine type ('gemini' or 'sarvam')
    'engine_used': str            # Engine identifier (added by orchestrator)
}
```

### Sarvam AI Request Format

```python
# Request Headers
{
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Request Payload
{
    'model': str,                 # e.g., 'sarvam-m'
    'messages': [
        {
            'role': 'system',     # Optional, only if system_instruction provided
            'content': str
        },
        {
            'role': 'user',
            'content': str
        }
    ],
    'temperature': float,         # 0.0 to 2.0
    'max_tokens': int            # Maximum tokens to generate
}
```

### Sarvam AI Response Format

```python
{
    'choices': [
        {
            'message': {
                'role': 'assistant',
                'content': str    # Generated text extracted from here
            },
            'finish_reason': str
        }
    ],
    'model': str,
    'usage': {
        'prompt_tokens': int,
        'completion_tokens': int,
        'total_tokens': int
    }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified several areas where properties can be consolidated to avoid redundancy:

**Consolidated Areas:**
1. **Sarvam Request Format Properties (5.1-5.7)**: These can be combined into a single comprehensive property that validates the entire request structure
2. **Logging Properties (6.1-6.2, 3.4)**: Engine attempt logging can be unified into one property covering both success and failure cases
3. **Gemini Engine Routing (2.2, 2.3, 2.5)**: These can be combined into one property about correct engine-to-client mapping
4. **Error Response Logging (1.2, 6.3, 6.4, 6.5)**: Can be unified into a comprehensive error logging property

**Retained Separate Properties:**
- Fallback sequence properties (3.1, 3.2, 3.3, 3.5) - each tests different aspects of the fallback chain
- Response structure properties (1.4, 7.2) - test different aspects of the response format
- Backward compatibility properties (7.1, 7.3, 7.4, 7.5) - each tests different compatibility aspects

### Property 1: Sarvam AI Request Format Compliance

*For any* prompt, system instruction, and temperature value, when the AI_Engine_System makes a request to Sarvam AI, the request SHALL include: (1) endpoint URL "https://api.sarvam.ai/v1/chat/completions", (2) Authorization header with format "Bearer {api_key}", (3) Content-Type header "application/json", (4) payload with model field, messages array (with system message first if system_instruction provided, then user message), temperature field, and max_tokens field, and (5) all message objects SHALL have role and content fields.

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7**

### Property 2: Sarvam AI Successful Response

*For any* valid prompt and system instruction, when Sarvam AI returns HTTP 200, the AI_Engine_System SHALL return a response containing the generated text extracted from data['choices'][0]['message']['content'], along with engine metadata including model name and engine identifier.

**Validates: Requirements 1.1, 1.4, 5.8**

### Property 3: Comprehensive Error Logging

*For any* engine failure, the AI_Engine_System SHALL log: (1) the engine name, (2) the error message, (3) for HTTP errors, the HTTP status code, (4) for Sarvam AI errors, attempt to parse and log JSON error response, and (5) if JSON parsing fails, log the raw response text.

**Validates: Requirements 1.2, 1.5, 6.1, 6.3, 6.4, 6.5**

### Property 4: Gemini Engine Parameter Routing

*For any* prompt and system instruction, when _generate_gemini is called with engine parameter AIEngine.GEMINI, it SHALL use the Gemini_Engine_1 client and model from engines[AIEngine.GEMINI], and when called with AIEngine.GEMINI3, it SHALL use the Gemini_Engine_3 client and model from engines[AIEngine.GEMINI3].

**Validates: Requirements 2.1, 2.2, 2.3, 2.5**

### Property 5: Gemini Engine 3 End-to-End Generation

*For any* valid prompt, when Gemini Engine 3 is available and selected, the AI_Engine_System SHALL successfully generate content using the GEMINI_ENGINE3 API key and return a response with generated text and engine metadata.

**Validates: Requirements 2.4**

### Property 6: Primary to Secondary Fallback

*For any* prompt, when Gemini_Engine_1 fails (raises exception or returns error), the AI_Engine_System SHALL attempt to use Sarvam_Engine as the next engine in the fallback sequence.

**Validates: Requirements 3.1**

### Property 7: Secondary to Tertiary Fallback

*For any* prompt, when both Gemini_Engine_1 and Sarvam_Engine fail, the AI_Engine_System SHALL attempt to use Gemini_Engine_3 as the final fallback engine.

**Validates: Requirements 3.2**

### Property 8: All Engines Failed Exception

*For any* prompt, when all three engines (Gemini, Sarvam, Gemini3) fail to generate content, the AI_Engine_System SHALL raise an exception containing details about the last error encountered.

**Validates: Requirements 3.3**

### Property 9: Engine Attempt Logging

*For any* generation request, the AI_Engine_System SHALL log each engine attempt with: (1) engine name at info level when attempting, (2) success status with engine name at info level when successful, and (3) failure status with engine name and error at warning level when failed.

**Validates: Requirements 3.4, 6.1, 6.2**

### Property 10: Short-Circuit on Success

*For any* prompt, when an engine successfully generates content, the AI_Engine_System SHALL return the result immediately without attempting any remaining engines in the priority list.

**Validates: Requirements 3.5**

### Property 11: Generate Content Signature Stability

*For any* existing code calling generate_content, the method signature SHALL accept the same parameters (prompt, system_instruction, temperature, preferred_engine) and return a dictionary with the same structure (success, text, content, model, engine, engine_used).

**Validates: Requirements 7.1, 7.2**

### Property 12: Engine Priority Order Preservation

*For any* initialization of MultiEngineAIClient, the engine_priority list SHALL maintain the order [AIEngine.GEMINI, AIEngine.SARVAM, AIEngine.GEMINI3] unless PRIMARY_AI_ENGINE environment variable specifies a different primary engine.

**Validates: Requirements 7.3**

### Property 13: Graceful Engine Unavailability

*For any* engine that is not configured (missing API key or initialization failure), the AI_Engine_System SHALL skip that engine during fallback without raising errors, and continue to the next available engine.

**Validates: Requirements 7.5**

### Property 14: Initialization Backward Compatibility

*For any* existing initialization code that creates a MultiEngineAIClient instance, the initialization SHALL complete successfully without requiring code modifications, and all previously working engines SHALL remain functional.

**Validates: Requirements 7.4**

## Error Handling

### Error Categories

**1. Configuration Errors**
- Missing API keys
- Invalid model names
- SDK not installed

**Handling Strategy:**
- Log warning during initialization
- Skip engine (don't add to engines dict)
- Continue with other engines
- System remains functional if at least one engine available

**2. API Errors**

**Sarvam AI Errors:**
- HTTP 400 Bad Request: Invalid request format
- HTTP 401 Unauthorized: Invalid API key
- HTTP 429 Too Many Requests: Rate limit exceeded
- HTTP 500 Server Error: Sarvam service issue

**Handling Strategy:**
- Catch requests.exceptions.HTTPError
- Attempt to parse JSON error response
- Log HTTP status code and error details
- Fall back to next engine
- Preserve error information for final exception if all engines fail

**Gemini Errors:**
- Quota exceeded
- Invalid API key
- Model not found
- Content safety violations

**Handling Strategy:**
- Catch exceptions from genai SDK
- Log error message
- Fall back to next engine
- Preserve error information

**3. Network Errors**
- Connection timeout
- DNS resolution failure
- Network unreachable

**Handling Strategy:**
- Set timeout on HTTP requests (30 seconds)
- Catch requests.exceptions.Timeout
- Catch requests.exceptions.ConnectionError
- Log error and fall back to next engine

**4. Response Parsing Errors**
- Invalid JSON response
- Missing expected fields
- Unexpected response structure

**Handling Strategy:**
- Catch json.JSONDecodeError
- Catch KeyError for missing fields
- Log raw response for debugging
- Fall back to next engine

### Error Logging Format

```python
# Engine Attempt
logger.info(f"Attempting generation with {engine.value}")

# Engine Success
logger.info(f"✓ Generation successful with {engine.value}")

# Engine Failure
logger.warning(f"✗ {engine.value} failed: {str(e)}")

# Sarvam HTTP Error (with JSON response)
logger.error(f"Sarvam AI error response: {error_detail}")
logger.error(f"Sarvam AI HTTP {response.status_code}: {error_detail}")

# Sarvam HTTP Error (without JSON response)
logger.error(f"Sarvam AI error text: {error_detail}")
logger.error(f"Sarvam AI HTTP {response.status_code}: {error_detail}")

# All Engines Failed
raise Exception(f"All AI engines failed. Last error: {last_error}")
```

### Error Recovery Flow

```
Error Occurs
     │
     ▼
┌─────────────────────┐
│ Log Error Details   │
│ - Engine name       │
│ - Error message     │
│ - HTTP status (if   │
│   applicable)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Store Last Error    │
│ (for final exception│
│  if all fail)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ More Engines        │
│ Available?          │
└──────────┬──────────┘
           │
      Yes  │  No
           │  │
           │  ▼
           │ ┌─────────────────────┐
           │ │ Raise Exception     │
           │ │ with Last Error     │
           │ └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Try Next Engine     │
└─────────────────────┘
```

## Testing Strategy

### Dual Testing Approach

This feature requires both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests** focus on:
- Specific examples of request/response formats
- Edge cases (empty prompts, missing API keys, malformed responses)
- Integration points between components
- Error conditions with specific error types
- Documentation completeness checks

**Property-Based Tests** focus on:
- Universal properties that hold for all inputs
- Request format validation across random prompts
- Fallback behavior across different failure scenarios
- Response structure consistency
- Comprehensive input coverage through randomization

Together, these approaches provide comprehensive coverage: unit tests catch concrete bugs and verify specific behaviors, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Configuration

**Framework:** Use `hypothesis` for Python property-based testing

**Configuration:**
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: multi-engine-ai-completion, Property {number}: {property_text}`

**Example Property Test Structure:**

```python
from hypothesis import given, strategies as st
import pytest

# Feature: multi-engine-ai-completion, Property 1: Sarvam AI Request Format Compliance
@given(
    prompt=st.text(min_size=1, max_size=1000),
    system_instruction=st.one_of(st.none(), st.text(min_size=1, max_size=500)),
    temperature=st.floats(min_value=0.0, max_value=2.0)
)
@pytest.mark.property_test
def test_sarvam_request_format_property(prompt, system_instruction, temperature, monkeypatch):
    """
    Property 1: For any prompt, system instruction, and temperature,
    Sarvam AI requests must follow the correct format
    """
    # Test implementation
    pass
```

### Unit Test Categories

**1. Initialization Tests**
- Test each engine initialization method
- Test with valid and invalid API keys
- Test with missing environment variables
- Test engine priority ordering

**2. Request Format Tests**
- Test Sarvam AI request structure
- Test header formatting
- Test payload structure with and without system_instruction
- Test message array ordering

**3. Response Parsing Tests**
- Test successful response parsing for each engine
- Test error response parsing
- Test JSON extraction from Sarvam responses
- Test handling of malformed responses

**4. Fallback Logic Tests**
- Test fallback from Gemini to Sarvam
- Test fallback from Sarvam to Gemini3
- Test all engines failing
- Test short-circuit on first success

**5. Error Handling Tests**
- Test HTTP error handling
- Test network timeout handling
- Test JSON parsing errors
- Test missing field errors

**6. Backward Compatibility Tests**
- Test existing method signatures
- Test return value formats
- Test initialization without modifications

**7. Documentation Tests**
- Verify MULTI_ENGINE_AI_SETUP.md contains all three engines
- Verify .env.example contains GEMINI_ENGINE3 variables
- Verify documentation includes troubleshooting steps

### Property Test Categories

**1. Request Format Properties**
- Property 1: Sarvam AI Request Format Compliance
- Property 11: Generate Content Signature Stability

**2. Response Properties**
- Property 2: Sarvam AI Successful Response
- Property 5: Gemini Engine 3 End-to-End Generation

**3. Routing Properties**
- Property 4: Gemini Engine Parameter Routing
- Property 12: Engine Priority Order Preservation

**4. Fallback Properties**
- Property 6: Primary to Secondary Fallback
- Property 7: Secondary to Tertiary Fallback
- Property 8: All Engines Failed Exception
- Property 10: Short-Circuit on Success

**5. Logging Properties**
- Property 3: Comprehensive Error Logging
- Property 9: Engine Attempt Logging

**6. Robustness Properties**
- Property 13: Graceful Engine Unavailability
- Property 14: Initialization Backward Compatibility

### Test Data Strategies

**For Property Tests:**
- Use `hypothesis.strategies` to generate random prompts (1-1000 chars)
- Generate random system instructions (optional, 1-500 chars)
- Generate random temperature values (0.0-2.0)
- Generate random API keys (valid and invalid formats)
- Generate random error responses (HTTP codes, JSON structures)

**For Unit Tests:**
- Use specific examples from documentation
- Use edge cases (empty strings, very long strings, special characters)
- Use known error responses from API documentation
- Use realistic prompts and responses

### Mocking Strategy

**Mock External Dependencies:**
- Mock `genai.Client` for Gemini engines
- Mock `requests.post` for Sarvam AI
- Mock environment variables for configuration
- Mock logger to verify logging calls

**Don't Mock:**
- Internal routing logic
- Fallback sequence logic
- Error handling logic
- Response formatting logic

### Test Execution

```bash
# Run all tests
pytest tests/

# Run only unit tests
pytest tests/ -m "not property_test"

# Run only property tests
pytest tests/ -m property_test

# Run with coverage
pytest tests/ --cov=src/services/ai_engine --cov-report=html

# Run specific property test with verbose output
pytest tests/test_ai_engine_properties.py::test_sarvam_request_format_property -v
```

### Success Criteria

- All unit tests pass
- All property tests pass (100 iterations each)
- Code coverage > 90% for ai_engine.py
- No regressions in existing functionality
- Documentation tests pass
- Manual testing confirms:
  - Sarvam AI returns HTTP 200 for valid requests
  - Gemini Engine 3 successfully generates content
  - Fallback works through all three engines
  - Error logging provides sufficient debugging information

## Implementation Notes

### Key Changes Required

**1. Modify _generate_gemini Method**

```python
# BEFORE
def _generate_gemini(
    self,
    prompt: str,
    system_instruction: Optional[str],
    temperature: float
) -> Dict[str, Any]:
    config = self.engines[AIEngine.GEMINI]  # Always uses Engine 1
    # ...

# AFTER
def _generate_gemini(
    self,
    prompt: str,
    system_instruction: Optional[str],
    temperature: float,
    engine: AIEngine  # NEW PARAMETER
) -> Dict[str, Any]:
    config = self.engines[engine]  # Uses specified engine
    # ...
```

**2. Update generate_content Method**

```python
# Update the routing logic to pass engine parameter
if engine == AIEngine.GEMINI or engine == AIEngine.GEMINI3:
    result = self._generate_gemini(prompt, system_instruction, temperature, engine)
    # Pass engine parameter ────────────────────────────────────────────────┘
```

**3. Fix Sarvam AI Request Format**

The current implementation is already correct, but ensure:
- Endpoint URL is exactly "https://api.sarvam.ai/v1/chat/completions"
- Authorization header format is "Bearer {api_key}" (with space after Bearer)
- Content-Type header is "application/json"
- Payload includes all required fields
- Messages array has correct structure

**4. Enhance Error Logging**

```python
except requests.exceptions.HTTPError as e:
    error_detail = ""
    try:
        error_detail = response.json()
        logger.error(f"Sarvam AI error response: {error_detail}")
    except:
        error_detail = response.text
        logger.error(f"Sarvam AI error text: {error_detail}")
    raise Exception(f"Sarvam AI HTTP {response.status_code}: {error_detail}")
```

### Sarvam AI API Specification

Based on research and the requirements, the Sarvam AI API follows the OpenAI-compatible chat completions format:

**Endpoint:** `https://api.sarvam.ai/v1/chat/completions`

**Authentication:** Bearer token in Authorization header

**Request Format:**
```json
{
  "model": "sarvam-m",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Response Format:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Generated text here"
      },
      "finish_reason": "stop"
    }
  ],
  "model": "sarvam-m",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### Environment Variables

```bash
# Gemini Engine 1 (Primary)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Sarvam AI Engine (Secondary)
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_MODEL=sarvam-m

# Gemini Engine 3 (Tertiary Backup)
GEMINI_ENGINE3=your_second_gemini_api_key_here
GEMINI_MODEL_ENGINE3=gemini-2.0-flash

# Optional: Set primary engine
PRIMARY_AI_ENGINE=gemini  # or 'sarvam'
```

### Migration Path

Since this is a bug fix and completion of existing functionality, no migration is required. The changes are backward compatible:

1. Existing code continues to work without modifications
2. Method signatures remain unchanged (engine parameter has default)
3. Return value formats remain unchanged
4. Engine priority order remains unchanged
5. Initialization process remains unchanged

### Performance Considerations

**Latency:**
- Gemini: ~1-3 seconds per request
- Sarvam AI: ~2-4 seconds per request
- Fallback adds latency only on failure

**Optimization:**
- Short-circuit on first success (don't try remaining engines)
- Set reasonable timeout (30 seconds) to avoid hanging
- Log timing information for monitoring

**Rate Limits:**
- Gemini free tier: 50 requests/day for gemini-2.0-flash
- Sarvam AI: Check https://www.sarvam.ai for current limits
- System automatically falls back when rate limits hit

### Security Considerations

**API Key Management:**
- Store API keys in environment variables only
- Never log API keys
- Use placeholder detection to skip unconfigured engines

**Input Validation:**
- Validate temperature range (0.0-2.0)
- Validate prompt is not empty
- Sanitize prompts if needed for specific use cases

**Error Information:**
- Log error details for debugging
- Don't expose API keys in error messages
- Include enough information to diagnose issues

### Monitoring and Observability

**Metrics to Track:**
- Engine success/failure rates
- Fallback frequency
- Average latency per engine
- Error types and frequencies

**Logging Strategy:**
- Info level: Engine attempts and successes
- Warning level: Engine failures
- Error level: HTTP errors with details
- Debug level: Request/response details (without API keys)

**Alerting:**
- Alert when all engines fail repeatedly
- Alert when primary engine has high failure rate
- Alert when response latency exceeds threshold

## Documentation Updates

### Files to Update

**1. MULTI_ENGINE_AI_SETUP.md**
- Add section for Gemini Engine 3
- Update architecture diagram to show three engines
- Add troubleshooting section for Sarvam AI 400 errors
- Include configuration examples for all three engines
- Document fallback order and behavior

**2. .env.example**
- Add GEMINI_ENGINE3 variable
- Add GEMINI_MODEL_ENGINE3 variable
- Include comments explaining each engine's purpose

**3. README.md** (if applicable)
- Update AI capabilities section
- Mention three-engine fallback system
- Link to MULTI_ENGINE_AI_SETUP.md

### Troubleshooting Guide

Add to MULTI_ENGINE_AI_SETUP.md:

```markdown
## Troubleshooting

### Sarvam AI Returns 400 Bad Request

**Symptoms:**
- Sarvam AI fails with HTTP 400
- Error message indicates invalid request

**Possible Causes:**
1. Incorrect API endpoint URL
2. Missing or malformed Authorization header
3. Invalid request payload structure
4. Missing required fields (model, messages, temperature, max_tokens)

**Solutions:**
1. Verify endpoint is exactly: https://api.sarvam.ai/v1/chat/completions
2. Check Authorization header format: "Bearer {api_key}" (with space)
3. Ensure Content-Type header is "application/json"
4. Verify payload includes all required fields
5. Check that messages array has correct structure with role and content

**Debugging:**
- Check logs for detailed error response from Sarvam API
- Verify API key is valid and not a placeholder
- Test API key with curl command (see examples below)

### Gemini Engine 3 Not Working

**Symptoms:**
- System skips Gemini Engine 3
- Logs show "Gemini Engine 3: API key not set or using placeholder"

**Solutions:**
1. Set GEMINI_ENGINE3 environment variable with valid API key
2. Ensure API key is not the placeholder "YOUR_SECOND_GEMINI_KEY_HERE"
3. Verify google-genai package is installed
4. Check that API key has not exceeded quota

### All Engines Failing

**Symptoms:**
- Exception: "All AI engines failed"
- No engines available

**Solutions:**
1. Check that at least one API key is configured
2. Verify API keys are valid and not expired
3. Check network connectivity
4. Verify none of the engines have exceeded rate limits
5. Check logs for specific error messages from each engine
```

## Conclusion

This design addresses both critical issues in the multi-engine AI system:

1. **Sarvam AI 400 Error**: Fixed by ensuring request format exactly matches API specification
2. **Gemini Engine 3 Completion**: Enabled by adding engine parameter to _generate_gemini method

The solution maintains backward compatibility while enabling a robust three-tier fallback system. Comprehensive error logging and testing ensure the system is reliable and debuggable.

**Next Steps:**
1. Implement code changes in ai_engine.py
2. Write unit tests and property-based tests
3. Update documentation files
4. Test with real API keys for all three engines
5. Verify fallback behavior in production-like environment
6. Monitor error logs and success rates after deployment
