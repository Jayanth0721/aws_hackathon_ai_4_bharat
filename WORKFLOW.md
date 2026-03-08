# Ashoka Platform - Complete Workflows & Use Cases

> **Comprehensive guide to using Ashoka for content governance, analysis, generation, and transformation**

---

## Table of Contents

1. [Introduction](#introduction)
2. [User Roles & Permissions](#user-roles--permissions)
3. [Core Workflows](#core-workflows)
4. [Use Case Scenarios](#use-case-scenarios)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Introduction

Ashoka is designed to streamline content governance workflows from creation to publication. This document outlines complete workflows for different user types and use cases, helping you maximize the platform's capabilities.

### Platform Philosophy

**Govern → Analyze → Generate → Transform → Monitor → Secure**

Every piece of content flows through this pipeline, ensuring quality, compliance, and optimization at every step.

### Recent UI/UX Improvements (March 2026)

The dashboard has been enhanced with several user experience improvements:

**Navigation & Layout:**
- Session timer relocated to header (top-right) for better visibility
- Command Center displays date-time with calendar icon and role badge
- Personalized workspace indicator with purple text
- Help section streamlined with full-width quick access panels

**Content Intelligence:**
- Clear button now resets both input and analysis results
- Analysis headers improved for better readability (black text)
- Smoother interaction flow

**Monitoring & Alerts:**
- Role-based visibility (Monitoring hidden for standard users)
- Auto-refresh only (manual refresh buttons removed)
- System Health consolidated in Alerts panel
- Enhanced alert visibility with minimum warning count

**Overview Panel:**
- Focused on platform capabilities and content metrics
- System Health moved to Alerts for better context
- Enhanced platform details with Core Services guide

---

## User Roles & Permissions

### Default Test Accounts

For testing and demonstration purposes, the platform includes:

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| admin | admin123 | Admin | Full platform access |
| creator | creator123 | Creator | Content creation access |
| guruji | guru1 | User | Standard user access |
| demo | demo123 | User | Demo/read-only access |

### 1. User Role (Standard Access)
**Who**: Content reviewers, analysts, viewers

**Can Access:**
- ✅ Content Intelligence (analysis only)
- ✅ Monitoring dashboard
- ✅ Alerts panel
- ✅ Profile and settings

**Cannot Access:**
- ❌ AI Content Generator
- ❌ Multi-Platform Transformer
- ❌ Security dashboard

**Typical Workflow:**
```
Login → Analyze Content → Review Quality Scores → Monitor Alerts → Logout
```

### 2. Creator Role (Content Creation)
**Who**: Content creators, marketers, social media managers

**Can Access:**
- ✅ Everything User role has
- ✅ AI Content Generator (text & images)
- ✅ Multi-Platform Transformer
- ✅ Transform history

**Cannot Access:**
- ❌ Security dashboard
- ❌ Content restrictions management

**Typical Workflow:**
```
Login → Generate Content → Analyze Quality → Transform for Platforms → Monitor Performance → Logout
```

### 3. Admin Role (Full Access)
**Who**: Platform administrators, compliance officers, security teams

**Can Access:**
- ✅ Everything Creator role has
- ✅ Security dashboard
- ✅ Content restrictions management
- ✅ User activity monitoring
- ✅ Security event logs

**Typical Workflow:**
```
Login → Set Restrictions → Monitor Security → Review User Activity → Manage Governance → Logout
```

---

## Core Workflows

### Workflow 1: Content Analysis & Quality Check

**Objective**: Analyze content for quality, sentiment, and compliance before publishing

**Steps:**

1. **Login to Dashboard**
   ```
   Navigate to: http://localhost:8080
   Enter credentials → Verify OTP → Access dashboard
   ```

2. **Navigate to Content Intelligence**
   ```
   Click: Content Intelligence tab (sidebar)
   ```

3. **Check AI Engine Usage (NEW)**
   ```
   View real-time API quota:
   - Engine 1: Gemini (X/50 used)
   - Engine 2: Sarvam AI (X/1000 used)
   - Engine 3: Gemini Backup (X/50 used)
   
   Select engine:
   - Auto (Recommended): System chooses best available
   - Manual: Select specific engine
   
   Note: Quotas reset every 24 hours at midnight
   ```

4. **Choose Input Method**
   
   **Option A: Text Input**
   ```
   1. Select "TEXT" tab
   2. Enter or paste content
   3. Click "Submit Content for Analysis"
   4. Wait for AI processing (5-10 seconds)
   ```

   **Option B: File Upload**
   ```
   1. Select appropriate tab (IMAGE, AUDIO, VIDEO, DOCUMENT)
   2. Click "Choose File" or drag & drop
   3. Upload file
   4. Click "Analyze [Type]"
   5. Wait for processing (10-30 seconds)
   ```

4. **Review Analysis Results**
   ```
   Results display inline with:
   - Summary
   - Sentiment (Positive/Negative/Neutral)
   - Confidence score
   - Keywords
   - Topics
   - Quality Score (0-100%)
   ```

5. **Interpret Quality Score**
   ```
   85-100%: Excellent - Ready to publish
   70-84%:  Good - Minor improvements recommended
   60-69%:  Fair - Review and enhance
   <60%:    Poor - Significant revision needed
   ```

6. **Take Action Based on Results**
   ```
   High Quality (>85%):
   → Proceed to transformation
   → Publish directly
   
   Medium Quality (70-84%):
   → Review suggestions
   → Make minor edits
   → Re-analyze
   
   Low Quality (<70%):
   → Major revision needed
   → Check sentiment and keywords
   → Rewrite and re-analyze
   ```

**Expected Outcome**: Content quality validated, ready for next steps

**Time Required**: 1-2 minutes per content piece

**API Usage**: 1 request per analysis (tracked in real-time dashboard)

---

### Workflow 2: AI Content Generation

**Objective**: Create professional content using AI

**Steps:**

1. **Access AI Content Generator**
   ```
   Navigate to: Content Intelligence → AI Content Generator section
   ```

2. **Select Generation Type**
   ```
   Choose one:
   - Text/Notes: Professional writing
   - Image: AI-generated visuals
   - Video: (Coming soon)
   ```

3. **For Text Generation:**
   ```
   1. Select "Text/Notes" radio button
   2. Enter detailed prompt:
      Example: "Write a professional email announcing a new product launch"
   3. Click "Generate Content"
   4. Wait 5-15 seconds
   5. Review generated text
   6. Copy or use in transformer
   ```

4. **For Image Generation:**
   ```
   1. Select "Image" radio button
   2. Enter descriptive prompt:
      Example: "Modern office workspace with natural lighting"
   3. Click "Generate Content"
   4. Wait 10-30 seconds (Cloudflare Workers processing)
   5. Review generated image
   6. Download if satisfied
   7. Regenerate if needed
   ```

5. **Quality Check Generated Content**
   ```
   For Text:
   → Click "Analyze This Content" button
   → Review quality score
   → Edit if needed
   
   For Images:
   → Visual inspection
   → Regenerate with refined prompt if needed
   ```

6. **Use Generated Content**
   ```
   Text:
   → Click "Use in Transformer" to adapt for platforms
   → Copy to clipboard for external use
   
   Images:
   → Download to local storage
   → Use in social media posts
   → Include in documents/presentations
   ```

**Expected Outcome**: High-quality AI-generated content ready for use

**Time Required**: 
- Text: 30 seconds - 1 minute
- Images: 1-2 minutes

**Cost**: 
- Text: ~$0.002 per generation (Gemini API)
- Images: FREE (Cloudflare Workers)

---

### Workflow 3: Multi-Platform Content Transformation

**Objective**: Adapt content for different social media platforms

**Prerequisites**: Creator or Admin role

**Steps:**

1. **Access Transformer**
   ```
   Navigate to: Content Intelligence → Multi-Platform Content Transformer
   ```

2. **Enter Original Content**
   ```
   Option A: Type/paste directly
   Option B: Use generated content (click "Use in Transformer")
   Option C: Load from transform history
   ```

3. **Select Target Platforms**
   ```
   Check boxes for:
   ☐ LinkedIn (Professional network)
   ☐ Twitter/X (Short-form, 280 chars)
   ☐ Instagram (Visual-first, hashtags)
   ☐ Facebook (Casual, longer form)
   ☐ Threads (Conversational)
   ```

4. **Choose Tone**
   ```
   Select one:
   ○ Professional: Business, formal
   ○ Casual: Friendly, relaxed
   ○ Storytelling: Narrative, engaging
   ```

5. **Configure Options**
   ```
   ☑ Include Hashtags (recommended for Instagram, Twitter)
   ```

6. **Transform Content**
   ```
   1. Click "Transform Content"
   2. Wait 10-20 seconds (processes all platforms)
   3. Review platform-specific outputs
   ```

7. **Review Platform Outputs**
   ```
   Each platform shows:
   - Adapted content
   - Character count
   - Platform-specific formatting
   - Hashtags (if enabled)
   ```

8. **Copy and Publish**
   ```
   For each platform:
   1. Click copy icon
   2. Paste into platform's posting interface
   3. Add images/media if needed
   4. Schedule or publish immediately
   ```

**Expected Outcome**: Platform-optimized content ready for multi-channel publishing

**Time Required**: 2-3 minutes for all platforms

**Cost**: ~$0.001 per platform (Gemini API)

---

### Workflow 4: Quality Monitoring & Alerts

**Objective**: Track content quality trends and respond to alerts

**Prerequisites**: Creator or Admin role (Monitoring section hidden for User role)

**Steps:**

1. **Access Monitoring Dashboard**
   ```
   Navigate to: Monitoring tab (sidebar)
   Note: Only visible for Creator and Admin roles
   ```

2. **Review Performance Trends**
   ```
   Check 24-hour line graphs for:
   - Quality score trends
   - Content processing rate
   - Success/failure rates
   ```

3. **Analyze Quality Metrics**
   ```
   Review cards showing:
   - Average quality score
   - Quality distribution
   - Risk assessments
   ```

4. **Navigate to Alerts**
   ```
   Click: Alerts tab (sidebar)
   ```

5. **Review Alert Summary**
   ```
   Check counts:
   - Critical: Quality <60% (immediate action)
   - Warnings: Quality <80% (review recommended) - minimum 1 shown
   - Success: Quality ≥85% (good performance)
   ```

6. **Check System Health**
   ```
   In Alerts panel, verify:
   - API: Healthy
   - Database: Healthy
   - AI: Healthy
   ```

7. **Filter Alerts**
   ```
   Use dropdown to filter by:
   - All
   - Critical
   - Warning
   - Info
   - Success
   ```

8. **Respond to Alerts**
   ```
   For Critical Alerts:
   1. Identify affected content
   2. Review quality issues
   3. Take corrective action
   4. Re-analyze content
   
   For Warnings:
   1. Note quality concerns
   2. Plan improvements
   3. Monitor trends
   ```

9. **Auto-Refresh**
   ```
   Wait for automatic refresh (10 minutes)
   Note: Manual refresh buttons removed for cleaner UI
   ```

**Expected Outcome**: Proactive quality management, early issue detection

**Time Required**: 5-10 minutes daily

**UI Notes:**
- Monitoring section only visible for Creator/Admin roles
- System Health moved from Overview to Alerts panel
- Auto-refresh only (no manual refresh buttons)
- Minimum 1 warning always displayed for visibility

---

### Workflow 5: Security & Governance (Admin Only)

**Objective**: Maintain platform security and content governance

**Prerequisites**: Admin role

**Steps:**

1. **Access Security Dashboard**
   ```
   Navigate to: Security tab (sidebar)
   ```

2. **Review Login Activity**
   ```
   Check recent logins:
   - Username
   - IP address
   - Location
   - Status (Success/Failed)
   - Timestamp
   ```

3. **Monitor Security Events**
   ```
   Review events:
   - Password changes
   - OTP generation
   - Session creation
   - Login attempts
   ```

4. **Manage Content Restrictions**
   ```
   1. Scroll to "AI Content Generation Restrictions"
   2. Review existing restrictions
   3. Add new restrictions:
      - Enter keyword/phrase
      - Add description (optional)
      - Click "Add Restriction"
   4. Remove outdated restrictions:
      - Click delete icon
      - Confirm removal
   ```

5. **Test Restrictions**
   ```
   1. Navigate to AI Content Generator
   2. Try generating content with restricted keywords
   3. Verify blocking works
   4. Check error message clarity
   ```

6. **Review User Activity**
   ```
   Monitor:
   - Active sessions
   - Feature usage patterns
   - Content generation frequency
   - Transformation activity
   ```

7. **Audit Trail Review**
   ```
   Periodically check:
   - Security event logs
   - Login patterns
   - Failed authentication attempts
   - Unusual activity
   ```

**Expected Outcome**: Secure platform, compliant content generation

**Time Required**: 10-15 minutes weekly

---

## Use Case Scenarios

### Scenario 1: Social Media Manager - Daily Content Publishing

**Profile**: Sarah, Social Media Manager at a tech startup

**Goal**: Create and publish content across LinkedIn, Twitter, and Instagram

**Workflow:**

```
Morning Routine (30 minutes):

1. Login as Creator
2. Generate AI content:
   - "Write a LinkedIn post about our new AI feature launch"
   - Generate accompanying image: "Modern AI technology interface"
3. Analyze generated text (quality check)
4. Transform for platforms:
   - LinkedIn: Professional tone
   - Twitter: Casual tone
   - Instagram: Storytelling tone
5. Copy platform-specific content
6. Schedule posts in respective platforms
7. Monitor alerts for any quality issues
```

**Result**: 3 platform-optimized posts in 30 minutes

---

### Scenario 2: Content Compliance Officer - Quality Audit

**Profile**: Mike, Compliance Officer at a financial services company

**Goal**: Audit all content for compliance and quality standards

**Workflow:**

```
Weekly Audit (1 hour):

1. Login as Admin
2. Navigate to Monitoring:
   - Review quality trends (past 7 days)
   - Identify content below 70% quality
3. Check Alerts:
   - Filter by "Critical" and "Warning"
   - Document all flagged content
4. Security Dashboard:
   - Review content generation patterns
   - Check for policy violations
   - Update restrictions if needed
5. Generate audit report:
   - Quality metrics
   - Alert summary
   - Compliance status
```

**Result**: Complete compliance audit with actionable insights

---

### Scenario 3: Marketing Team - Campaign Launch

**Profile**: Marketing team launching a new product

**Goal**: Create multi-channel campaign content

**Workflow:**

```
Campaign Creation (2 hours):

1. Team Lead (Admin):
   - Set content restrictions for brand guidelines
   - Define quality thresholds

2. Content Creator 1:
   - Generate blog post content
   - Analyze quality (target: >85%)
   - Refine until quality threshold met

3. Content Creator 2:
   - Generate social media images (5 variations)
   - Download best performers

4. Content Creator 3:
   - Transform blog content for:
     * LinkedIn (professional)
     * Twitter (casual, thread format)
     * Instagram (storytelling + hashtags)
     * Facebook (community-focused)

5. Team Review:
   - Check all content quality scores
   - Review platform adaptations
   - Approve for publishing

6. Monitor:
   - Track quality metrics
   - Respond to alerts
   - Adjust strategy based on insights
```

**Result**: Complete multi-channel campaign with quality assurance

---

### Scenario 4: Content Analyst - Performance Review

**Profile**: Data analyst reviewing content performance

**Goal**: Identify quality trends and optimization opportunities

**Workflow:**

```
Monthly Analysis (2 hours):

1. Login as User
2. Monitoring Dashboard:
   - Export 30-day quality trends
   - Analyze performance graphs
   - Identify patterns

3. Alerts Review:
   - Count critical vs warning alerts
   - Categorize by content type
   - Identify common issues

4. Content Intelligence:
   - Re-analyze top-performing content
   - Compare quality scores
   - Extract success patterns

5. Generate Report:
   - Quality score distribution
   - Alert frequency analysis
   - Recommendations for improvement
   - ROI analysis (cost vs quality)

6. Present Findings:
   - Share insights with team
   - Propose optimization strategies
   - Set quality targets for next month
```

**Result**: Data-driven content strategy improvements

---

### Scenario 5: Startup Founder - Cost-Optimized Content Creation

**Profile**: Founder of a bootstrapped startup

**Goal**: Create high-quality content while minimizing costs

**Workflow:**

```
Weekly Content Creation (1 hour):

1. Login as Creator
2. Generate Images (FREE):
   - Create 5 blog post images
   - Generate social media graphics
   - Download all (no cost)

3. Generate Text Content:
   - Write 1 blog post (~$0.002)
   - Create 3 social posts (~$0.006)
   - Total text cost: ~$0.008

4. Transform Content:
   - Blog → LinkedIn article (~$0.001)
   - Blog → Twitter thread (~$0.001)
   - Blog → Instagram caption (~$0.001)
   - Total transform cost: ~$0.003

5. Analyze Quality:
   - Check all content (~$0.005)

6. Total Weekly Cost: ~$0.016
   Monthly Cost: ~$0.064
   Annual Cost: ~$0.77

7. Monitor Performance:
   - Track quality trends
   - Optimize based on insights
```

**Result**: Professional content creation for <$1/year

---

## Best Practices

### Content Analysis
1. **Always analyze before publishing** - Catch issues early
2. **Target 85%+ quality** - Ensures professional standards
3. **Review sentiment carefully** - Negative sentiment impacts engagement
4. **Check keywords** - Ensure relevance and SEO value
5. **Use analysis history** - Learn from past successes

### AI Generation
1. **Be specific in prompts** - Better prompts = better results
2. **Iterate on images** - Regenerate until satisfied (it's free!)
3. **Analyze generated text** - AI isn't perfect, verify quality
4. **Use restrictions wisely** - Block inappropriate content proactively
5. **Monitor costs** - Track API usage for budgeting

### Content Transformation
1. **Choose appropriate tone** - Match platform culture
2. **Enable hashtags selectively** - Instagram/Twitter benefit most
3. **Review platform outputs** - Ensure context is preserved
4. **Save successful transforms** - Build a template library
5. **Test on small audience first** - Validate before full rollout

### Monitoring & Alerts
1. **Check daily** - Stay on top of quality issues
2. **Respond to critical alerts immediately** - Prevent reputation damage
3. **Track trends** - Identify systematic issues
4. **Set quality thresholds** - Define acceptable standards
5. **Use auto-refresh** - Keep data current

### Security & Governance
1. **Update restrictions regularly** - Adapt to new policies
2. **Audit user activity** - Ensure compliance
3. **Review security events** - Detect anomalies
4. **Backup database** - Protect against data loss
5. **Document policies** - Maintain clear guidelines

---

## Troubleshooting

### Issue: Low Quality Scores

**Symptoms**: Content consistently scores below 70%

**Solutions**:
1. Check sentiment - Avoid negative language
2. Increase content length - Aim for 50+ words
3. Add more keywords - Include relevant terms
4. Diversify topics - Cover multiple related themes
5. Improve confidence - Be more assertive in language

### Issue: Image Generation Fails

**Symptoms**: "Image generation failed" error

**Solutions**:
1. Check internet connection - API requires connectivity
2. Simplify prompt - Avoid overly complex descriptions
3. Wait and retry - Temporary API issues
4. Check logs - Review error details
5. Contact support - If persistent

### Issue: Transform Not Working

**Symptoms**: "Access Restricted" or no output

**Solutions**:
1. Verify role - Need Creator or Admin role
2. Check content length - Minimum 10 words required
3. Select platforms - At least one platform must be checked
4. Review restrictions - Content may be blocked
5. Refresh page - Clear any UI issues

### Issue: Alerts Not Updating

**Symptoms**: Stale alert data

**Solutions**:
1. Click "Refresh Alerts" - Manual refresh
2. Wait for auto-refresh - Updates every 10 minutes
3. Check database connection - Verify connectivity
4. Review logs - Check for errors
5. Restart dashboard - Clear any cache issues

### Issue: Login Problems

**Symptoms**: Cannot login or OTP not working

**Solutions**:
1. Check credentials - Verify username/password
2. Wait for new OTP - Codes expire after 5 minutes
3. Check storage secret - Must be set in .env
4. Clear browser cache - Remove old sessions
5. Use different browser - Test compatibility

---

## Workflow Optimization Tips

### Time-Saving Strategies
1. **Batch processing** - Analyze multiple pieces together
2. **Template reuse** - Save successful transforms
3. **Keyboard shortcuts** - Learn UI navigation
4. **Auto-refresh** - Let system update in background
5. **Parallel workflows** - Multiple team members working simultaneously

### Cost-Saving Strategies
1. **Use image generation** - It's FREE via Cloudflare
2. **Analyze once, transform many** - Reuse analysis results
3. **Set quality thresholds** - Avoid re-analyzing good content
4. **Use restrictions** - Block wasteful API calls
5. **Monitor usage** - Track and optimize spending

### Quality-Improving Strategies
1. **Iterative refinement** - Analyze → Edit → Re-analyze
2. **Learn from history** - Study high-scoring content
3. **Use appropriate tones** - Match platform expectations
4. **Monitor trends** - Adapt to changing standards
5. **Team collaboration** - Share best practices

---

## Conclusion

Ashoka provides a complete content governance workflow from creation to publication. By following these workflows and best practices, you can:

- ✅ Ensure content quality and compliance
- ✅ Optimize costs while maintaining standards
- ✅ Scale content production efficiently
- ✅ Monitor performance proactively
- ✅ Maintain security and governance

For technical details, see [SCRIPTS.md](SCRIPTS.md)

For setup instructions, see [SETUP.md](SETUP.md)

---

**Master these workflows to unlock Ashoka's full potential!**
