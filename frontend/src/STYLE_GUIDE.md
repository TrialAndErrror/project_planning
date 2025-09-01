# Style Guide

## Overview
This document describes the CSS architecture and styling conventions used in the Project Planning application.

## File Structure
- `style.css` - Main stylesheet with global styles, components, and utilities

## CSS Architecture

### 1. CSS Variables (Custom Properties)
All colors, spacing, and common values are defined as CSS variables in the `:root` selector:

```css
:root {
  --primary-color: #2c3e50;
  --secondary-color: #34495e;
  --accent-color: #3498db;
  --success-color: #27ae60;
  --warning-color: #f39c12;
  --danger-color: #e74c3c;
  --text-color: #333;
  --text-muted: #6c757d;
  --border-color: #dee2e6;
  --background-color: #f8f9fa;
  --card-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  --transition-speed: 0.3s;
}
```

### 2. Organization
The CSS is organized into logical sections:

1. **Global Styles** - Base styles, typography, layout
2. **Components** - Cards, buttons, forms, modals
3. **Utilities** - Helper classes for spacing, alignment, etc.
4. **Animations** - Keyframes and animation classes
5. **Responsive Design** - Media queries for different screen sizes
6. **Custom Components** - Project-specific styles
7. **Accessibility** - Focus states, screen reader support
8. **Print Styles** - Print-specific styling

## Key Features

### Bootstrap 5 Integration
- Complements Bootstrap 5 classes
- Enhances Bootstrap components with custom styling
- Maintains Bootstrap's responsive grid system

### Modern CSS Features
- CSS Variables for theming
- Flexbox and Grid layouts
- Smooth transitions and animations
- Mobile-first responsive design

### Accessibility
- Proper focus states
- Screen reader support
- High contrast colors
- Keyboard navigation support

## Usage Examples

### Buttons
```html
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-success">Success Button</button>
```

### Cards
```html
<div class="card">
  <div class="card-header">Card Title</div>
  <div class="card-body">Card content</div>
</div>
```

### Status Badges
```html
<span class="status-badge status-in-progress">In Progress</span>
<span class="status-badge status-completed">Completed</span>
```

### Utility Classes
```html
<div class="d-flex justify-content-between align-items-center">
  <span class="text-muted">Muted text</span>
  <div class="spinner"></div>
</div>
```

## Color Palette

### Primary Colors
- **Primary**: #2c3e50 (Dark Blue)
- **Secondary**: #34495e (Darker Blue)
- **Accent**: #3498db (Bright Blue)

### Status Colors
- **Success**: #27ae60 (Green)
- **Warning**: #f39c12 (Orange)
- **Danger**: #e74c3c (Red)

### Neutral Colors
- **Light**: #ecf0f1 (Light Gray)
- **Dark**: #2c3e50 (Dark Blue)
- **Text**: #333 (Dark Gray)
- **Text Muted**: #6c757d (Medium Gray)

## Responsive Breakpoints

- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

## Best Practices

1. **Use CSS Variables** for consistent theming
2. **Mobile-first** approach for responsive design
3. **Semantic class names** that describe purpose, not appearance
4. **Progressive enhancement** - styles work without JavaScript
5. **Accessibility first** - ensure all interactive elements are keyboard accessible

## Customization

To customize the theme:

1. Update CSS variables in the `:root` selector
2. Modify component styles as needed
3. Add new utility classes for common patterns
4. Test across different screen sizes and browsers

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox support required
- CSS Variables support required
- Graceful degradation for older browsers
