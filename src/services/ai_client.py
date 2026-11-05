"""Groq API client for Mr. Computer."""

import httpx
from typing import List, Dict
from src.utils.config import config
from src.utils.logger import log

async def get_ai_response(history: List[Dict[str, str]]) -> str:
    """Send conversation history to Groq and get a response."""
    
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": config.GROQ_MODEL,
        "messages": history,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(config.GROQ_API_URL, headers=headers, json=payload)
            
            if response.status_code != 200:
                log.error(f"Groq API error: {response.status_code} - {response.text}")
                return "⚠️ Sorry, I'm having trouble connecting to my AI brain right now. Please try again later."
                
            data = response.json()
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not reply:
                return "⚠️ I couldn't generate a response. Please try again."
                
            return reply.strip()
            
    except Exception as e:
        log.error(f"AI Client Exception: {e}")
        return "⚠️ Connection error. Please try again."
