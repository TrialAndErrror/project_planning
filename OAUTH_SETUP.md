# OAuth Setup Guide

This guide will help you set up Google OAuth for the Project Planning application.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Project Planning OAuth")
5. Click "Create"

## Step 2: Enable Google+ API

1. In your new project, go to "APIs & Services" > "Library"
2. Search for "Google+ API" or "Google Identity"
3. Click on "Google Identity" or "Google+ API"
4. Click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Project Planning"
   - User support email: Your email
   - Developer contact information: Your email
   - Save and continue through the other sections

4. Back in "Create OAuth client ID":
   - Application type: "Web application"
   - Name: "Project Planning Web Client"
   - Authorized redirect URIs: `http://localhost:3000/oauth/callback`
   - Click "Create"

5. Copy the **Client ID** and **Client Secret** (you'll need these later)

## Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp backend/env.example backend/.env
   ```

2. Edit `backend/.env` and add your Google OAuth credentials:
   ```
   GOOGLE_CLIENT_ID=your-google-client-id-here
   GOOGLE_CLIENT_SECRET=your-google-client-secret-here
   ```

## Step 5: Restart the Application

1. Restart the backend container to load the new environment variables:
   ```bash
   docker-compose restart backend
   ```

## Step 6: Test OAuth

1. Visit http://localhost:3000
2. Click "Login" or "Register"
3. Click "Continue with Google"
4. You should be redirected to Google's consent screen
5. After authorization, you'll be redirected back to the application

## Troubleshooting

### "Google OAuth not configured" Error
- Make sure you've created the `.env` file in the `backend/` directory
- Verify that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set correctly
- Restart the backend container after making changes

### "Invalid redirect URI" Error
- Make sure the redirect URI in Google Cloud Console exactly matches: `http://localhost:3000/oauth/callback`
- Check for extra spaces or typos

### "Access blocked" Error
- Make sure you've enabled the Google+ API or Google Identity API
- Check that your OAuth consent screen is properly configured

## Production Deployment

For production deployment, you'll need to:

1. Update the redirect URI in Google Cloud Console to your production domain
2. Update the `OAUTH_CALLBACK_URL` in your environment variables
3. Use environment-specific Google OAuth credentials

## Security Notes

- Never commit your `.env` file to version control
- Keep your Client Secret secure
- Use different OAuth credentials for development and production
- Regularly rotate your OAuth credentials

## Adding Other OAuth Providers

The application is designed to easily support additional OAuth providers. To add providers like GitHub, Facebook, or Microsoft:

1. Add the provider configuration to `SOCIALACCOUNT_PROVIDERS` in `backend/core/settings.py`
2. Create corresponding OAuth views in `backend/users/oauth_views.py`
3. Add the provider to the frontend OAuth buttons
4. Update the environment variables with the new provider's credentials 