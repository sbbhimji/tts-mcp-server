#!/usr/bin/env python3
"""TTS MCP Server using FastMCP for SDLC progress announcements"""

import boto3
import os
import tempfile
from playsound3 import playsound
from mcp.server.fastmcp import FastMCP

# Create FastMCP server for stdio transport
mcp = FastMCP("tts-mcp-server", instructions="Text-to-Speech MCP Server using AWS Polly")

def play_audio(audio_data: bytes) -> str:
    """Play audio using playsound library (OS-independent)."""
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_data)
            temp_file = f.name
        
        playsound(temp_file)
        return None
    except Exception as e:
        return f"Failed to play audio: {str(e)}"
    finally:
        if temp_file:
            try:
                os.remove(temp_file)
            except Exception:
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
        
        error = play_audio(audio_data)
        if error:
            return f"TTS Error: {error}"
        
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
