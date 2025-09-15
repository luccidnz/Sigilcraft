# Overview

Sigilcraft Nexus is a mystical sigil generation web application that offers both free and paid tiers. The application combines spiritual aesthetics with modern web technologies to create personalized sigils (mystical symbols) based on user input phrases. The core concept revolves around transforming text into visually appealing mystical symbols with various "energy vibes" and customization options.

The application implements a freemium model where free users have limited functionality (3 energy types, 512px PNG output, watermarks, cooldowns) while Pro users unlock premium features (all 12+ energy vibes, 2048px + SVG output, batch generation, no watermarks/cooldowns).

**Recent Major Updates (September 15, 2025):**
- Fixed critical JavaScript syntax errors that were causing app crashes
- Enhanced Pro key validation to accept specific keys including "Volt2089"
- Significantly improved sigil generation algorithm with distinct vibe patterns
- Added spiritual features: chakra alignment, lunar phase integration, energy readings
- Implemented AI-powered intention analysis for vibe recommendations
- Upgraded visual design with glassmorphism, aurora effects, and mystical animations
- Fixed gallery modal opening issues
- Enhanced each of the 12 vibes with unique visual patterns and effects

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Single Page Application (SPA)**: Built with vanilla JavaScript, HTML5, and CSS3
- **Responsive Design**: Mobile-first approach with mystical/spiritual theming
- **State Management**: Client-side state management for user preferences, gallery, and Pro status
- **Modular Structure**: Organized into separate concerns (UI, API communication, state management)
- **Progressive Enhancement**: Core functionality works without JavaScript, enhanced features require it

## Backend Architecture
- **Flask Framework**: Python-based REST API server with CORS enabled
- **Modular Design**: Separation of concerns with multiple Python modules
- **Request/Response Pattern**: Standard HTTP API endpoints for sigil generation and configuration
- **Performance Monitoring**: Built-in request tracking and rate limiting capabilities
- **Error Handling**: Comprehensive logging and error recovery mechanisms

## Authentication & Authorization
- **Cookie-based Sessions**: HTTP-only cookies for secure Pro status persistence
- **Pro Key System**: Secret key validation for Pro feature unlocking
- **Client-side Flags**: Local storage backup for Pro status (with server validation)
- **Rate Limiting**: Built-in cooldown system for free users

## Data Storage Strategy
- **Stateless Design**: No persistent database required for core functionality
- **Client-side Storage**: Gallery and preferences stored in browser localStorage
- **Session Management**: Server-side session handling for Pro status
- **File System**: Static assets served directly from filesystem

## Content Generation Pipeline
- **Text Processing**: Phrase-to-sigil transformation algorithms
- **Image Generation**: PIL-based graphics generation with multiple output formats
- **Batch Processing**: Pro users can generate multiple sigils simultaneously
- **Format Support**: PNG (multiple resolutions) and SVG output options

# External Dependencies

## Python Backend Dependencies
- **Flask 2.3.0+**: Web framework and HTTP server
- **Flask-CORS 4.0.0+**: Cross-origin resource sharing handling
- **Pillow 10.0.0+**: Image processing and generation library
- **Gunicorn 21.0.0+**: Production WSGI server
- **pytest 7.4.0+**: Testing framework

## Frontend Dependencies
- **Google Fonts**: Cinzel and Orbitron font families for mystical typography
- **Browser APIs**: localStorage, fetch, Canvas API for enhanced functionality

## Payment Integration
- **Stripe Checkout**: Payment processing for Pro upgrades (placeholder implementation)
- **Custom Pro Key System**: Manual key distribution post-purchase

## Deployment & Infrastructure
- **Replit Platform**: Primary hosting and development environment
- **Static File Serving**: Direct filesystem serving for public assets
- **Environment Variables**: Configuration through .env files
- **Process Management**: Gunicorn for production deployment

## Development & Testing Tools
- **pytest**: Comprehensive test suite with performance tracking
- **Semgrep**: Static analysis and security scanning
- **psutil**: System monitoring and performance metrics
- **Logging**: Multi-level logging with file and console output