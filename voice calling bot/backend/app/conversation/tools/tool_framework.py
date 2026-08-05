from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import asyncio

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ToolDefinition:
    """Definition of a tool."""

    name: str
    type: str
    description: str
    parameters_schema: Dict[str, Any]
    timeout: float = 30.0
    max_retries: int = 3
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolRequest:
    """Request for tool execution."""

    tool_name: str
    parameters: Dict[str, Any]
    session_id: str
    turn_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResponse:
    """Response from tool execution."""

    success: bool
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class Tool(ABC):
    """
    Abstract base class for tools.
    
    All tools must implement this interface. The framework supports:
    - CRM tools
    - HRMS tools
    - ERP tools
    - Calendar tools
    - Email tools
    - WhatsApp tools
    - REST API tools
    - Webhook tools
    - Database tools
    - MCP tools
    - Business module tools
    """

    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResponse:
        """
        Execute the tool with given parameters.
        
        Args:
            parameters: Tool parameters
            context: Optional context information
        
        Returns:
            ToolResponse with execution result
        """
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate tool parameters.
        
        Args:
            parameters: Parameters to validate
        
        Returns:
            True if parameters are valid
        """
        pass

    @property
    @abstractmethod
    def tool_name(self) -> str:
        """Get the tool name."""
        pass

    @property
    @abstractmethod
    def tool_type(self) -> str:
        """Get the tool type."""
        pass


class ToolRegistry:
    """
    Registry for tool registration and discovery.
    
    This registry manages the registration and resolution of tools.
    It allows for dynamic tool registration and discovery.
    """

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Tool] = {}
        self._tool_definitions: Dict[str, ToolDefinition] = {}

    def register_tool(
        self,
        tool: Tool,
        definition: ToolDefinition,
    ) -> None:
        """
        Register a tool with its definition.
        
        Args:
            tool: Tool instance
            definition: Tool definition
        """
        self._tools[tool.tool_name] = tool
        self._tool_definitions[tool.tool_name] = definition
        logger.info(
            "Tool registered",
            tool_name=tool.tool_name,
            tool_type=tool.tool_type,
        )

    def unregister_tool(self, tool_name: str) -> bool:
        """
        Unregister a tool.
        
        Args:
            tool_name: Tool name
        
        Returns:
            True if tool was unregistered successfully
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            del self._tool_definitions[tool_name]
            logger.info("Tool unregistered", tool_name=tool_name)
            return True
        return False

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        Args:
            tool_name: Tool name
        
        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(tool_name)

    def get_tool_definition(self, tool_name: str) -> Optional[ToolDefinition]:
        """
        Get a tool definition by name.
        
        Args:
            tool_name: Tool name
        
        Returns:
            Tool definition or None if not found
        """
        return self._tool_definitions.get(tool_name)

    def list_tools(self) -> List[ToolDefinition]:
        """
        List all registered tools.
        
        Returns:
            List of tool definitions
        """
        return list(self._tool_definitions.values())

    def list_tools_by_type(self, tool_type: str) -> List[ToolDefinition]:
        """
        List tools by type.
        
        Args:
            tool_type: Tool type to filter by
        
        Returns:
            List of tool definitions of the specified type
        """
        return [
            defn for defn in self._tool_definitions.values()
            if defn.type == tool_type
        ]

    def is_tool_enabled(self, tool_name: str) -> bool:
        """
        Check if a tool is enabled.
        
        Args:
            tool_name: Tool name
        
        Returns:
            True if tool is enabled
        """
        definition = self._tool_definitions.get(tool_name)
        return definition.enabled if definition else False

    def enable_tool(self, tool_name: str) -> bool:
        """
        Enable a tool.
        
        Args:
            tool_name: Tool name
        
        Returns:
            True if tool was enabled successfully
        """
        definition = self._tool_definitions.get(tool_name)
        if definition:
            definition.enabled = True
            logger.info("Tool enabled", tool_name=tool_name)
            return True
        return False

    def disable_tool(self, tool_name: str) -> bool:
        """
        Disable a tool.
        
        Args:
            tool_name: Tool name
        
        Returns:
            True if tool was disabled successfully
        """
        definition = self._tool_definitions.get(tool_name)
        if definition:
            definition.enabled = False
            logger.info("Tool disabled", tool_name=tool_name)
            return True
        return False


