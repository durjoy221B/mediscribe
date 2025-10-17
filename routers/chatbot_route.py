from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agents import Agent, Runner, SQLiteSession
from fastapi.responses import JSONResponse


from services.chat_service import create_gemini_model, tavily_search
from config.prompt import CHATBOT_PROMPT

templates = Jinja2Templates(directory="templates")

chatbot_router = APIRouter()

@chatbot_router.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    request.app.state.medicine_information = getattr(request.app.state, "extra_info_prompt", None)

    return templates.TemplateResponse("chatbot.html", {"request": request})


@chatbot_router.post("/chatbot/message")
async def chatbot_message(request: Request):
    try:
        # Parse the incoming JSON request
        data = await request.json()
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id")
        
        if not user_message:
            return JSONResponse(
                content={"error": "Message cannot be empty"},
                status_code=400
            )
        
        # Generate session ID if not provided
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Get medicine information from app state
        medicine_info = getattr(request.app.state, "medicine_information", None)
        
        # Create instructions with medicine info if available
        instructions = CHATBOT_PROMPT
        if medicine_info:
            instructions += f"\n\nmedicine information: {medicine_info}"
        
        # Create Gemini model
        gemini_model = await create_gemini_model()
        
        # Create agent
        agent = Agent(
            name="Medical Assistant",
            instructions=instructions,
            model=gemini_model,
            tools=[tavily_search],
        )
        
        # Create or retrieve session for this conversation
        db_session = SQLiteSession(session_id, "conversation_history.db")
        
        # Run the agent with user input
        result = await Runner.run(
            agent,
            user_message,
            session=db_session
        )
        
        return JSONResponse(
            content={
                "response": result.final_output,
                "session_id": session_id
            },
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500
        )

