# Implementation Plan: Ashoka Platform

## Overview

This implementation plan breaks down the Ashoka platform into discrete, incremental coding tasks. The platform will be built in layers, starting with foundational infrastructure, then the base intelligence layer, followed by transformation and monitoring capabilities. Each task builds on previous work, with property-based tests integrated throughout to ensure correctness.

The implementation uses Python with AWS services (Lambda, S3, DynamoDB, Step Functions, Bedrock) and follows a serverless architecture pattern.

## Tasks

- [x] 1. Set up project infrastructure and core utilities
  - Create project directory structure (src/, tests/, config/, docs/)
  - Set up Python virtual environment and dependencies (boto3, hypothesis, pytest, pydantic)
  - Configure AWS SDK with credentials and region settings
  - Create base configuration management (config.py for environment variables)
  - Set up logging infrastructure with structured logging
  - Create common utility functions (ID generation, timestamp handling)
  - _Requirements: 13.1, 13.2, 13.3, 14.1_

- [ ] 2. Implement data models and validation
  - [x] 2.1 Create core data models using Pydantic
    - Define User, ContentVersion, Session, OTP models
    - Define ContentAnalysis, Sentiment, OutcomeClassification models
    - Define TransformationResult, PlatformOutput models
    - Define QualityMetrics, RiskAssessment, Alert models
    - Add validation rules and constraints to all models
    - _Requirements: 1.3, 1.4, 1.5, 2.5, 3.1_
  
  - [ ] 2.2 Write property tests for data model validation
    - **Property: Model Validation Consistency** - For any valid data, creating a model instance should succeed; for any invalid data, it should raise validation errors
    - **Validates: Requirements 1.3, 2.5, 3.1**
  
  - [x] 2.3 Create database schema for DuckDB
    - Define tables for content analysis results
    - Define tables for quality metrics and risk assessments
    - Create indexes for efficient querying
    - _Requirements: 13.2_
  
  - [ ] 2.4 Create DynamoDB table definitions
    - Define table for user sessions with TTL
    - Define table for audit logs with GSI on user_id and timestamp
    - Define table for alerts with GSI on severity and timestamp
    - _Requirements: 11.1, 12.1_

- [ ] 3. Implement Authentication Service
  - [ ] 3.1 Implement credential validation
    - Create password hashing utilities (using bcrypt)
    - Implement username/password validation logic
    - Create user lookup from DynamoDB
    - _Requirements: 10.1_
  
  - [ ] 3.2 Write property test for credential validation
    - **Property 27: Credential Validation** - For any login attempt, the Authentication Service should validate credentials, returning success only when both match stored credentials
    - **Validates: Requirements 10.1**
  
  - [ ] 3.3 Implement OTP generation and validation
    - Create OTP generator (6-digit numeric codes)
    - Implement time-bound OTP with 5-minute expiration
    - Store OTPs in DynamoDB with TTL
    - Implement OTP validation logic
    - Implement single-use enforcement (mark as used after validation)
    - _Requirements: 10.2, 10.3, 10.4, 10.5, 10.6_
  
  - [ ] 3.4 Write property tests for OTP lifecycle
    - **Property 28: OTP Generation and Delivery** - For any valid credentials, an OTP should be generated and delivered
    - **Property 30: OTP Single-Use Enforcement** - For any successfully used OTP, subsequent attempts should be rejected
    - **Property 31: OTP Expiration Enforcement** - For any expired OTP, authentication attempts should be rejected
    - **Validates: Requirements 10.2, 10.3, 10.5, 10.6**
  
  - [ ] 3.5 Implement session management
    - Create session creation with 30-minute timeout
    - Store sessions in DynamoDB with TTL
    - Implement session validation logic
    - Implement activity tracking (update last_activity timestamp)
    - Implement session expiration check
    - _Requirements: 11.1, 11.2, 11.3, 11.4_
  
  - [ ] 3.6 Write property tests for session management
    - **Property 32: Session Creation with Timeout** - For any successful authentication, a session with 30-minute timeout should be created
    - **Property 33: Session Activity Tracking** - For any active session, activity should be tracked
    - **Property 34: Session Expiration on Timeout** - For any session inactive for 30+ minutes, it should be expired
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.4**
  
  - [ ] 3.7 Implement access control middleware
    - Create decorator for protected endpoints
    - Implement session validation before request processing
    - Implement redirect to login for expired sessions
    - _Requirements: 11.5_
  
  - [ ] 3.8 Write property test for access control
    - **Property 35: Protected Resource Access Control** - For any expired session, access to protected resources should be denied
    - **Validates: Requirements 11.5**

