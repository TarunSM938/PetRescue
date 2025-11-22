# PetRescue Test Matrix

## Overview
This document provides a comprehensive test matrix for the PetRescue project, covering all main user journeys, admin workflows, and cross-browser compatibility.

## Test Environment
- **Operating Systems**: Windows 10, macOS, Ubuntu 20.04
- **Browsers**: Chrome (latest), Firefox (latest), Edge (latest), Safari (latest)
- **Devices**: Desktop, Tablet, Mobile (iOS and Android)
- **Screen Sizes**: 320px, 375px, 414px, 768px, 1024px, 1200px, 1440px

## End-to-End Testing

### 1. User Registration and Login Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC001 | 1. Navigate to registration page<br>2. Fill valid registration form<br>3. Submit form | User successfully registered and redirected to login page |  |  |  |
| TC002 | 1. Navigate to login page<br>2. Enter valid credentials<br>3. Click login | User successfully logged in and redirected to home page |  |  |  |
| TC003 | 1. Navigate to login page<br>2. Enter invalid credentials<br>3. Click login | Error message displayed, user remains on login page |  |  |  |
| TC004 | 1. Navigate to registration page<br>2. Submit empty form | Validation errors displayed for all required fields |  |  |  |
| TC005 | 1. Navigate to registration page<br>2. Enter existing username/email<br>3. Submit form | Error message indicating duplicate user |  |  |  |

### 2. Report Lost Pet Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC006 | 1. Login as regular user<br>2. Navigate to "Report Lost Pet"<br>3. Fill valid form with image<br>4. Submit | Pet report created, request in pending status, admin notified |  |  |  |
| TC007 | 1. Login as regular user<br>2. Navigate to "Report Lost Pet"<br>3. Submit empty form | Validation errors displayed for required fields |  |  |  |
| TC008 | 1. Login as regular user<br>2. Navigate to "Report Lost Pet"<br>3. Upload invalid file type<br>4. Submit | Error message for invalid file type |  |  |  |
| TC009 | 1. Login as regular user<br>2. Navigate to "Report Lost Pet"<br>3. Upload oversized image<br>4. Submit | Error message for file size limit |  |  |  |
| TC010 | 1. Login as regular user<br>2. Navigate to "Report Lost Pet"<br>3. Fill form with extremely long text<br>4. Submit | Validation errors for text length limits |  |  |  |

### 3. Report Found Pet Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC011 | 1. Login as regular user<br>2. Navigate to "Report Found Pet"<br>3. Fill valid form with images<br>4. Submit | Pet report created, request in pending status, admin notified |  |  |  |
| TC012 | 1. Login as regular user<br>2. Navigate to "Report Found Pet"<br>3. Submit empty form | Validation errors displayed for required fields |  |  |  |
| TC013 | 1. Login as regular user<br>2. Navigate to "Report Found Pet"<br>3. Upload multiple valid images<br>4. Submit | All images uploaded successfully |  |  |  |

### 4. Admin Review and Approval Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC014 | 1. Login as admin<br>2. Navigate to pending requests<br>3. Approve a request | Request status changes to accepted, pet becomes visible in search |  |  |  |
| TC015 | 1. Login as admin<br>2. Navigate to pending requests<br>3. Reject a request | Request status changes to rejected, pet not visible in search |  |  |  |
| TC016 | 1. Login as two different admins simultaneously<br>2. Both attempt to update same request | System handles concurrent updates gracefully |  |  |  |

### 5. Search and Filter Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC017 | 1. Navigate to search page<br>2. Enter search criteria<br>3. Submit search | Relevant pets displayed in results |  |  |  |
| TC018 | 1. Navigate to search page<br>2. Enter non-matching criteria<br>3. Submit search | "No results found" message displayed |  |  |  |
| TC019 | 1. Search for pet<br>2. Click on pet result<br>3. View similar pets | Similar pets displayed based on criteria |  |  |  |

### 6. Profile Management Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC020 | 1. Login as user<br>2. Navigate to profile<br>3. Edit profile information<br>4. Save changes | Profile updated successfully |  |  |  |
| TC021 | 1. Login as user<br>2. Navigate to "My Reports"<br>3. Edit pending request | Request updated successfully |  |  |  |
| TC022 | 1. Login as user<br>2. Navigate to "My Reports"<br>3. Delete pending request | Request deleted successfully |  |  |  |

### 7. Notification System Flow

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC023 | 1. New pet reported<br>2. Admin views notifications | Notification appears in admin panel |  |  |  |
| TC024 | 1. Admin clicks notification<br>2. Marks as read | Notification marked as read, count decreases |  |  |  |

## Cross-Browser Compatibility Testing

| Browser | Device | Screen Size | Test Cases | Pass/Fail | Notes |
|---------|--------|-------------|------------|-----------|-------|
| Chrome | Desktop | 1200px | All flows |  |  |
| Firefox | Desktop | 1200px | All flows |  |  |
| Edge | Desktop | 1200px | All flows |  |  |
| Safari | Desktop | 1200px | All flows |  |  |
| Chrome | Mobile | 375px | All flows |  |  |
| Safari | Mobile | 375px | All flows |  |  |

## Edge Cases and Negative Testing

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC025 | 1. Upload extremely large payload | Server rejects with appropriate error |  |  |  |
| TC026 | 1. Attempt to access admin pages as regular user | Redirected to login or access denied |  |  |  |
| TC027 | 1. Submit form with JavaScript disabled | Form still validates server-side |  |  |  |
| TC028 | 1. Simultaneously submit multiple requests | System handles without data corruption |  |  |  |

## Performance Testing

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC029 | 1. Load home page with 1000+ pets | Page loads within 3 seconds |  |  |  |
| TC030 | 1. Search with complex filters | Results return within 2 seconds |  |  |  |

## Security Testing

| Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|-----------|-------|-----------------|---------------|-----------|-------|
| TC031 | 1. Attempt SQL injection in search | Input sanitized, no database access |  |  |  |
| TC032 | 1. Attempt XSS in form fields | Input sanitized, no script execution |  |  |  |
| TC033 | 1. Access admin endpoints without authentication | Access denied |  |  |  |

## Mobile Responsiveness Testing

| Screen Size | Test Cases | Pass/Fail | Notes |
|-------------|------------|-----------|-------|
| 320px | All flows |  |  |
| 375px | All flows |  |  |
| 414px | All flows |  |  |
| 768px | All flows |  |  |
| 1024px | All flows |  |  |

## Test Results Summary

| Category | Total Tests | Passed | Failed | Pass Rate |
|----------|-------------|--------|--------|-----------|
| Functional | 25 |  |  |  |
| Cross-Browser | 6 |  |  |  |
| Edge Cases | 4 |  |  |  |
| Performance | 2 |  |  |  |
| Security | 3 |  |  |  |
| Mobile | 5 |  |  |  |
| **Total** | **45** |  |  |  |

## Screenshots of Critical Flows

(Screenshots will be attached here during testing)

## Bugs Found and Fixed

(Bugs discovered during testing will be documented here with file/line references)