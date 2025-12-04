"""SRM AI Agent using LangChain and Azure OpenAI."""
import logging
from typing import Optional, List
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from backend.models import ChatMessage, ChatResponse
from backend.config import Settings
from backend.services import UserService, MaintenanceService
from backend.ai.prompts import SYSTEM_PROMPT_AR, SYSTEM_PROMPT_FR
from backend.ai.tools import create_payment_tool, create_maintenance_tool

logger = logging.getLogger(__name__)


class SRMAgent:
    """
    SRM AI Agent for customer service.
    
    Handles chat interactions with tool execution.
    """
    
    def __init__(
        self,
        settings: Settings,
        user_service: UserService,
        maintenance_service: MaintenanceService
    ):
        """
        Initialize SRM agent.
        
        Args:
            settings: Application settings
            user_service: User service for payment checks
            maintenance_service: Maintenance service for outage checks
        """
        self.settings = settings
        self.user_service = user_service
        self.maintenance_service = maintenance_service
        self._llm = None
        self._tools = None
    
    def initialize(self) -> bool:
        """
        Initialize the LLM and bind tools.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Initialize Azure OpenAI
            self._llm = AzureChatOpenAI(
                azure_endpoint=self.settings.azure_openai_endpoint,
                api_key=self.settings.azure_openai_api_key,
                api_version=self.settings.azure_openai_api_version,
                deployment_name=self.settings.azure_openai_deployment_name,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Create tools
            payment_tool = create_payment_tool(self.user_service)
            maintenance_tool = create_maintenance_tool(self.maintenance_service)
            self._tools = [payment_tool, maintenance_tool]
            
            # Bind tools to LLM
            self._llm = self._llm.bind_tools(self._tools)
            
            logger.info("SRM Agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            return False
    
    def chat(self, message: str, history: List[ChatMessage], language: str = "ar") -> ChatResponse:
        """
        Process a chat message and return response.
        
        Args:
            message: User message
            history: Previous chat messages
            language: Language code ('ar' or 'fr')
            
        Returns:
            ChatResponse with agent response
        """
        logger.info("=" * 60)
        logger.info("AI Chat Request")
        logger.info("=" * 60)
        logger.info(f"Incoming user message: {message}")
        logger.debug(f"Chat history length: {len(history)} messages")
        
        if not self._llm:
            logger.error("LLM not initialized")
            error_message = "Désolé, l'assistant intelligent n'a pas été initialisé. Veuillez vérifier les paramètres." if language == "fr" else "عذراً، لم يتم تهيئة المساعد الذكي. الرجاء التحقق من الإعدادات."
            return ChatResponse(
                response=error_message,
                tool_calls=None
            )
        
        try:
            # Build messages list
            messages = self._build_messages(message, history, language)
            logger.debug(f"Built {len(messages)} messages for LLM (including system prompt)")
            
            # Get response from agent
            logger.debug("Invoking LLM...")
            response = self._llm.invoke(messages)
            logger.debug(f"LLM response received: {response.content[:200]}...")
            
            # Check if agent wants to use tools
            tool_calls = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                logger.info(f"AI requested {len(response.tool_calls)} tool call(s)")
                for idx, tool_call in enumerate(response.tool_calls):
                    tool_name = tool_call.get('name', 'unknown')
                    tool_args = tool_call.get('args', {})
                    logger.info(f"Tool call {idx+1}: {tool_name}")
                    logger.debug(f"Tool {tool_name} arguments: {tool_args}")
                
                # Add the AI response with tool calls to messages
                messages.append(response)
                
                # Execute tools and create tool messages
                logger.info("Executing tool calls...")
                tool_messages = self._execute_tools(response.tool_calls, language)
                logger.info(f"Tool execution completed, {len(tool_messages)} tool message(s) generated")
                messages.extend(tool_messages)
                
                # Store tool call info for response
                tool_calls = response.tool_calls
                
                # Get final response after tool execution
                logger.debug("Invoking LLM for final response after tool execution...")
                final_response = self._llm.invoke(messages)
                logger.info(f"Final AI response: {final_response.content[:200]}...")
                logger.info("=" * 60)
                
                return ChatResponse(
                    response=final_response.content,
                    tool_calls=tool_calls
                )
            
            logger.info(f"AI response (no tools): {response.content[:200]}...")
            logger.info("=" * 60)
            
            return ChatResponse(
                response=response.content,
                tool_calls=None
            )
            
        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            error_message = f"Désolé, une erreur s'est produite: {str(e)}" if language == "fr" else f"عذراً، حدث خطأ: {str(e)}"
            return ChatResponse(
                response=error_message,
                tool_calls=None
            )
    
    def _build_messages(self, message: str, history: List[ChatMessage], language: str = "ar") -> List:
        """
        Build messages list for LLM.
        
        Args:
            message: Current user message
            history: Previous chat messages
            language: Language code ('ar' or 'fr')
            
        Returns:
            List of LangChain messages
        """
        # Select system prompt based on language
        system_prompt = SYSTEM_PROMPT_FR if language == "fr" else SYSTEM_PROMPT_AR
        messages = [SystemMessage(content=system_prompt)]
        
        # Add chat history
        for msg in history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
        
        # Add current user input
        messages.append(HumanMessage(content=message))
        
        return messages
    
    def _execute_tools(self, tool_calls: List[dict], language: str = "ar") -> List[ToolMessage]:
        """
        Execute tool calls and return tool messages.
        
        Args:
            tool_calls: List of tool call dictionaries
            language: Language code ('ar' or 'fr')
            
        Returns:
            List of ToolMessage objects
        """
        tool_messages = []
        
        for idx, tool_call in enumerate(tool_calls):
            tool_name = tool_call.get('name')
            tool_args = tool_call.get('args', {})
            tool_call_id = tool_call.get('id')
            
            logger.info(f"Executing tool {idx+1}/{len(tool_calls)}: {tool_name}")
            logger.debug(f"Tool {tool_name} call ID: {tool_call_id}")
            logger.debug(f"Tool {tool_name} arguments: {tool_args}")
            
            # Find and execute the tool
            tool_result = None
            for tool in self._tools:
                if tool.name == tool_name:
                    try:
                        logger.debug(f"Invoking tool {tool_name}...")
                        tool_result = tool.invoke(tool_args)
                        logger.info(f"Tool {tool_name} execution SUCCESS")
                        # Log result preview (first 300 chars)
                        result_preview = str(tool_result)[:300] + "..." if len(str(tool_result)) > 300 else str(tool_result)
                        logger.debug(f"Tool {tool_name} result (preview): {result_preview}")
                    except Exception as e:
                        logger.error(f"Tool {tool_name} execution failed: {e}", exc_info=True)
                        error_msg = f"Désolé, une erreur s'est produite lors de l'exécution de l'outil: {str(e)}" if language == "fr" else f"عذراً، حدث خطأ في تنفيذ الأداة: {str(e)}"
                        tool_result = error_msg
                    break
            
            if tool_result:
                tool_messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                ))
            else:
                logger.warning(f"Tool {tool_name} returned no result")
        
        return tool_messages