- [ ] 4. Implement Audit Logger
  - [ ] 4.1 Create audit logging functions
    - Implement log_login_attempt function
    - Implement log_session_start function
    - Implement log_session_end function
    - Store audit logs in DynamoDB
    - _Requirements: 12.1, 12.2, 12.3, 12.4_
  
  - [ ] 4.2 Write property test for audit logging
    - **Property 36: Login Attempt Logging** - For any login attempt, it should be logged with timestamp and outcome
    - **Property 37: Session Duration Logging** - For any ended session, duration should be logged
    - **Validates: Requirements 12.1, 12.2, 12.3, 12.4**
  
  - [ ] 4.3 Implement monthly report generation
    - Create query to aggregate login attempts by user and month
    - Calculate successful logins, failed attempts, and session durations
    - Generate MonthlyReport object
    - _Requirements: 12.5, 12.6_
  
  - [ ] 4.4 Write property test for monthly reports
    - **Property 38: Monthly Report Completeness** - For any user and month, the report should include all logins, failures, and durations
    - **Validates: Requirements 12.5, 12.6**

- [ ] 5. Checkpoint - Authentication and audit system complete
  - Ensure all authentication and audit tests pass
  - Verify OTP generation and session management work end-to-end
  - Ask the user if questions arise

- [ ] 6. Implement Content Ingestion Service
  - [x] 6.1 Create content ingestion functions
    - Implement ingest_text function
    - Implement file upload to S3
    - Implement text extraction from PDF (using PyPDF2)
    - Implement text extraction from DOCX (using python-docx)
    - Implement text extraction from TXT
    - Create version ID generator (UUID-based)
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 6.2 Write property tests for content ingestion
    - **Property 1: Content Ingestion Acceptance** - For any text or supported file, content should be accepted and stored
    - **Property 2: Version Identifier Uniqueness** - For any set of submissions, all version IDs should be unique
    - **Validates: Requirements 1.1, 1.2, 1.3**
  
  - [ ] 6.3 Implement version management
    - Create version history tracking
    - Link new versions to parent versions
    - Store version metadata in DynamoDB
    - Implement chronological ordering
    - _Requirements: 1.4, 1.5_
  
  - [ ] 6.4 Write property test for version history
    - **Property 3: Version History Preservation** - For any modified content, both original and new versions should be retrievable in chronological order
    - **Validates: Requirements 1.4, 1.5**
  
  - [ ] 6.5 Implement content storage and retrieval
    - Store content in S3 with encryption
    - Implement content retrieval with metadata
    - Add caching for frequently accessed content
    - _Requirements: 13.1, 13.4_
  
  - [ ] 6.6 Write property tests for storage
    - **Property 39: Comprehensive Data Persistence** - For any ingested content, it should be stored and retrievable
    - **Property 40: Retrieval Performance** - For any content request, retrieval should complete within 2 seconds
    - **Validates: Requirements 13.1, 13.4**

- [ ] 7. Implement Content Analyzer with Amazon Bedrock
  - [ ] 7.1 Create Bedrock client wrapper
    - Initialize Bedrock runtime client
    - Implement retry logic with exponential backoff
    - Implement circuit breaker pattern
    - Add error handling for rate limits and timeouts
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [ ] 7.2 Implement content analysis functions
    - Create generate_summary function using Bedrock
    - Create extract_takeaways function
    - Create extract_keywords function
    - Create extract_topics function
    - Create analyze_sentiment function
    - Combine all into analyze_content function
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [ ] 7.3 Write property test for comprehensive analysis
    - **Property 4: Comprehensive Content Analysis** - For any content, all analysis components (summary, takeaways, keywords, topics, sentiment) should be generated
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
  
  - [ ] 7.4 Store analysis results in DuckDB
    - Insert analysis results into database
    - Create indexes for efficient querying
    - _Requirements: 13.2_

