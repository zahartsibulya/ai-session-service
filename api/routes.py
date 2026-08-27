from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from db.database import get_db
from db.models import Session, Message
from schemas.pydantic_models import SessionCreate, SessionResponse, MessageCreate, MessageResponse
from services.openai_service import get_chat_response
from core.pricing import calculate_cost, is_model_supported

router = APIRouter(prefix="/api/v1")

@router.post("/sessions", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: DBSession = Depends(get_db)):
    if not is_model_supported(session_data.model_name):
        raise HTTPException(status_code=400, detail=f"Model '{session_data.model_name}' is not supported.")
    
    db_session = Session(
        model_name=session_data.model_name,
        system_prompt=session_data.system_prompt
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, db: DBSession = Depends(get_db)):
    db_session = db.query(Session).filter(Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    active_messages = db.query(Message).filter(
        Message.session_id == session_id, 
        Message.is_archived == False
    ).order_by(Message.created_at).all()
    
    return {
        "id": db_session.id,
        "model_name": db_session.model_name,
        "system_prompt": db_session.system_prompt,
        "total_tokens": db_session.total_tokens,
        "total_cost": db_session.total_cost,
        "active_tokens": db_session.active_tokens,
        "active_cost": db_session.active_cost,
        "created_at": db_session.created_at,
        "messages": active_messages
    }

@router.post("/sessions/{session_id}/reset")
def reset_session(session_id: str, db: DBSession = Depends(get_db)):
    db_session = db.query(Session).filter(Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.query(Message).filter(Message.session_id == session_id).update({"is_archived": True})
    
    db_session.active_tokens = 0
    db_session.active_cost = 0.0
    db.commit()
    return {"status": "success", "message": "Session context reset."}

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
def send_message(session_id: str, message_data: MessageCreate, db: DBSession = Depends(get_db)):
    db_session = db.query(Session).filter(Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    used_model = message_data.model if message_data.model else db_session.model_name
    if not is_model_supported(used_model):
        raise HTTPException(status_code=400, detail=f"Model '{used_model}' is not supported.")

    user_message = Message(session_id=session_id, role="user", content=message_data.content)
    db.add(user_message)
    db.commit()

    history = db.query(Message).filter(
        Message.session_id == session_id, 
        Message.is_archived == False
    ).order_by(Message.created_at).all()

    openai_messages = []
    if db_session.system_prompt:
        openai_messages.append({"role": "system", "content": db_session.system_prompt})
        
    openai_messages.extend([{"role": msg.role, "content": msg.content} for msg in history])

    try:
        ai_content, prompt_tokens, comp_tokens = get_chat_response(used_model, openai_messages)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API Error: {str(e)}")

    interaction_cost = calculate_cost(used_model, prompt_tokens, comp_tokens)
    total_tokens_used = prompt_tokens + comp_tokens

    ai_message = Message(
        session_id=session_id, role="assistant", content=ai_content,
        tokens_used=total_tokens_used, cost=interaction_cost
    )
    db.add(ai_message)

    db_session.total_tokens += total_tokens_used
    db_session.total_cost += interaction_cost
    db_session.active_tokens += total_tokens_used
    db_session.active_cost += interaction_cost

    db.commit()
    db.refresh(ai_message)

    return ai_message
    db.commit()
    db.refresh(ai_message)

    return ai_message
