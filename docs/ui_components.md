# PetRescue UI Component Guide

This document describes the key UI components used throughout the PetRescue application.

## Color Palette

### Primary Colors
- **Primary Blue**: #2563EB (Pet reports, links)
- **Success Green**: #16A34A (Approve actions, success messages)
- **Warning Yellow**: #F59E0B (Pending status, warnings)
- **Danger Red**: #DC2626 (Reject actions, errors)

### Gradient Buttons
- **Lost Pet Button**: Red gradient (#F87171 to #DC2626)
- **Found Pet Button**: Green gradient (#22C55E to #16A34A)
- **Search Button**: Yellow gradient (#FACC15 to #EAB308)

## Button Styles

### Primary Buttons
```css
.btn-primary {
  background: linear-gradient(to right, #2563EB, #1D4ED8);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Gradient Buttons
```css
.hero-btn-lost {
  background: linear-gradient(to right, #F87171, #DC2626);
  border: none;
  color: white;
  padding: 0.875rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-btn-lost:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(248, 113, 113, 0.4);
  background: linear-gradient(to right, #DC2626, #F87171);
}
```

## Status Badges

### Lost Status
```css
.status-badge-lost {
  background-color: #FECACA;
  color: #DC2626;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
}
```

### Found Status
```css
.status-badge-found {
  background-color: #BBF7D0;
  color: #16A34A;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
}
```

### Adoptable Status
```css
.status-badge-adoptable {
  background-color: #BFDBFE;
  color: #2563EB;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
}
```

## Cards

### Pet Cards
```css
.pet-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  background: white;
  transform: translateZ(0);
  will-change: transform;
}

.pet-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12) !important;
}
```

### Submission Cards
```css
.submission-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.submission-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}
```

## Forms

### Input Fields
```css
.form-control, .form-select {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.form-control:focus, .form-select:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 0.25rem rgba(37, 99, 235, 0.25);
  background-color: white;
}
```

## Dropdowns

### Status Dropdown
```css
.dropdown-menu {
  min-width: 220px;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 1050;
  padding: 0.5rem 0;
  margin-top: 0.25rem;
}

.dropdown-item {
  padding: 0.75rem 1.25rem;
  transition: all 0.2s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  color: #495057;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #212529;
}
```

## Responsive Design

### Mobile Breakpoints
```css
/* Mobile first approach */
@media (max-width: 768px) {
  .hero-buttons {
    flex-direction: column;
    gap: 1rem !important;
  }
  
  .hero-btn-primary,
  .hero-btn-success,
  .hero-btn-outline {
    width: 100%;
    justify-content: center;
  }
  
  .dropdown-menu {
    position: fixed !important;
    inset: auto auto 20px 20px !important;
    width: calc(100vw - 40px) !important;
    max-width: 350px !important;
    max-height: 70vh !important;
    overflow-y: auto;
  }
}
```

## Animations

### Fade-in Effects
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}
```

## Typography

### Font Family
```css
body {
  font-family: 'Poppins', sans-serif;
}
```

### Heading Styles
```css
.hero-title {
  color: #2c3e50;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.section-badge {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: rgba(76, 175, 80, 0.1);
  color: #2563EB;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

This guide ensures consistent UI implementation across the application and helps maintain a cohesive design language.