#!/usr/bin/env python3
"""TTS MCP Server using FastMCP for SDLC progress announcements"""

import boto3
import os
import platform
import tempfile
from mcp.server.fastmcp import FastMCP

# Create FastMCP server for stdio transport
mcp = FastMCP("tts-mcp-server", instructions="Text-to-Speech MCP Server using AWS Polly")

def play_audio(audio_data: bytes) -> None:
    """Play audio using system player."""
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_data)
            temp_file = f.name
        
        system = platform.system()
        if system == 'Darwin':
            os.system(f'afplay {temp_file}')
        elif system == 'Windows':
            os.system(f'start {temp_file}')
        elif system == 'Linux':
            os.system(f'xdg-open {temp_file}')
        else:
            print(f"Warning: Unsupported OS {system}, audio file saved to {temp_file}")
            return
    finally:
        if temp_file:
            try:
                os.remove(temp_file)
            except Exception:
                pass  # Silently ignore cleanup failures

@mcp.tool()
def announce_progress(message: str, voice_id: str = "Joanna") -> str:
    """
    Announce SDLC workflow progress via text-to-speech using AWS Polly.
    
    Args:
        message: Progress message to announce
        voice_id: AWS Polly voice ID (Joanna, Matthew, Salli)
    
    Returns:
        Status message indicating success or failure
    """
    if os.environ.get('ENABLE_TTS', 'true').lower() != 'true':
        return f"TTS disabled: {message}"
    
    try:
        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            Text=message,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='generative'
        )
        
        audio_data = response['AudioStream'].read()
        response['AudioStream'].close()
        
        play_audio(audio_data)
        return f"✓ Announced: {message}"
        
    except polly.exceptions.InvalidSsmlException:
        return f"TTS Error: Invalid message format"
    except polly.exceptions.TextLengthExceededException:
        return f"TTS Error: Message too long"
    except Exception as e:
        return f"TTS Error: {str(e)}"

def main():
    """Main entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    # Run with stdio transport for Q CLI integration
    main()