- [ ] 8. Implement Outcome Classifier
  - [ ] 8.1 Create outcome classification logic
    - Implement policy risk detection rules
    - Implement failure detection based on analysis quality
    - Implement classification algorithm (Successful, Partially correct, Policy risk, Failed)
    - Calculate confidence scores
    - _Requirements: 3.1, 3.2, 3.3_
  
  - [ ] 8.2 Write property tests for outcome classification
    - **Property 5: Outcome Classification Completeness** - For any analysis, outcome should be one of the four classifications
    - **Property 6: Policy Risk Flagging** - For any policy risk content, it should be flagged for review
    - **Property 7: Failure Diagnostic Logging** - For any failed content, diagnostic info should be logged
    - **Validates: Requirements 3.1, 3.2, 3.3**
  
  - [ ] 8.3 Implement classification persistence
    - Store classification with content version
    - Make classification retrievable with version
    - _Requirements: 3.4_
  
  - [ ] 8.4 Write property test for classification persistence
    - **Property 8: Classification Persistence** - For any content version, classification should be stored and retrievable
    - **Validates: Requirements 3.4**

- [ ] 9. Checkpoint - Content intelligence layer complete
  - Ensure all content ingestion and analysis tests pass
  - Verify end-to-end flow: ingest → analyze → classify
  - Ask the user if questions arise

- [ ] 10. Implement Content Transformer
  - [ ] 10.1 Create platform adapter functions
    - Implement LinkedIn post formatter (3000 char limit, professional formatting)
    - Implement Twitter thread generator (280 char per tweet, thread numbering)
    - Implement Instagram caption formatter (2200 char limit, hashtag optimization)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ] 10.2 Write property tests for platform transformation
    - **Property 9: Multi-Platform Transformation** - For any content and platform, transformation should generate platform-specific output
    - **Property 10: Character Limit Enforcement** - For any transformed content, character limits should be respected
    - **Property 11: Platform Formatting Optimization** - For any transformed content, platform-specific formatting should be applied
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**
  
  - [ ] 10.3 Implement Tone Customization Engine
    - Create tone transformation prompts for Bedrock
    - Implement professional tone transformation
    - Implement casual tone transformation
    - Implement storytelling tone transformation
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 10.4 Write property tests for tone transformation
    - **Property 12: Tone Transformation Support** - For any content and tone, transformation should apply the tone
    - **Property 13: Message Preservation During Transformation** - For any transformed content, core message should be preserved
    - **Property 14: Tone Consistency** - For any tone-transformed content, tone should be consistent throughout
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
  
  - [ ] 10.4 Implement transformation orchestration
    - Combine platform adapters and tone engine
    - Create transform_content function
    - Store transformation results in S3
    - _Requirements: 4.1, 4.2, 4.3, 13.3_

- [ ] 11. Implement Quality Monitor
  - [ ] 11.1 Create quality metric calculators
    - Implement readability score calculation (Flesch-Kincaid)
    - Implement tone consistency checker
    - Implement duplicate detection (content hashing)
    - Implement similarity calculation (cosine similarity on embeddings)
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ] 11.2 Write property tests for quality monitoring
    - **Property 15: Quality Metrics Calculation** - For any content, all quality metrics should be calculated
    - **Property 16: Quality Alert Generation** - For any low-quality content, alerts should be generated
    - **Property 17: Duplicate Detection** - For any duplicate content, it should be detected
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
  
  - [ ] 11.3 Implement quality alert generation
    - Define quality thresholds
    - Create alert generation logic
    - Store alerts in DynamoDB
    - _Requirements: 6.5_

