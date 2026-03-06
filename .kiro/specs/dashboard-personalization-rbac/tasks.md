# Implementation Plan: Dashboard Personalization and RBAC

## Overview

This implementation plan breaks down the dashboard personalization and role-based access control (RBAC) feature into discrete coding tasks. The implementation will add feature usage tracking, personalized recent features display, user-specific alert filtering, admin aggregated metrics, and enhanced access controls with visual indicators.

The tasks build incrementally, starting with database schema and core services, then moving to UI modifications, and finally integration and testing.

## Tasks

- [x] 1. Set up database schema for RBAC features
  - [x] 1.1 Create feature_usage_history table in DuckDB schema
    - Add table with columns: usage_id (VARCHAR, PK), user_id (VARCHAR), feature_name (VARCHAR), accessed_at (TIMESTAMP)
    - Create index on (user_id, accessed_at DESC) for efficient recent features queries
    - Create index on (feature_name, accessed_at DESC) for analytics queries
    - Modify `src/database/duckdb_schema.py` to include table creation in `initialize_schema()` method
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [x] 1.2 Create user_preferences table in DuckDB schema
    - Add table with columns: user_id (VARCHAR, PK), preferences_json (JSON), updated_at (TIMESTAMP)
    - Modify `src/database/duckdb_schema.py` to include table creation
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ]* 1.3 Write unit tests for database schema
    - Test feature_usage_history table structure and columns
    - Test user_preferences table structure and columns
    - Test index creation for both tables
    - _Requirements: 8.1-8.6, 9.1-9.3_

- [x] 2. Implement AccessControlService for role-based permissions
  - [x] 2.1 Create AccessControlService class
    - Create new file `src/services/access_control_service.py`
    - Implement `can_access_feature(user_id, feature_name)` method with FEATURE_PERMISSIONS mapping
    - Implement `get_user_role(user_id)` method using auth_service
    - Implement `get_accessible_features(user_id)` method returning list of accessible features
    - Implement `is_feature_locked(user_id, feature_name)` method for UI lock icon logic
    - _Requirements: 1.1, 2.1, 2.2_

  - [ ]* 2.2 Write property test for universal Content Intelligence access
    - **Property 1: Universal Content Intelligence Access**
    - **Validates: Requirements 1.1**
    - Test that all user roles (admin, creator, viewer) can access Content Intelligence
    - Use hypothesis library with sampled_from strategy for roles

  - [ ]* 2.3 Write property test for Transform access control by role
    - **Property 2: Transform Access Control by Role**
    - **Validates: Requirements 2.1**
    - Test that Transform access is granted if and only if role is admin or creator
    - Use hypothesis library with sampled_from strategy for roles

- [-] 3. Implement FeatureUsageTracker for usage tracking
  - [x] 3.1 Create FeatureUsageTracker class
    - Create new file `src/services/feature_usage_tracker.py`
    - Implement `track_feature_access(user_id, feature_name)` method to record events
    - Implement `get_recent_features(user_id, limit=3)` method to query recent features
    - Implement `get_usage_count(user_id, feature_name)` method to count accesses
    - Implement `get_last_accessed(user_id, feature_name)` method to get last timestamp
    - Implement `should_track_event(user_id, feature_name)` method to prevent duplicates on refresh
    - Use session-based tracking with `current_sessions` dictionary to detect navigation vs refresh
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.6, 10.7_

  - [ ]* 3.2 Write property test for feature access event structure
    - **Property 3: Feature Access Event Structure**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
    - Test that all recorded events contain valid usage_id, user_id, feature_name, and timestamp
    - Use hypothesis library with text and sampled_from strategies

  - [ ]* 3.3 Write unit tests for FeatureUsageTracker
    - Test tracking Content Intelligence access generates event
    - Test no duplicate events on data refresh within same feature
    - Test new event generated when navigating to different feature
    - Test usage count accuracy for multiple accesses
    - _Requirements: 10.1, 10.6, 10.7, 14.1_

- [x] 4. Implement AlertFilterService for user-specific alerts
  - [x] 4.1 Create AlertFilterService class
    - Create new file `src/services/alert_filter_service.py`
    - Implement `get_user_alerts(user_id)` method to retrieve all user-specific alerts
    - Implement `get_personalized_labels(user_role)` method returning label mappings
    - Implement `filter_content_intelligence_alerts(user_id)` method
    - Implement `filter_transform_alerts(user_id)` method
    - Implement `filter_quality_alerts(user_id)` method
    - Implement `filter_rate_limit_alerts(user_id)` method
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ]* 4.2 Write property test for user-specific alert filtering
    - **Property 6: User-Specific Alert Filtering**
    - **Validates: Requirements 6.1, 6.6**
    - Test that all displayed alerts match the current user's user_id
    - Use hypothesis library to generate user alerts and other user alerts

  - [ ]* 4.3 Write property test for alert source inclusion
    - **Property 7: Alert Source Inclusion**
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
    - Test that alerts from all sources (Content Intelligence, Transform, Quality, Rate Limits) are included
    - Verify no alerts from other users are included

  - [ ]* 4.4 Write unit tests for AlertFilterService
    - Test personalized labels for non-admin users
    - Test system-wide label for admin users
    - Test empty alerts message display
    - Test alert filtering from each source
    - _Requirements: 11.1-11.5, 6.9_

