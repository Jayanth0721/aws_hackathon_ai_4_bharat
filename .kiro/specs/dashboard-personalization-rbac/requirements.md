# Requirements Document

## Introduction

This document specifies requirements for enhancing the Ashoka GenAI Governance Dashboard with role-based access control (RBAC) improvements and personalized dashboard features. The system will track user feature usage, display personalized recent features, filter alerts by user context, and provide admin-specific aggregated metrics while maintaining strict access controls based on user roles.

## Glossary

- **Dashboard**: The Ashoka GenAI Governance Dashboard web application built with NiceGUI
- **User**: An authenticated person using the Dashboard with an assigned role
- **Admin**: A User with the "admin" role who has full system access and can view aggregated metrics
- **Creator**: A User with the "creator" role who can access Content Intelligence and Transform features
- **Viewer**: A User with the "viewer" role who has read-only access to Content Intelligence only
- **Feature**: A major functional area of the Dashboard (Content Intelligence, Transform, Monitoring, Alerts, Security, Overview)
- **Feature_Usage_Tracker**: The system component that records when Users access Features
- **Access_Control_Manager**: The system component that enforces role-based permissions
- **Alert_Filter**: The system component that filters alerts to show only user-relevant information
- **Metrics_Aggregator**: The system component that computes aggregated statistics across all Users
- **Recent_Features_Panel**: The UI component in Overview that displays the 3 most recently used Features
- **Transform_Feature**: The content transformation functionality accessible only to Admin and Creator roles
- **Content_Intelligence_Feature**: The content analysis functionality accessible to all User roles
- **Feature_Access_Event**: A recorded instance of a User accessing a Feature, including timestamp and user_id
- **User_Specific_Alert**: An alert that relates to activities performed by a specific User
- **Aggregated_Metric**: A statistical measure computed across all Users, visible only to Admin
- **Lock_Icon**: A visual indicator showing that a Feature is inaccessible to the current User
- **Usage_Count**: The total number of times a User has accessed a specific Feature
- **Last_Used_Timestamp**: The most recent time a User accessed a specific Feature
- **Profile_Settings**: The user interface section where Users can view their account information and preferences
- **Feature_Usage_History_Table**: The database table storing Feature_Access_Events
- **User_Preferences_Table**: The database table storing personalization settings for each User


## Requirements

### Requirement 1: Universal Content Intelligence Access

**User Story:** As a Viewer, I want to access the Content Intelligence feature, so that I can analyze content even with read-only permissions.

#### Acceptance Criteria

1. THE Access_Control_Manager SHALL grant access to Content_Intelligence_Feature for all User roles
2. WHEN a Viewer navigates to Content_Intelligence_Feature, THE Dashboard SHALL display the full content analysis interface
3. WHEN a Viewer submits content for analysis, THE Dashboard SHALL process the analysis request
4. THE Access_Control_Manager SHALL store analysis results with the Viewer's user_id in the ashoka_contentint table

### Requirement 2: Transform Feature Access Restriction

**User Story:** As a system administrator, I want to restrict Transform feature access to Admin and Creator roles only, so that Viewers cannot modify or transform content.

#### Acceptance Criteria

1. THE Access_Control_Manager SHALL grant access to Transform_Feature only when the User role is "admin" OR "creator"
2. WHEN a Viewer attempts to navigate to Transform_Feature, THE Dashboard SHALL prevent navigation to the Transform tab
3. WHEN a Viewer hovers over the Transform tab, THE Dashboard SHALL display a Lock_Icon with tooltip text "You don't have access"
4. WHEN a Viewer clicks on the Transform tab, THE Dashboard SHALL display a notification message "Access denied: Transform feature requires admin or creator role"
5. WHEN an Admin OR Creator navigates to Transform_Feature, THE Dashboard SHALL display the full transformation interface

### Requirement 3: Feature Usage Tracking

**User Story:** As a system, I want to track when users access features, so that I can provide personalized dashboard experiences and usage analytics.

#### Acceptance Criteria

1. WHEN a User navigates to any Feature, THE Feature_Usage_Tracker SHALL record a Feature_Access_Event
2. THE Feature_Usage_Tracker SHALL store the user_id in each Feature_Access_Event
3. THE Feature_Usage_Tracker SHALL store the feature_name in each Feature_Access_Event
4. THE Feature_Usage_Tracker SHALL store the accessed_at timestamp in each Feature_Access_Event
5. THE Feature_Usage_Tracker SHALL persist Feature_Access_Events to the Feature_Usage_History_Table
6. THE Feature_Usage_Tracker SHALL track access for Content_Intelligence_Feature, Transform_Feature, Monitoring, Alerts, and Security Features

### Requirement 4: Recent Features Display in Overview

**User Story:** As a User, I want to see my 3 most recently used features on the Overview panel, so that I can quickly access the features I use most often.

#### Acceptance Criteria