- [ ] 12. Implement Risk and Safety Monitor
  - [ ] 12.1 Create risk detection functions
    - Implement toxicity detection using Bedrock or external API
    - Implement hate speech detection
    - Implement policy-borderline content detection
    - Implement backlash risk estimation
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [ ] 12.2 Write property tests for risk assessment
    - **Property 18: Risk Assessment Completeness** - For any content, all risk assessments should be performed
    - **Property 19: High-Risk Content Blocking** - For any high-risk content, publication should be prevented and alerts generated
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**
  
  - [ ] 12.3 Implement publication blocking
    - Create should_prevent_publication function
    - Implement administrator alert generation
    - _Requirements: 7.5_

- [ ] 13. Implement Operations Monitor
  - [ ] 13.1 Create operations tracking
    - Implement operation metric recording
    - Calculate failure rates over time windows
    - Calculate average latency
    - Store metrics in CloudWatch
    - _Requirements: 8.1, 8.2_
  
  - [ ] 13.2 Write property tests for operations monitoring
    - **Property 20: Operations Metrics Tracking** - For any operation, failure rate and latency should be tracked
    - **Property 21: Quality Drift Detection** - For any quality degradation >20%, drift should be detected
    - **Property 22: Operational Alert Generation** - For any threshold breach, alerts should be generated
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
  
  - [ ] 13.3 Implement quality drift detection
    - Calculate baseline quality metrics
    - Compare current quality to baseline
    - Detect drift >20%
    - Generate alerts and notifications
    - _Requirements: 8.3, 8.4, 8.5_

- [ ] 14. Implement Reaction Intelligence Monitor
  - [ ] 14.1 Create reaction collection functions
    - Implement comment/reply collection (mock for now, real integration later)
    - Parse reaction data
    - Store reactions in DuckDB
    - _Requirements: 9.1_
  
  - [ ] 14.2 Implement engagement analysis
    - Calculate engagement patterns
    - Classify reactions (Positive, Neutral, Toxic, High backlash)
    - Detect toxic reactions
    - Detect high backlash (>30% negative)
    - _Requirements: 9.2, 9.3, 9.4, 9.5_
  
  - [ ] 14.3 Write property tests for reaction intelligence
    - **Property 23: Reaction Collection and Analysis** - For any published content, reactions should be collected and analyzed
    - **Property 24: Reaction Classification** - For any reaction, it should be classified into one category
    - **Property 25: Toxic Reaction Alerting** - For any toxic reactions, alerts should be sent
    - **Property 26: High Backlash Urgent Alerting** - For any high backlash, urgent alerts should be generated
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

- [ ] 15. Checkpoint - Monitoring layer complete
  - Ensure all monitoring tests pass
  - Verify quality, risk, operations, and reaction monitoring work
  - Ask the user if questions arise

- [ ] 16. Implement Workflow Orchestrator with Step Functions
  - [ ] 16.1 Define Step Functions state machine
    - Create state machine definition JSON
    - Define steps: Ingest → Analyze → Classify → Transform → Monitor
    - Configure retry policies (3 retries, exponential backoff)
    - Configure error handling and compensation
    - _Requirements: 15.1, 15.2_
  
  - [ ] 16.2 Create Lambda functions for each workflow step
    - Create ingestion Lambda
    - Create analysis Lambda
    - Create classification Lambda
    - Create transformation Lambda
    - Create monitoring Lambda
    - _Requirements: 15.1_
  
  - [ ] 16.3 Implement workflow orchestration logic
    - Create start_content_workflow function
    - Implement workflow status tracking
    - Implement failure logging and notification
    - Implement status updates on completion
    - Maintain execution history
    - _Requirements: 15.3, 15.4, 15.5_
  
  - [ ] 16.4 Write property tests for workflow orchestration
    - **Property 46: Workflow Orchestration** - For any workflow, Step Functions should be used for orchestration
    - **Property 47: Workflow Step Retry** - For any failed step, retries should occur per policy
    - **Property 48: Workflow Failure Handling** - For any exhausted retries, failure should be logged and admins notified
    - **Property 49: Workflow Completion Status Update** - For any completed workflow, content status should be updated
    - **Property 50: Workflow Execution History** - For any workflow, complete execution history should be maintained
    - **Validates: Requirements 15.1, 15.2, 15.3, 15.4, 15.5**

