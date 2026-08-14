from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class CopilotState(TypedDict):
    """
    LangGraph Copilot State Container.
    Strictly governed state schema for Multi-Agent Supervisor workflow.
    """
    conversation_id: str
    execution_id: str
    organization_id: str
    user_id: str
    
    user_message: str
    # Using operator.add allows list concatenation when updates are returned
    conversation_history: Annotated[List[Dict[str, Any]], operator.add]
    
    intent: str
    intent_confidence: float
    
    entities: Dict[str, Any]
    candidate_ids: Annotated[List[str], operator.add]
    job_ids: Annotated[List[str], operator.add]
    application_ids: Annotated[List[str], operator.add]
    interview_ids: Annotated[List[str], operator.add]
    
    reasoning: str
    tool_calls: Annotated[List[Dict[str, Any]], operator.add]
    tool_results: Annotated[List[Dict[str, Any]], operator.add]
    
    recommendations: List[Dict[str, Any]]
    
    hitl_request: Optional[Dict[str, Any]]
    human_decision: Optional[str]
    
    final_response: Dict[str, Any]
    response_type: str
    
    errors: Annotated[List[str], operator.add]
    metadata: Dict[str, Any]
