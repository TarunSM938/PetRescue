# PetRescue Admin Guide

This guide provides comprehensive instructions for administrators to manage the PetRescue platform effectively.

## Table of Contents
1. [Admin Dashboard Overview](#admin-dashboard-overview)
2. [Managing Pet Requests](#managing-pet-requests)
3. [Notification System](#notification-system)
4. [Contact Submissions](#contact-submissions)
5. [Activity Logs](#activity-logs)
6. [Handling Conflicts](#handling-conflicts)
7. [Operational Runbook](#operational-runbook)

## Admin Dashboard Overview

The admin dashboard is the central hub for managing all aspects of the PetRescue platform. Upon logging in as an administrator, you'll be directed to the dashboard which provides:

- Summary statistics of platform activity
- Quick access to pending requests
- Notification center
- Quick links to all admin sections

### Navigation Menu
The left sidebar provides access to:
- **Dashboard**: Overview and statistics
- **Pending Requests**: Reports awaiting review
- **Accepted Requests**: Approved reports
- **Rejected Requests**: Denied reports
- **Contact Submissions**: User messages and reports
- **Notifications**: System notifications
- **Activity Logs**: Historical activity tracking

## Managing Pet Requests

### Pending Requests
Pending requests are new pet reports that require admin review:

1. Navigate to "Pending Requests" in the sidebar
2. Review each request carefully:
   - Verify the information provided
   - Check uploaded images for appropriateness
   - Ensure contact information is valid
3. Take one of the following actions:
   - **Accept**: Approve the report for public visibility
   - **Reject**: Deny the report (provide reason if appropriate)
   - **View Details**: See additional information about the report

### Status Management
Each request can have one of three statuses:
- **Pending**: Awaiting admin review
- **Accepted**: Verified and visible in public search
- **Rejected**: Not approved for public visibility

### Accepting Requests
To accept a request:
1. Click "Accept" on the request card
2. The request status will change to "Accepted"
3. The associated pet will become visible in public search results
4. The reporter will receive a notification (if implemented)

### Rejecting Requests
To reject a request:
1. Click "Reject" on the request card
2. Provide a reason for rejection (optional but recommended)
3. The request status will change to "Rejected"
4. The associated pet will not be visible in public search results

## Notification System

### Notification Panel
The notification panel provides real-time alerts for:
- New pet reports requiring review
- User contact submissions
- System issues or maintenance requirements

### Managing Notifications
1. Click the bell icon in the top navigation bar
2. View unread notifications
3. Click on any notification to view details
4. Notifications can be marked as read automatically or manually

### Notification Types
- **Lost Pet Report**: New lost pet report submitted
- **Found Pet Report**: New found pet report submitted
- **Contact Submission**: User has sent a message
- **Issue Report**: User has reported a platform issue

## Contact Submissions

Users can submit various types of messages through the contact system:

### Submission Types
- **General Inquiry**: Questions or feedback
- **Issue Report**: Technical problems or bugs
- **Support Request**: Help with using the platform

### Managing Submissions
1. Navigate to "Contact Submissions" in the sidebar
2. View all submissions in a card-based layout
3. Filter submissions by:
   - Status (Pending, Reviewed, Closed)
   - Type (General, Issue, Support)
   - Search terms
4. Update submission status:
   - **Pending**: New submission awaiting review
   - **Reviewed**: Submission has been reviewed
   - **Closed**: Issue resolved or no further action needed

### Responding to Submissions
While the platform doesn't currently support direct messaging, you should:
1. Review each submission carefully
2. Update the status appropriately
3. For urgent issues, contact the user directly if possible
4. Keep notes on actions taken for future reference

## Activity Logs

Activity logs track all significant actions on the platform:

### Log Types
- **Created**: New pet report or user account
- **Edited**: Modifications to existing records
- **Status Changed**: Request status updates
- **Deleted**: Removed records

### Viewing Activity Logs
1. Navigate to "Activity Logs" in the sidebar
2. Filter logs by:
   - Date range
   - Activity type
   - User or pet involved
3. Click on any log entry to view detailed information

### Log Information
Each log entry includes:
- Timestamp of the activity
- Type of activity performed
- User who performed the action
- Details about what was changed

## Handling Conflicts

### Simultaneous Updates
When multiple admins work on the same request:
1. The system will show the most recent update
2. Previous changes are preserved in activity logs
3. Communicate with other admins to avoid conflicts

### Disputed Reports
For reports that may be fraudulent or disputed:
1. Mark as "Pending Review" if not already
2. Gather additional information if possible
3. Consult with other administrators
4. Make a final decision based on available evidence

### Recommended Workflow
1. **Verification First**: Always verify information before accepting
2. **Conservative Approach**: When in doubt, reject and request more information
3. **Documentation**: Keep notes on decisions for future reference
4. **Communication**: Coordinate with other admins on complex cases

## Operational Runbook

### Daily Tasks
- Review pending requests (aim for 24-hour turnaround)
- Check contact submissions
- Monitor activity logs for unusual patterns
- Review system notifications

### Weekly Tasks
- Generate usage reports
- Review rejected requests for patterns
- Update documentation if needed
- Coordinate with development team on issues

### Monthly Tasks
- Review platform performance metrics
- Assess user feedback trends
- Plan for capacity upgrades if needed
- Update operational procedures

### Handling Spam Reports
1. Identify spam patterns (repeated submissions, inappropriate content)
2. Reject spam reports with appropriate status
3. Consider implementing IP-based restrictions if needed
4. Document spam patterns for future prevention

### Backfilling Historical Data
If new data fields are added (e.g., "helped" flag):
1. Create a migration script for bulk updates
2. Test on staging environment first
3. Schedule during low-traffic periods
4. Monitor for issues after implementation

### Emergency Procedures
**Database Issues**:
1. Switch to read-only mode if possible
2. Notify users of maintenance
3. Restore from latest backup
4. Verify data integrity

**Security Breach**:
1. Immediately change all admin passwords
2. Review access logs for suspicious activity
3. Notify affected users
4. Implement additional security measures

## Best Practices

### Review Process
1. **Thoroughness**: Check all information for accuracy
2. **Consistency**: Apply standards uniformly
3. **Timeliness**: Process requests within 24 hours
4. **Documentation**: Keep notes on complex decisions

### Communication
1. **Professionalism**: Maintain professional tone in all interactions
2. **Clarity**: Provide clear reasons for rejections
3. **Empathy**: Remember users are often in distress about their pets
4. **Promptness**: Respond to internal communications quickly

### Quality Assurance
1. **Regular Audits**: Periodically review accepted/rejected requests
2. **Peer Review**: Have another admin review complex cases
3. **Process Improvement**: Continuously refine procedures
4. **Training**: Keep up to date with platform changes

## Technical Information

### Health Check Endpoints
- `/health/`: Basic system health
- `/admin/`: Admin panel accessibility
- `/api/health/`: API endpoint status

### Monitoring
- Database performance
- Response times
- Error rates
- User authentication success rates

## Support Resources

For technical issues not covered in this guide:
- Contact the development team
- Check system documentation
- Review recent code changes
- Consult with senior administrators

Thank you for your dedication to helping pets find their way home!