- [ ] 17. Implement API Gateway and REST API
  - [ ] 17.1 Create API Gateway configuration
    - Define REST API resources and methods
    - Configure CORS settings
    - Set up request/response models
    - _Requirements: 14.1_
  
  - [ ] 17.2 Implement API authentication middleware
    - Create token validation Lambda authorizer
    - Implement authentication token validation
    - _Requirements: 14.2_
  
  - [ ] 17.3 Write property test for API authentication
    - **Property 42: API Authentication Validation** - For any API request, authentication should be validated
    - **Validates: Requirements 14.2**
  
  - [ ] 17.4 Create API endpoint handlers
    - Implement POST /content/ingest endpoint
    - Implement GET /content/{version_id} endpoint
    - Implement POST /content/transform endpoint
    - Implement GET /analysis/{version_id} endpoint
    - Implement GET /monitoring/dashboard endpoint
    - _Requirements: 14.3_
  
  - [ ] 17.5 Write property tests for API endpoints
    - **Property 43: Authenticated Request Processing** - For any authenticated request, it should be processed
    - **Property 44: API Error Response Quality** - For any failed request, descriptive errors should be returned
    - **Validates: Requirements 14.3, 14.4**
  
  - [ ] 17.6 Implement rate limiting
    - Configure API Gateway rate limiting (100 req/min per client)
    - Implement rate limit exceeded responses (HTTP 429)
    - _Requirements: 14.5_
  
  - [ ] 17.7 Write property test for rate limiting
    - **Property 45: API Rate Limiting** - For any client exceeding rate limits, requests should be rejected
    - **Validates: Requirements 14.5**

- [ ] 18. Implement User Interface with Streamlit
  - [ ] 18.1 Create main application structure
    - Set up Streamlit app with navigation
    - Create login page
    - Create content submission page
    - Create dashboard page
    - Create monitoring page
    - _Requirements: 16.1, 16.2_
  
  - [ ] 18.2 Implement content submission interface
    - Create text input form
    - Create file upload widget
    - Display processing status with progress bar
    - _Requirements: 16.2, 16.3_
  
  - [ ] 18.3 Write property test for status display
    - **Property 51: Processing Status Display** - For any submission, processing status should be displayed
    - **Validates: Requirements 16.3**
  
  - [ ] 18.4 Implement analysis results dashboard
    - Display summary, keywords, topics, sentiment
    - Display quality metrics
    - Display risk assessment
    - Create visualizations (charts, gauges)
    - _Requirements: 16.4_
  
  - [ ] 18.5 Write property test for analysis display
    - **Property 52: Analysis Results Display** - For any completed analysis, all insights should be displayed
    - **Validates: Requirements 16.4**
  
  - [ ] 18.6 Implement transformation output display
    - Display LinkedIn post preview
    - Display Twitter thread preview
    - Display Instagram caption preview
    - Add copy-to-clipboard functionality
    - _Requirements: 16.5_
  
  - [ ] 18.7 Write property test for transformation display
    - **Property 53: Transformation Output Display** - For any transformation, all platform outputs should be displayed
    - **Validates: Requirements 16.5**

