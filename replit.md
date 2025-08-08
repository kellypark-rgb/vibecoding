# Overview

This is a Korean N-line poetry (행시) generator web application built with Streamlit and powered by Google's Gemini AI. The application allows users to input Korean words and generates traditional Korean acrostic poetry where each line starts with the corresponding character from the input word. The poetry follows specific formatting rules with bracketed characters and maintains thematic coherence across lines.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit for web interface
- **Design Pattern**: Single-page application with real-time interaction
- **User Interface**: Simple input field for Korean words with instant poetry generation
- **Caching Strategy**: Resource caching for Gemini client initialization to optimize API usage

## Backend Architecture
- **Runtime**: Python-based application
- **API Integration**: Direct integration with Google Gemini 2.5 Flash model
- **Poetry Generation Logic**: Custom prompt engineering for Korean acrostic poetry (행시) with specific formatting rules
- **Error Handling**: Environment variable validation and user-friendly error messages

## Authentication & Configuration
- **API Authentication**: Environment variable-based API key management for Gemini
- **Security**: API keys stored as environment variables, not hardcoded

## Poetry Generation Rules
- Each character of input word starts a new line in brackets
- Lines maintain 10-20 character length for readability
- Thematic coherence across all lines
- Traditional Korean poetic structure

# External Dependencies

## AI Services
- **Google Gemini API**: Primary AI service for Korean poetry generation
  - Model: gemini-2.5-flash
  - Purpose: Natural language processing and creative text generation
  - Authentication: API key-based

## Python Libraries
- **Streamlit**: Web application framework for user interface
- **google-genai**: Official Google Generative AI Python client
- **os**: Environment variable management

## Environment Requirements
- **GEMINI_API_KEY**: Required environment variable for Google Gemini API access