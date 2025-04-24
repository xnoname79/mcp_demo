import os
import subprocess

import httpx
from langchain_core.tools import BaseTool


class PlayBase64AudioTool(BaseTool):
    name: str = "Convert text to speech and play audio."
    description: str = "Convert text to speech and play its audio."

    def _run(self, text: str, language: str) -> str:
        base_url = os.getenv("TTS_REST_CONNECTION", "http://localhost:50051")
        endpoint = f"{base_url.rstrip('/')}/api/gtts/speak/"

        with httpx.Client(timeout=10.0) as client:
            # adjust payload key if your API expects something else
            resp = client.get(endpoint, params={"text": text, "language": language})
            resp.raise_for_status()
            audio_bytes = resp.content

        filename = "tts_output.mp3"
        with open(filename, "wb") as f:
            f.write(audio_bytes)

        player = None
        for cmd in ("mpv", "mpg123", "aplay"):
            if (
                subprocess.call(
                    ["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                == 0
            ):
                player = cmd
                break

        if player:
            subprocess.call([player, filename])
            return f"🔊 Played audio for: “{text}”"
        else:
            return f"✅ Audio saved to {filename} (no player found)"

    async def _arun(self, text: str) -> str:
        raise NotImplementedError("Async not supported in this example")
