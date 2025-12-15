# Frontend Setup Guide

This is the frontend for the Educational Document Management System built with React, Vite, and Tailwind CSS.

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Backend server running on port 5000 (or update the API URL)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Update the `.env` file with your backend API URL (default is `http://localhost:5000`)

## Development

Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

```bash
npm run preview
```

## Features

- User authentication (Login/Register)
- Document upload with metadata
- Document listing and search
- User profile management
- Responsive design with Tailwind CSS
- Protected routes

## Tech Stack

- React 19
- Vite
- React Router v7
- Axios
- Tailwind CSS v4