- [ ] 19. Implement Monitoring Dashboard with CloudWatch
  - [ ] 19.1 Create CloudWatch dashboard
    - Define dashboard layout
    - Add widgets for failure rates, latency, quality metrics
    - Configure auto-refresh
    - _Requirements: 17.1, 17.4_
  
  - [ ] 19.2 Implement real-time metrics display
    - Stream metrics to CloudWatch
    - Display metrics with <60 second latency
    - _Requirements: 17.2_
  
  - [ ] 19.3 Write property test for real-time display
    - **Property 54: Real-Time Metrics Display** - For any metric, it should appear in dashboard within 60 seconds
    - **Validates: Requirements 17.2**
  
  - [ ] 19.4 Implement alert display
    - Display alerts with severity indicators
    - Implement alert acknowledgment
    - _Requirements: 17.3_
  
  - [ ] 19.5 Write property test for alert display
    - **Property 55: Alert Prominence Display** - For any alert, it should be displayed prominently with severity
    - **Validates: Requirements 17.3**
  
  - [ ] 19.6 Implement threshold configuration
    - Create UI for threshold management
    - Implement threshold update logic
    - Apply new thresholds to metric evaluation
    - _Requirements: 17.5_
  
  - [ ] 19.7 Write property test for threshold configuration
    - **Property 56: Alert Threshold Configuration** - For any threshold change, it should be applied to subsequent evaluations
    - **Validates: Requirements 17.5**

- [ ] 20. Implement security and compliance features
  - [ ] 20.1 Implement encryption
    - Configure S3 bucket encryption (AES-256)
    - Configure DynamoDB encryption at rest
    - Enforce TLS 1.2+ for all connections
    - _Requirements: 13.5, 18.1, 18.2_
  
  - [ ] 20.2 Write property test for encryption
    - **Property 41: Comprehensive Encryption** - For any data, it should be encrypted at rest and in transit
    - **Validates: Requirements 13.5, 18.1, 18.2**
  
  - [ ] 20.3 Implement data deletion
    - Create data deletion workflow
    - Remove content from S3
    - Remove metadata from DynamoDB and DuckDB
    - Verify deletion within 30 days
    - _Requirements: 18.3_
  
  - [ ] 20.4 Write property test for data deletion
    - **Property 57: Data Deletion Compliance** - For any deletion request, all data should be removed within 30 days
    - **Validates: Requirements 18.3**
  
  - [ ] 20.5 Ensure audit log immutability
    - Configure DynamoDB to prevent audit log modifications
    - Implement audit log verification
    - _Requirements: 18.5_
  
  - [ ] 20.6 Write property test for audit logs
    - **Property 58: Audit Log Maintenance** - For any security event, an immutable audit log entry should be created
    - **Validates: Requirements 18.5**

- [ ] 21. Integration and end-to-end testing
  - [ ] 21.1 Write end-to-end workflow tests
    - Test complete flow: login → submit content → analyze → transform → monitor
    - Test authentication flow: login → OTP → session → logout
    - Test risk detection flow: submit risky content → detect → block → alert
  
  - [ ] 21.2 Write integration tests for external services
    - Test Amazon Bedrock integration
    - Test S3 storage and retrieval
    - Test DynamoDB operations
    - Test Step Functions execution
  
  - [ ] 21.3 Write performance tests
    - Test retrieval performance (<2 seconds)
    - Test concurrent user load (100, 500, 1000 users)
    - Test API rate limiting

- [ ] 22. Final checkpoint - Complete platform verification
  - Run all unit tests and property tests
  - Verify all 58 properties pass
  - Test end-to-end workflows
  - Review security configurations
  - Ask the user if questions arise

- [ ] 23. Deployment preparation
  - [ ] 23.1 Create deployment scripts
    - Create CloudFormation or Terraform templates
    - Define all AWS resources (Lambda, S3, DynamoDB, Step Functions, API Gateway)
    - Configure IAM roles and policies
  
  - [ ] 23.2 Create CI/CD pipeline
    - Set up GitHub Actions or AWS CodePipeline
    - Configure automated testing on commits
    - Configure deployment to staging and production
  
  - [ ] 23.3 Create documentation
    - Write API documentation
    - Write deployment guide
    - Write user guide
    - Write operator guide for monitoring

## Notes

- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- The implementation follows a layered approach: infrastructure → intelligence → transformation → monitoring
- AWS services are used throughout for scalability and managed operations
- All sensitive data is encrypted at rest and in transit
- Comprehensive audit logging ensures compliance and traceability