1. WHEN a User views the Overview panel, THE Recent_Features_Panel SHALL query Feature_Access_Events for the current user_id
2. THE Recent_Features_Panel SHALL display the 3 most recently accessed Features ordered by Last_Used_Timestamp descending
3. WHEN a User has accessed fewer than 3 Features, THE Recent_Features_Panel SHALL display only the Features the User has accessed
4. WHEN a User has not accessed any Features, THE Recent_Features_Panel SHALL display a message "Start using features to see your recent activity"
5. FOR EACH displayed Feature, THE Recent_Features_Panel SHALL show the feature name
6. FOR EACH displayed Feature, THE Recent_Features_Panel SHALL show the feature icon
7. FOR EACH displayed Feature, THE Recent_Features_Panel SHALL show the Last_Used_Timestamp formatted as relative time
8. FOR EACH displayed Feature, THE Recent_Features_Panel SHALL show the Usage_Count for that Feature
9. WHEN a User clicks on a Feature card in Recent_Features_Panel, THE Dashboard SHALL navigate to that Feature

### Requirement 5: Recent Features in Profile Settings

**User Story:** As a User, I want to view my feature usage history in my profile settings, so that I can understand my usage patterns.

#### Acceptance Criteria

1. WHEN a User opens Profile_Settings, THE Dashboard SHALL display a "Recent Features" section
2. THE Profile_Settings SHALL query Feature_Access_Events for the current user_id
3. THE Profile_Settings SHALL display the 3 most recently accessed Features ordered by Last_Used_Timestamp descending
4. FOR EACH displayed Feature, THE Profile_Settings SHALL show the feature name
5. FOR EACH displayed Feature, THE Profile_Settings SHALL show the Last_Used_Timestamp formatted as absolute date and time
6. FOR EACH displayed Feature, THE Profile_Settings SHALL show the total Usage_Count for that Feature
7. WHEN a User has not accessed any Features, THE Profile_Settings SHALL display "No feature usage recorded yet"

### Requirement 6: User-Specific Alert Filtering

**User Story:** As a User, I want to see only alerts related to my activities, so that I can focus on issues relevant to my work without being overwhelmed by system-wide alerts.

#### Acceptance Criteria

1. WHEN a User views the Alerts panel, THE Alert_Filter SHALL query alerts where the user_id matches the current User's user_id
2. THE Alert_Filter SHALL include alerts for Content Intelligence analyses performed by the current User
3. THE Alert_Filter SHALL include alerts for Transform operations created by the current User
4. THE Alert_Filter SHALL include alerts for quality issues detected in the current User's content
5. THE Alert_Filter SHALL include alerts for rate limit warnings specific to the current User
6. THE Alert_Filter SHALL exclude alerts related to other Users' activities
7. WHEN displaying alert metrics, THE Dashboard SHALL show "Your content quality score" instead of generic labels
8. WHEN displaying alert metrics, THE Dashboard SHALL show "Your recent analyses" instead of generic labels
9. WHEN a User has no User_Specific_Alerts, THE Dashboard SHALL display "No alerts for your account"

### Requirement 7: Admin Aggregated Metrics View

**User Story:** As an Admin, I want to view aggregated metrics for all users, so that I can monitor system-wide usage and performance.

#### Acceptance Criteria

1. WHEN an Admin views the Monitoring panel, THE Metrics_Aggregator SHALL compute metrics across all Users
2. THE Metrics_Aggregator SHALL include the Admin's own metrics in the aggregation
3. THE Metrics_Aggregator SHALL display total analysis count across all Users
4. THE Metrics_Aggregator SHALL display total transformation count across all Users
5. THE Metrics_Aggregator SHALL display average quality scores by User
6. THE Metrics_Aggregator SHALL display Feature usage statistics aggregated by User
7. THE Monitoring panel SHALL provide a user filter dropdown to view specific User metrics
8. WHEN an Admin selects a User from the filter dropdown, THE Dashboard SHALL display metrics for only that User
9. WHEN an Admin selects "All Users" from the filter dropdown, THE Dashboard SHALL display aggregated metrics
10. WHEN a Creator OR Viewer views the Monitoring panel, THE Dashboard SHALL display only the current User's metrics

### Requirement 8: Feature Usage History Database Schema

**User Story:** As a system, I want to persist feature usage data in a structured format, so that I can query and analyze usage patterns efficiently.

#### Acceptance Criteria

1. THE Feature_Usage_History_Table SHALL have a column "usage_id" of type VARCHAR as the primary key
2. THE Feature_Usage_History_Table SHALL have a column "user_id" of type VARCHAR
3. THE Feature_Usage_History_Table SHALL have a column "feature_name" of type VARCHAR
4. THE Feature_Usage_History_Table SHALL have a column "accessed_at" of type TIMESTAMP
5. THE Feature_Usage_History_Table SHALL have an index on (user_id, accessed_at) for efficient querying
6. THE Feature_Usage_History_Table SHALL have an index on (feature_name, accessed_at) for analytics queries

### Requirement 9: User Preferences Database Schema

**User Story:** As a system, I want to store user personalization preferences, so that I can maintain user-specific dashboard configurations.

#### Acceptance Criteria

1. THE User_Preferences_Table SHALL have a column "user_id" of type VARCHAR as the primary key
2. THE User_Preferences_Table SHALL have a column "preferences_json" of type JSON to store flexible preference data
3. THE User_Preferences_Table SHALL have a column "updated_at" of type TIMESTAMP
4. THE Dashboard SHALL initialize default preferences when a new User account is created