- [ ] 5. Extend MonitoringService for admin aggregated metrics
  - [ ] 5.1 Add aggregated metrics methods to MonitoringService
    - Modify `src/services/monitoring_service.py`
    - Implement `get_aggregated_metrics(user_id)` method that checks role and returns appropriate metrics
    - Implement `_get_all_users_metrics()` private method for admin aggregation
    - Implement `_get_user_specific_metrics(user_id)` private method for creator/viewer
    - Implement `get_user_metrics_breakdown()` method returning per-user table data
    - Implement `get_filtered_metrics(user_id, filter_user_id)` method for admin user filtering
    - Implement `compute_user_statistics(user_id)` method for individual user stats
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10_

  - [ ]* 5.2 Write property test for admin metrics aggregation completeness
    - **Property 8: Admin Metrics Aggregation Completeness**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**
    - Test that admin aggregated metrics include data from all users
    - Verify admin's own data is included in aggregation

  - [ ]* 5.3 Write property test for non-admin metrics isolation
    - **Property 9: Non-Admin Metrics Isolation**
    - **Validates: Requirements 7.10**
    - Test that creator/viewer only see their own metrics
    - Verify no other user data is included

  - [ ]* 5.4 Write unit tests for MonitoringService extensions
    - Test admin sees all users in breakdown table
    - Test non-admin sees only own metrics
    - Test user filter dropdown functionality
    - Test breakdown table columns and data
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [ ] 6. Checkpoint - Ensure all service layer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Modify auth_service to initialize user preferences
  - [ ] 7.1 Add user preferences initialization to signup
    - Modify `src/services/auth_service.py`
    - Add `_initialize_user_preferences(user_id)` private method
    - Call initialization method in `signup()` after user creation
    - Set default preferences: theme=light, language=English, notifications=true, auto_save=true, email_alerts=false, session_timeout=30
    - _Requirements: 9.4_

  - [ ]* 7.2 Write unit test for default preferences initialization
    - Test that new user accounts get default preferences
    - Verify preferences_json structure and values
    - _Requirements: 9.4_

- [ ] 8. Update alert generation to include user_id association
  - [ ] 8.1 Modify content_analyzer.py to associate alerts with user_id
    - Modify `src/services/content_analyzer.py`
    - Update `generate_quality_alert()` method to query user_id from ashoka_contentint table
    - Include user_id in alert metadata
    - _Requirements: 15.1, 15.3_

  - [ ] 8.2 Modify content_transformer.py to associate alerts with user_id
    - Modify `src/services/content_transformer.py`
    - Update `generate_transform_alert()` method to query user_id from transform_history table
    - Include user_id in alert metadata
    - _Requirements: 15.2_

  - [ ] 8.3 Modify rate limit tracking to associate alerts with user_id
    - Modify relevant service handling YouTube rate limits
    - Ensure rate limit alerts include user_id from youtube_rate_limits table
    - _Requirements: 15.4_

  - [ ]* 8.4 Write property test for alert user association
    - **Property 15: Alert User Association**
    - **Validates: Requirements 15.1, 15.2, 15.3, 15.4, 15.5**
    - Test that all generated alerts have user_id in metadata
    - Verify user_id corresponds to source table user_id

- [ ] 9. Implement dashboard UI modifications for access control
  - [ ] 9.1 Add access control initialization to dashboard
    - Modify `src/ui/dashboard.py`
    - Initialize AccessControlService, FeatureUsageTracker, and AlertFilterService in `create_dashboard()` method
    - Store service instances as class attributes
    - _Requirements: 1.1, 2.1_

  - [ ] 9.2 Implement Transform tab with conditional lock icon
    - Modify tab creation in `create_dashboard()` method
    - Check `is_feature_locked()` for Transform feature
    - For viewers: Add lock icon with tooltip "You don't have access", apply opacity-50 class
    - For admin/creator: Display normal tab without lock icon
    - Add click handler to show access denied notification for viewers
    - _Requirements: 2.2, 2.3, 2.4, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

  - [ ] 9.3 Implement feature access tracking on tab navigation
    - Add `_track_feature_access(feature_name)` helper method
    - Call tracking method in each tab panel (Overview, Content Intelligence, Transform, Monitoring, Alerts, Security)
    - Retrieve user_id from app.storage.general
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]* 9.4 Write unit tests for Transform lock icon display
    - Test viewer sees lock icon on Transform tab
    - Test admin/creator do not see lock icon
    - Test viewer clicking Transform shows access denied notification
    - Test lock icon tooltip appears within 200ms
    - Test Transform tab has reduced opacity for viewers
    - _Requirements: 2.3, 2.4, 2.6, 13.1-13.6_