class ToolExecutor:
    """
    Executor for tool invocations.
    
    This executor handles the execution of tools with:
    - Parameter validation
    - Timeout handling
    - Retry logic
    - Error handling
    - Response processing
    """

    def __init__(self, registry: ToolRegistry):
        """
        Initialize the tool executor.
        
        Args:
            registry: Tool registry to use
        """
        self._registry = registry

    async def execute_tool(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute a tool with the given request.
        
        Args:
            request: Tool request
        
        Returns:
            ToolResponse with execution result
        """
        start_time = datetime.utcnow()
        
        # Get tool
        tool = self._registry.get_tool(request.tool_name)
        definition = self._registry.get_tool_definition(request.tool_name)
        
        if not tool:
            return ToolResponse(
                success=False,
                result=None,
                error=f"Tool '{request.tool_name}' not found",
                execution_time=0.0,
            )
        
        if not definition or not definition.enabled:
            return ToolResponse(
                success=False,
                result=None,
                error=f"Tool '{request.tool_name}' is disabled",
                execution_time=0.0,
            )
        
        # Validate parameters
        if not tool.validate_parameters(request.parameters):
            return ToolResponse(
                success=False,
                result=None,
                error="Invalid parameters",
                execution_time=0.0,
            )
        
        # Execute with retry logic
        max_retries = definition.max_retries
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    tool.execute(request.parameters, {"session_id": request.session_id}),
                    timeout=definition.timeout,
                )
                
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                logger.info(
                    "Tool executed successfully",
                    tool_name=request.tool_name,
                    session_id=request.session_id,
                    execution_time=execution_time,
                )
                
                return ToolResponse(
                    success=result.success,
                    result=result.result,
                    error=result.error,
                    execution_time=execution_time,
                )
            
            except asyncio.TimeoutError:
                last_error = "Tool execution timeout"
                retry_count += 1
                logger.warning(
                    "Tool execution timeout",
                    tool_name=request.tool_name,
                    session_id=request.session_id,
                    retry_count=retry_count,
                )
            
            except Exception as e:
                last_error = str(e)
                retry_count += 1
                logger.error(
                    "Tool execution failed",
                    tool_name=request.tool_name,
                    session_id=request.session_id,
                    error=str(e),
                    retry_count=retry_count,
                )
            
            # Wait before retry
            if retry_count <= max_retries:
                await asyncio.sleep(1.0 * retry_count)
        
        # All retries failed
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return ToolResponse(
            success=False,
            result=None,
            error=last_error or "Tool execution failed after retries",
            execution_time=execution_time,
        )

    async def execute_tool_batch(
        self,
        requests: List[ToolRequest],
    ) -> List[ToolResponse]:
        """
        Execute multiple tools in parallel.
        
        Args:
            requests: List of tool requests
        
        Returns:
            List of tool responses
        """
        tasks = [self.execute_tool(request) for request in requests]
        return await asyncio.gather(*tasks, return_exceptions=True)


class ToolFramework:
    """
    Main framework for tool calling.
    
    This framework provides the complete tool calling infrastructure:
    - Tool registration and discovery
    - Tool execution with validation
    - Error handling and timeouts
    - Retry logic
    - Response processing
    
    The Conversation Engine invokes tools through this framework without
    knowing implementation details.
    """

    def __init__(self):
        """Initialize the tool framework."""
        self._registry = ToolRegistry()
        self._executor = ToolExecutor(self._registry)

    def register_tool(
        self,
        tool: Tool,
        definition: ToolDefinition,
    ) -> None:
        """
        Register a tool with the framework.
        
        Args:
            tool: Tool instance
            definition: Tool definition
        """
        self._registry.register_tool(tool, definition)

    def get_registry(self) -> ToolRegistry:
        """
        Get the tool registry.
        
        Returns:
            ToolRegistry instance
        """
        return self._registry

    async def execute_tool(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute a tool through the framework.
        
        Args:
            request: Tool request
        
        Returns:
            ToolResponse with execution result
        """
        return await self._executor.execute_tool(request)

    async def execute_tool_batch(
        self,
        requests: List[ToolRequest],
    ) -> List[ToolResponse]:
        """
        Execute multiple tools in parallel.
        
        Args:
            requests: List of tool requests
        
        Returns:
            List of tool responses
        """
        return await self._executor.execute_tool_batch(requests)

    def list_available_tools(self) -> List[ToolDefinition]:
        """
        List all available tools.
        
        Returns:
            List of tool definitions
        """
        return self._registry.list_tools()

    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the schema for a tool.
        
        Args:
            tool_name: Tool name
        
        Returns:
            Tool schema or None if not found
        """
        definition = self._registry.get_tool_definition(tool_name)
        if definition:
            return definition.parameters_schema
        return None


# Global tool framework instance
_tool_framework: Optional[ToolFramework] = None


def get_tool_framework() -> ToolFramework:
    """
    Get the global tool framework instance.
    
    Returns:
        ToolFramework: The global tool framework
    """
    global _tool_framework
    if _tool_framework is None:
        _tool_framework = ToolFramework()
    return _tool_framework
