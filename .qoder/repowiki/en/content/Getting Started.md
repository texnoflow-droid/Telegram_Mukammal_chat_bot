# Getting Started

<cite>
**Referenced Files in This Document**
- [index.html](file://index.html)
- [main.css](file://main.css)
- [main.js](file://main.js)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [First-Time Usage](#first-time-usage)
5. [Core Features Overview](#core-features-overview)
6. [Step-by-Step Instructions](#step-by-step-instructions)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Browser Compatibility](#browser-compatibility)
9. [Conclusion](#conclusion)

## Introduction
This guide helps you set up and use the Vinetttka teacher directory project. It covers prerequisites, local development setup, first-time usage, and troubleshooting. The project is a static website featuring a YouTube video background, a responsive teacher gallery, and a modal system for viewing teacher photos.

## Prerequisites
- Basic web development knowledge:
  - Understanding of HTML, CSS, and JavaScript fundamentals
  - How to open an HTML file in a browser
  - How to use developer tools to inspect elements and debug
- Browser compatibility:
  - Modern browsers (Chrome, Firefox, Safari, Edge) recommended
  - JavaScript enabled
  - Pop-ups and autoplay policies may affect the video background depending on browser settings

## Local Development Setup
Follow these steps to run the project locally:

1. **File placement**
   - Place all files in the same folder:
     - index.html
     - main.css
     - main.js
   - Ensure the HTML links to CSS and JS match the filenames and relative paths.

2. **Open in a browser**
   - Double-click index.html to open it in your default browser.
   - Alternatively, right-click the file and choose "Open with" your preferred browser.

3. **Server configuration options**
   - Static file serving:
     - No server required for local testing. The project loads resources via relative paths.
   - Alternative local servers:
     - Python (if installed): python -m http.server 8000 (then visit http://localhost:8000)
     - Node.js (if installed): npx serve (then visit http://localhost:3000)
   - Notes:
     - The project uses relative paths and does not require a complex build process.

4. **Assets and media**
   - The HTML references external YouTube video content and local image files.
   - Ensure internet connectivity for the YouTube video background.
   - For local images, confirm the image paths referenced in the HTML exist in the project folder.

**Section sources**
- [index.html:1-106](file://index.html#L1-L106)
- [main.css:1-517](file://main.css#L1-L517)
- [main.js:1-83](file://main.js#L1-L83)

## First-Time Usage
When you open the project for the first time:

1. Initial page load
   - The page displays a full-screen YouTube video background with a vignette overlay.
   - The main content container shows the school year badge and teacher sections.

2. Navigation through the teacher gallery
   - Scroll to view the leadership section and the teachers grid.
   - Hover over teacher cards to see elevation effects.
   - Click any teacher card to open the modal with a larger view.

3. Interaction with the modal system
   - Click a teacher card to open the modal.
   - Close the modal by clicking the X button, clicking outside the image, or pressing the Escape key.

**Section sources**
- [index.html:9-106](file://index.html#L9-L106)
- [main.js:2-58](file://main.js#L2-L58)

## Core Features Overview
- Responsive design:
  - The layout adapts to desktop, laptop, tablet, and mobile screens using CSS Grid and media queries.
- Video background:
  - A YouTube embed plays automatically with muted audio and loop controls.
- Teacher gallery:
  - Two sections: leadership cards and a responsive grid of teachers.
- Modal system:
  - Fullscreen modal with image and caption, keyboard support, and smooth scrolling behavior.

**Section sources**
- [index.html:21-93](file://index.html#L21-L93)
- [main.css:105-147](file://main.css#L105-L147)
- [main.css:207-491](file://main.css#L207-L491)
- [main.js:2-82](file://main.js#L2-L82)

## Step-by-Step Instructions

### Viewing the Video Background
1. Open index.html in a browser.
2. Confirm the video fills the screen with a vignette overlay.
3. If the video does not play:
   - Check browser autoplay policies and permissions.
   - Ensure the browser allows embedded content from YouTube.
   - Verify internet connectivity.

### Navigating the Responsive Grid Layout
1. On desktop:
   - The leadership section shows four cards arranged in a grid.
   - The teachers grid adjusts to fit available space with consistent gaps.
2. On tablets and phones:
   - The grid reflows to fewer columns based on viewport width.
   - Cards adapt to smaller heights for better readability.
3. Hover and click:
   - Cards elevate slightly on hover.
   - Click any card to open the modal.

### Understanding the Modal Functionality
1. Opening the modal:
   - Click a teacher card to display the modal with the selected image and caption.
   - The modal overlays the page with a dark backdrop and centered content.
2. Closing the modal:
   - Click the X button in the top-right corner.
   - Click outside the image area.
   - Press the Escape key.
3. Behavior:
   - Scrolling is disabled when the modal is open.
   - Images fade in smoothly when loaded.

**Section sources**
- [index.html:58-92](file://index.html#L58-L92)
- [main.css:149-205](file://main.css#L149-L205)
- [main.js:9-58](file://main.js#L9-L58)

## Troubleshooting Guide

Common issues and resolutions:

- Video background not playing
  - Cause: Autoplay restrictions or blocked embedded content.
  - Resolution: Allow autoplay and embedded content in your browser settings; ensure internet connectivity.

- Images not loading
  - Cause: Incorrect image paths or missing files.
  - Resolution: Verify that referenced image paths exist in the project folder. The HTML references both absolute and relative paths.

- Modal does not open
  - Cause: JavaScript errors preventing event listeners from attaching.
  - Resolution: Open browser developer tools (F12) and check the console for errors. Ensure main.js is loaded and there are no network errors.

- Modal does not close
  - Cause: Event listener not firing or CSS conflicts.
  - Resolution: Test clicking the X button, clicking outside the image, and pressing Escape. If still failing, reload the page and check for JavaScript errors.

- Layout appears broken on small devices
  - Cause: Media query conditions or viewport meta tag issues.
  - Resolution: Ensure the viewport meta tag is present (already included). Resize the browser window to test responsiveness.

- Scrolling issues when modal is open
  - Cause: Body overflow not restored after closing.
  - Resolution: Close the modal using the X button or Escape key. The script restores scrolling automatically.

**Section sources**
- [index.html:3-8](file://index.html#L3-L8)
- [main.js:2-82](file://main.js#L2-L82)

## Browser Compatibility
- Supported browsers:
  - Chrome, Firefox, Safari, Edge
- Known considerations:
  - Autoplay policy varies by browser and device settings.
  - Some browsers may require user gesture for autoplay.
  - CSS Grid and modern JavaScript features are widely supported in current browsers.

## Conclusion
You now have the essentials to run and use the Vinetttka teacher directory project locally. Explore the responsive layout, enjoy the video background, and interact with the teacher gallery and modal system. If you encounter issues, use the troubleshooting steps and consult your browser’s developer tools for diagnostics.