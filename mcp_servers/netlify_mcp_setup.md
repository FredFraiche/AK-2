# Netlify MCP Server Setup

## Overview
The Netlify MCP Server enables AI agents to build, deploy, and manage Netlify projects using natural language.

## Prerequisites
- Node.js 22 or higher
- A Netlify account
- Netlify CLI (recommended): `npm install -g netlify-cli`

## Installation

### For VS Code (mcp.json format)
Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "netlify": {
      "command": "npx",
      "args": ["-y", "@netlify/mcp"],
      "env": {
        "NETLIFY_PERSONAL_ACCESS_TOKEN": "${env:NETLIFY_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

## Authentication Setup

### Get Netlify Personal Access Token (PAT)
1. Go to [Netlify User Settings - OAuth](https://app.netlify.com/user/applications#personal-access-tokens)
2. Click "New access token"
3. Copy the token securely
4. Add to your environment variables or `.env` file:
   ```
   NETLIFY_PERSONAL_ACCESS_TOKEN=your_token_here
   ```

### Alternative: Use Netlify CLI auth
```powershell
netlify login
netlify status
```

## Use Cases
- Create, manage, and deploy projects
- Modify Netlify access controls
- Install or uninstall Netlify extensions
- Fetch user and team information
- Manage form submissions
- Create environment variables and secrets

## Example Prompts
- "Create a new Netlify site from my project"
- "Deploy my current project to Netlify"
- "Show me my Netlify sites"
- "Add an environment variable for my API key"

## Troubleshooting

### Node Version Issues
Check your Node version:
```powershell
node --version
```

If using nvm:
```powershell
nvm install 22
nvm use 22
```

### Authentication Issues
Test Netlify CLI auth:
```powershell
netlify status
```

## Links
- [Official Documentation](https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/)
- [GitHub Repository](https://github.com/netlify/netlify-mcp)
- [Netlify CLI Docs](https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli)