- [ ] 10. Implement Recent Features Panel in Overview
  - [ ] 10.1 Create Recent Features section in Overview panel
    - Modify `_create_overview_panel()` method in `src/ui/dashboard.py`
    - Add "Recent Features" card section
    - Query `feature_tracker.get_recent_features(user_id, limit=3)`
    - Display empty state message if no features accessed
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 10.2 Implement feature card rendering
    - Create `_create_feature_card(feature)` helper method
    - Display feature icon, name, relative timestamp, and usage count
    - Map feature names to icons (Content Intelligence→psychology, Transform→transform, etc.)
    - Implement `_format_relative_time(timestamp)` helper for relative time formatting
    - Make cards clickable with hover effects
    - _Requirements: 4.5, 4.6, 4.7, 4.8_

  - [ ] 10.3 Implement feature navigation on card click
    - Create `_navigate_to_feature(feature_name)` helper method
    - Map feature names to tab objects
    - Trigger tab change when card is clicked
    - _Requirements: 4.9_

  - [ ]* 10.4 Write property test for recent features ordering and limiting
    - **Property 4: Recent Features Ordering and Limiting**
    - **Validates: Requirements 4.2, 5.3**
    - Test that at most 3 features are returned
    - Test features are ordered by accessed_at descending

  - [ ]* 10.5 Write unit tests for Recent Features Panel
    - Test empty state message when no features accessed
    - Test display of fewer than 3 features
    - Test feature card click navigation
    - Test relative time formatting
    - _Requirements: 4.4, 4.3, 4.9_

- [ ] 11. Implement Recent Features in Profile Settings
  - [ ] 11.1 Add Recent Features section to profile dialog
    - Modify `_show_profile_dialog()` method in `src/ui/dashboard.py`
    - Add "Recent Features" section after user info
    - Query `feature_tracker.get_recent_features(user_id, limit=3)`
    - Display empty state message if no usage history
    - _Requirements: 5.1, 5.2, 5.3, 5.7_

  - [ ] 11.2 Display feature usage with absolute timestamps
    - For each feature, show feature name, absolute timestamp, and total usage count
    - Format timestamp as "YYYY-MM-DD HH:MM:SS"
    - Make cards non-interactive (no click navigation)
    - _Requirements: 5.4, 5.5, 5.6_

  - [ ]* 11.3 Write property test for recent features display completeness
    - **Property 5: Recent Features Display Completeness**
    - **Validates: Requirements 4.5, 4.6, 4.7, 4.8, 5.4, 5.5, 5.6**
    - Test that all displayed features include name, icon, timestamp, and usage count

- [ ] 12. Implement user-specific Alerts Panel
  - [ ] 12.1 Modify Alerts Panel to use AlertFilterService
    - Modify `_create_alerts_panel()` method in `src/ui/dashboard.py`
    - Get user_id and user_role from session
    - Call `alert_filter.get_personalized_labels(user_role)` for label mappings
    - Call `alert_filter.get_user_alerts(user_id)` to get filtered alerts
    - Display empty state message if no alerts
    - _Requirements: 6.1, 6.6, 6.9_

  - [ ] 12.2 Implement personalized alert labels
    - Use personalized labels from AlertFilterService
    - Display "Your Content Quality Score", "Your Recent Analyses", "Your Transformations", "Your API Usage" for non-admin
    - Display "System-Wide Alerts" panel header for admin
    - _Requirements: 6.7, 6.8, 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ] 12.3 Implement alert card rendering
    - Create `_create_alert_card(alert)` helper method
    - Display alert severity with color coding
    - Show alert message and relative timestamp
    - Use icon based on alert type
    - _Requirements: 6.1-6.6_

  - [ ]* 12.4 Write unit tests for Alerts Panel
    - Test personalized labels for non-admin
    - Test system-wide label for admin
    - Test empty alerts message
    - Test alert filtering by user_id
    - _Requirements: 6.7, 6.8, 6.9, 11.1-11.5_

