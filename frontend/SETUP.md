# Medical AI Frontend - Vue.js

This is a Vue 3-based frontend for the Medical AI Diagnosis Assistant.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

## Project Structure

```
src/
├── main.js           # Vue app entry point
├── App.vue           # Root component
├── style.css         # Global styles
└── components/       # Vue components
    ├── Header.vue        # Header with navigation
    ├── HeroSection.vue   # Hero banner
    ├── FeaturesSection.vue # Features showcase
    ├── FeatureCard.vue   # Reusable feature card
    ├── CtaSection.vue    # Call-to-action section
    ├── ChatSection.vue   # Medical image analysis & chat
    └── Footer.vue        # Footer
```

## Features

- **Medical Image Analysis**: Upload and analyze medical images using the AI backend
- **AI Chat**: Interactive chat interface for health-related questions
- **Responsive Design**: Mobile-friendly UI
- **Component-Based**: Modular Vue components for easy maintenance

## API Configuration

The app automatically detects the API endpoint:
- **Development**: Uses relative paths (assumes backend on same server)
- **Production**: Uses `https://medical-ai-bot-mtg8.onrender.com`

## Technologies

- **Vue 3**: Progressive JS framework
- **Vite**: Fast build tool
- **Scoped CSS**: Component-specific styling
