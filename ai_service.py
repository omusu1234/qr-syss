import os
import json
import time
from google import genai
from google.genai import types

def get_ai_client():
    """Initialize and return the Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def triage_support_ticket(message):
    """
    Sends the support ticket message to Gemini and asks it to classify it.
    Returns a dictionary with 'category' and 'priority'.
    """
    client = get_ai_client()
    if not client:
        return {"category": "General", "priority": "Medium"}
        
    prompt = f"""
    You are an AI assistant for a university QR Attendance System. 
    A lecturer has submitted the following support ticket:
    "{message}"
    
    Please classify this ticket.
    1. Category must be one of: "Login Issue", "Hardware", "Bug", or "General".
    2. Priority must be one of: "High", "Medium", or "Low".
    
    Return ONLY a valid JSON object matching exactly this schema:
    {{"category": "Category Here", "priority": "Priority Here"}}
    """
    
    try:
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
        except Exception as primary_e:
            if "503" in str(primary_e):
                print("Google API busy, retrying once...")
                time.sleep(1.5)
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
            else:
                raise primary_e
                
        # Parse the JSON response
        response_text = response.text.strip()
        # Clean up Markdown JSON formatting if Gemini wraps it
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text)
        
        # Validate output
        valid_categories = ["Login Issue", "Hardware", "Bug", "General"]
        valid_priorities = ["High", "Medium", "Low"]
        
        if result.get("category") not in valid_categories:
            result["category"] = "General"
        if result.get("priority") not in valid_priorities:
            result["priority"] = "Medium"
            
        return result
    except Exception as e:
        print(f"AI Triage Error: {e}")
        return {"category": "General", "priority": "Medium"}

def chat_with_lecturer(query, context_data):
    """
    Handles a query from a lecturer on the dashboard, providing the system's current context.
    """
    client = get_ai_client()
    if not client:
        return "AI features are currently unavailable because the API key is not configured."
        
    system_instruction = f"""
    You are the AI Assistant for the 'QR Attendance System', built to help university lecturers manage their classes.
    Here is the current database context for this lecturer (in JSON format):
    {json.dumps(context_data, indent=2)}
    
    Answer the lecturer's query based ONLY on this context. 
    Keep your answers concise, professional, and directly address their data.
    If they ask something unrelated to the attendance system or context data, politely inform them you can only assist with their attendance records.
    """
    
    try:
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=query,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                )
            )
        except Exception as primary_e:
            if "503" in str(primary_e):
                print("Google API busy, retrying once...")
                time.sleep(1.5)
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=query,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                    )
                )
            else:
                raise primary_e
                
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg:
            return "Google's AI servers are currently experiencing high demand. Please try again in a few moments."
        print(f"AI Chat Error: {error_msg}")
        return f"Sorry, I encountered an error: {error_msg}"

def generate_early_warning_report(student_stats):
    """
    Generates a personalized early warning report based on student attendance statistics.
    """
    client = get_ai_client()
    if not client:
        return "Early Warning System requires an active API key."
        
    if not student_stats:
        return "No student data available to generate a report."
        
    prompt = f"""
    You are an Early Warning Analytics AI for a university.
    Analyze the following list of students with the lowest attendance rates:
    {json.dumps(student_stats, indent=2)}
    
    Write a brief, professional summary (1-2 paragraphs) for the lecturer. 
    Highlight which students are at the highest risk (e.g. less than 75% attendance) and suggest a brief course of action (e.g. reaching out to them).
    Do not use markdown headers, just plain text with simple formatting.
    """
    
    try:
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
        except Exception as primary_e:
            if "503" in str(primary_e):
                print("Google API busy, retrying once...")
                time.sleep(1.5)
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
            else:
                raise primary_e
                
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg:
            return "Google's AI servers are extremely busy right now. Please check back in a few minutes."
        print(f"AI Analytics Error: {error_msg}")
        return f"Analytics engine is currently down. Error: {error_msg}"