### Requirement 10: Feature Access Event Generation

**User Story:** As a developer, I want feature access events to be generated automatically, so that usage tracking is consistent and requires no manual intervention.

#### Acceptance Criteria

1. WHEN the Dashboard renders the Content_Intelligence_Feature panel, THE Feature_Usage_Tracker SHALL generate a Feature_Access_Event
2. WHEN the Dashboard renders the Transform_Feature panel, THE Feature_Usage_Tracker SHALL generate a Feature_Access_Event
3. WHEN the Dashboard renders the Monitoring panel, THE Feature_Usage_Tracker SHALL generate a Feature_Access_Event
4. WHEN the Dashboard renders the Alerts panel, THE Feature_Usage_Tracker SHALL generate a Feature_Access_Event
5. WHEN the Dashboard renders the Security panel, THE Feature_Usage_Tracker SHALL generate a Feature_Access_Event
6. THE Feature_Usage_Tracker SHALL NOT generate duplicate events when a User refreshes data within the same Feature
7. THE Feature_Usage_Tracker SHALL generate a new event only when a User navigates away and returns to a Feature

### Requirement 11: Alert Personalization Labels

**User Story:** As a User, I want alert labels to reflect that they are my personal alerts, so that I understand the alerts are specific to my activities.

#### Acceptance Criteria

1. WHEN displaying content quality metrics in Alerts, THE Dashboard SHALL use the label "Your Content Quality Score"
2. WHEN displaying analysis counts in Alerts, THE Dashboard SHALL use the label "Your Recent Analyses"
3. WHEN displaying transformation counts in Alerts, THE Dashboard SHALL use the label "Your Transformations"
4. WHEN displaying rate limit warnings in Alerts, THE Dashboard SHALL use the label "Your API Usage"
5. WHEN an Admin views Alerts with aggregated data, THE Dashboard SHALL use the label "System-Wide Alerts" in the panel header

### Requirement 12: Admin User Metrics Breakdown

**User Story:** As an Admin, I want to see a breakdown of metrics by individual user, so that I can identify usage patterns and potential issues per user.

#### Acceptance Criteria

1. WHEN an Admin views the Monitoring panel, THE Dashboard SHALL display a "User Metrics Breakdown" section
2. THE User Metrics Breakdown SHALL display a table with columns: Username, Total Analyses, Total Transformations, Avg Quality Score, Last Active
3. THE User Metrics Breakdown SHALL include data for all Users in the system
4. THE User Metrics Breakdown SHALL be sortable by each column
5. WHEN an Admin clicks on a Username in the breakdown table, THE Dashboard SHALL filter all metrics to show only that User's data
6. THE Dashboard SHALL provide a "Reset Filter" button to return to aggregated view

### Requirement 13: Transform Feature Lock Icon Display

**User Story:** As a Viewer, I want to see a clear visual indicator that Transform is locked, so that I understand why I cannot access it without attempting to click.

#### Acceptance Criteria

1. WHEN a Viewer views the Dashboard navigation, THE Dashboard SHALL display a Lock_Icon next to the Transform tab label
2. THE Lock_Icon SHALL be visually distinct with a lock symbol
3. WHEN a Viewer hovers over the Lock_Icon, THE Dashboard SHALL display a tooltip within 200 milliseconds
4. THE tooltip SHALL contain the text "You don't have access"
5. THE Transform tab SHALL have reduced opacity to indicate disabled state for Viewers
6. WHEN an Admin OR Creator views the Dashboard navigation, THE Dashboard SHALL NOT display a Lock_Icon next to the Transform tab

### Requirement 14: Usage Count Calculation

**User Story:** As a system, I want to accurately calculate feature usage counts, so that users see correct statistics about their feature usage.

#### Acceptance Criteria

1. WHEN calculating Usage_Count for a Feature, THE Dashboard SHALL count all Feature_Access_Events for the current user_id and feature_name
2. THE Dashboard SHALL update Usage_Count in real-time when a new Feature_Access_Event is recorded
3. THE Dashboard SHALL display Usage_Count as an integer value
4. WHEN a Feature has never been accessed by a User, THE Dashboard SHALL display Usage_Count as 0

### Requirement 15: Alert Source User Association

**User Story:** As a system, I want all alert sources to be associated with the user who triggered them, so that alerts can be filtered by user context.

#### Acceptance Criteria

1. WHEN the Dashboard generates an alert from a Content Intelligence analysis, THE Dashboard SHALL associate the alert with the user_id from the ashoka_contentint table
2. WHEN the Dashboard generates an alert from a Transform operation, THE Dashboard SHALL associate the alert with the user_id from the transform_history table
3. WHEN the Dashboard generates an alert from a quality issue, THE Dashboard SHALL associate the alert with the user_id of the content owner
4. WHEN the Dashboard generates an alert from a rate limit event, THE Dashboard SHALL associate the alert with the user_id from the youtube_rate_limits table
5. THE Dashboard SHALL store the user_id in the alert metadata for filtering purposes

