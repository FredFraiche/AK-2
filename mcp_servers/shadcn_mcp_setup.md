# Shadcn MCP Server Setup

## Overview
The Shadcn MCP Server allows AI assistants to browse, search, and install components from shadcn/ui and other compatible registries using natural language.

## Prerequisites
- Node.js installed
- A project with `components.json` (shadcn/ui project)

## Quick Setup

### Initialize with CLI
From your project root:
```powershell
npx shadcn@latest mcp init --client vscode
```

### Manual Setup for VS Code (mcp.json format)
Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

## Configuring Multiple Registries
Add custom registries to your `components.json`:

```json
{
  "registries": {
    "@acme": "https://registry.acme.com/{name}.json",
    "@internal": {
      "url": "https://internal.company.com/{name}.json",
      "headers": {
        "Authorization": "Bearer ${REGISTRY_TOKEN}"
      }
    }
  }
}
```

## Authentication for Private Registries
Set environment variables in `.env.local`:
```
REGISTRY_TOKEN=your_token_here
API_KEY=your_api_key_here
```

## Use Cases
- Browse available components from registries
- Search for specific components
- Install components using natural language
- Access multiple registries (public, private, third-party)

## Example Prompts

### Browse & Search
- "Show me all available components in the shadcn registry"
- "Find me a login form from the shadcn registry"

### Install Components
- "Add the button component to my project"
- "Create a login form using shadcn components"
- "Install the dialog and card components"

### Work with Namespaces
- "Show me components from acme registry"
- "Install @internal/auth-form"
- "Build me a landing page using hero, features and testimonials sections from the acme registry"

## Troubleshooting

### MCP Not Responding
1. Verify MCP server is enabled in VS Code
2. Restart VS Code after configuration changes
3. Ensure `shadcn` is accessible via npx

### Registry Access Issues
1. Check `components.json` for correct registry URLs
2. Test authentication with environment variables
3. Verify registry is online and accessible
4. Check namespace syntax: `@namespace/component`

### Installation Failures
1. Ensure valid `components.json` file exists
2. Verify target directories exist
3. Check write permissions
4. Review required dependencies

### No Tools or Prompts
1. Clear npx cache: `npx clear-npx-cache`
2. Re-enable MCP server in VS Code
3. Check logs: View -> Output -> Select "MCP: project-*"

## Supported Registries
- **shadcn/ui Registry** - Default registry with all shadcn/ui components
- **Third-Party Registries** - Any registry following shadcn registry specification
- **Private Registries** - Your company's internal component libraries
- **Namespaced Registries** - Multiple registries with `@namespace` syntax

## Links
- [Official Documentation](https://ui.shadcn.com/docs/mcp)
- [Registry Documentation](https://ui.shadcn.com/docs/registry)
- [Authentication Guide](https://ui.shadcn.com/docs/registry/authentication)
- [MCP Specification](https://modelcontextprotocol.io/)
