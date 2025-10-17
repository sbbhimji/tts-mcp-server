#!/usr/bin/env python3
"""TTS MCP Server using FastMCP for SDLC progress announcements"""

import boto3
import os
import platform
import tempfile
from mcp.server.fastmcp import FastMCP

# Create FastMCP server for stdio transport
mcp = FastMCP("tts-mcp-server")

def play_audio(audio_data: bytes) -> None:
    """Play audio using system player."""
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
    
    # Clean up temp file
    try:
        os.remove(temp_file)
    except:
        pass

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
    # Check if TTS is enabled
    if os.environ.get('ENABLE_TTS', 'true').lower() != 'true':
        return f"TTS disabled: {message}"
    
    try:
        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            Text=message,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural'
        )
        
        audio_data = response['AudioStream'].read()
        play_audio(audio_data)
        
        return f"✓ Announced: {message}"
    except Exception as e:
        return f"TTS Error: {str(e)}"

if __name__ == "__main__":
    # Run with stdio transport for Q CLI integration
    mcp.run(transport="stdio")