- [ ] 13. Checkpoint - Ensure all UI component tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Implement admin Monitoring Panel with user breakdown
  - [ ] 14.1 Modify Monitoring Panel for role-based metrics
    - Modify `_create_monitoring_panel()` method in `src/ui/dashboard.py`
    - Get user_id and user_role from session
    - For admin: Add user filter dropdown with all usernames
    - Add "Reset Filter" button for admin
    - Create metrics_container for dynamic metric updates
    - _Requirements: 7.7, 7.8, 7.9_

  - [ ] 14.2 Implement metrics loading based on role and filter
    - Create `_load_metrics(user_id, filter_user_id)` helper method
    - Call `monitoring_service.get_aggregated_metrics(user_id)` for initial load
    - Call `monitoring_service.get_filtered_metrics(user_id, filter_user_id)` when filter applied
    - Display metrics in cards: Total Analyses, Total Transformations, Avg Quality Score
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.10_

  - [ ] 14.3 Implement admin user metrics breakdown table
    - Create `_load_user_breakdown()` helper method (admin only)
    - Call `monitoring_service.get_user_metrics_breakdown()`
    - Create sortable table with columns: Username, Total Analyses, Total Transformations, Avg Quality Score, Last Active
    - Make username clickable to filter metrics
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ] 14.4 Implement user filter interactions
    - Create `_on_user_filter_change(selected_user)` handler for dropdown
    - Create `_on_username_click(username)` handler for table row clicks
    - Create `_reset_user_filter()` handler for reset button
    - Update metrics display when filter changes
    - _Requirements: 7.8, 12.5, 12.6_

  - [ ]* 14.5 Write property test for admin user filter behavior
    - **Property 10: Admin User Filter Behavior**
    - **Validates: Requirements 7.8**
    - Test that selecting a user filters metrics to that user only
    - Test that "All Users" shows aggregated metrics

  - [ ]* 14.6 Write unit tests for Monitoring Panel
    - Test admin sees user breakdown table
    - Test non-admin sees only own metrics
    - Test user filter dropdown functionality
    - Test breakdown table columns and sorting
    - Test username click filters metrics
    - _Requirements: 7.10, 12.1-12.6_

- [ ] 15. Implement usage count calculation and display
  - [ ] 15.1 Add real-time usage count updates
    - Ensure `get_usage_count()` is called after each feature access event
    - Update Recent Features Panel to show updated counts
    - Update Profile Settings to show updated counts
    - _Requirements: 14.1, 14.2_

  - [ ] 15.2 Implement usage count formatting
    - Display usage count as integer
    - Display 0 for never-accessed features
    - _Requirements: 14.3, 14.4_

  - [ ]* 15.3 Write property test for usage count accuracy
    - **Property 13: Usage Count Accuracy**
    - **Validates: Requirements 14.1, 14.3**
    - Test that displayed usage count equals number of events in database
    - Use hypothesis to generate random number of accesses

  - [ ]* 15.4 Write property test for usage count real-time update
    - **Property 14: Usage Count Real-Time Update**
    - **Validates: Requirements 14.2**
    - Test that usage count updates immediately after new event

  - [ ]* 15.5 Write unit tests for usage count calculation
    - Test zero usage count for never-accessed features
    - Test usage count is integer type
    - Test usage count increments correctly
    - _Requirements: 14.3, 14.4_

- [ ] 16. Implement database migration for existing users
  - [ ] 16.1 Create migration script for RBAC tables
    - Create `migrations/add_rbac_tables.py`
    - Implement `upgrade()` function to create feature_usage_history and user_preferences tables
    - Implement `downgrade()` function to drop tables
    - Initialize default preferences for all existing users
    - _Requirements: 8.1-8.6, 9.1-9.4_

  - [ ] 16.2 Test migration script
    - Test upgrade creates tables and indexes
    - Test existing users get default preferences
    - Test downgrade removes tables cleanly
    - _Requirements: 9.4_

- [ ] 17. Integration testing and end-to-end flows
  - [ ]* 17.1 Test end-to-end feature access flow
    - User logs in → navigates to feature → event tracked → recent features updated → usage count incremented
    - _Requirements: 3.1-3.6, 4.1-4.9, 14.1-14.4_

  - [ ]* 17.2 Test role-based access flow
    - Viewer logs in → attempts Transform access → sees lock icon → clicks tab → receives denial notification
    - _Requirements: 2.1-2.5, 13.1-13.6_

  - [ ]* 17.3 Test admin metrics flow
    - Admin logs in → views monitoring → sees all users → selects specific user → metrics filtered → resets filter → sees aggregated view
    - _Requirements: 7.1-7.10, 12.1-12.6_

  - [ ]* 17.4 Test alert filtering flow
    - User performs analysis → alert generated with user_id → user views alerts → sees only own alerts → labels personalized
    - _Requirements: 6.1-6.9, 11.1-11.5, 15.1-15.5_

- [ ] 18. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties using hypothesis library
- Unit tests validate specific examples, edge cases, and UI components
- Integration tests validate end-to-end user flows
- All database queries use parameterized statements to prevent SQL injection
- Access control checks are enforced server-side, not just in UI
- Feature usage tracking uses session-based deduplication to prevent duplicate events on refresh
