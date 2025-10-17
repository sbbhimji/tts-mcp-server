# Text-to-Speech MCP Server for SDLC Progress Announcements

A Model Context Protocol (MCP) server that provides real-time audio feedback during the Software Development Lifecycle workflow using AWS Polly.

## Overview

This TTS MCP server integrates with the CLI Agent Orchestrator to announce progress at key milestones throughout the SDLC workflow, providing audio feedback without requiring constant screen monitoring.

## Features

- **Real-time Progress Announcements**: Audio notifications at each SDLC stage
- **AWS Polly Integration**: High-quality neural text-to-speech
- **Cross-platform Support**: Works on macOS, Linux (Windows via WSL)
- **Configurable**: Enable/disable via environment variable
- **Multiple Voices**: Support for different AWS Polly voices

## Prerequisites

- Python 3.8+
- `uv` package manager installed ([Installation guide](https://github.com/astral-sh/uv))
- AWS account with Polly access
- AWS credentials configured (`aws configure`)
- IAM permissions for `polly:SynthesizeSpeech`
- Audio output device

## Installation

The TTS MCP server is automatically installed and managed by `uv` when you install the supervisor agent. No manual installation or virtual environment setup is required.

### Update supervisor.md with Absolute Path

Edit `supervisor.md` and replace the path with your absolute path:

```yaml
tts-mcp-server:
  type: stdio
  command: uv
  args:
    - "run"
    - "python"
    - "/Users/yourusername/echo-reinvent/echo-architect/tts-mcp-server/server.py"
```

### Install Supervisor Agent

```bash
cao install ../cli_agent_orchestrator/agent_store/supervisor.md
```

## Usage

### Launch Supervisor with TTS

```bash
cao launch --agents supervisor
```

### Give It a Task

```
"Create a social media app like Facebook"
```

You'll hear announcements like:
- 🔊 "Starting new project social-media-app"
- 🔊 "Creating specifications for your project"
- 🔊 "Specifications completed. Beginning parallel development phase"
- 🔊 "Building AWS solution with CDK and React"
- 🔊 "Generating architecture diagrams"
- 🔊 "Calculating AWS cost estimates"
- 🔊 "Creating user stories in Jira"
- 🔊 "All parallel tasks completed"
- 🔊 "Publishing artifacts to GitHub repository"
- 🔊 "Project completed successfully. Total time: X minutes"

## Configuration

### Enable/Disable TTS

```bash
# Enable (default)
export ENABLE_TTS=true

# Disable
export ENABLE_TTS=false
```

### Available Voices

- **Joanna** (Female, US) - Default, general progress
- **Matthew** (Male, US) - Error notifications
- **Salli** (Female, US) - Completion messages

[Full list of AWS Polly voices](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html)

## Troubleshooting

### No Audio Output

**Check AWS credentials:**
```bash
aws sts get-caller-identity
```

**Verify Polly access:**
```bash
aws polly describe-voices --language-code en-US
```

**Test audio system:**
```bash
# macOS
afplay /System/Library/Sounds/Ping.aiff

# Linux
speaker-test -t wav -c 2
```

### TTS Not Working


**Check environment:**
```bash
echo $ENABLE_TTS  # Should be 'true' or empty
```

**Reinstall supervisor:**
```bash
cao install ../cli_agent_orchestrator/agent_store/supervisor.md
```

### Permission Errors

Add Polly permissions to your IAM user/role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "polly:SynthesizeSpeech",
      "Resource": "*"
    }
  ]
}
```

### Module Not Found Error

Verify the absolute path in supervisor.md is correct:
```bash
cat ../cli_agent_orchestrator/agent_store/supervisor.md | grep server.py
```

Reinstall supervisor agent:
```bash
cao install ../cli_agent_orchestrator/agent_store/supervisor.md
```

## Files

```
tts-mcp-server/
├── server.py              # FastMCP TTS server
├── pyproject.toml         # Python project configuration for uv
├── requirements.txt       # Python dependencies
├── .gitignore            # Git exclusions
└── README.md             # This file
```

## Important Notes

- ✅ **No virtual environment needed** - `uv` manages dependencies automatically
- ✅ **Use absolute paths** - Update supervisor.md with your full path to server.py
- ✅ **Dependencies auto-installed** - `uv` handles everything when supervisor launches

