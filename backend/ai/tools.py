"""LangChain tool definitions for SRM agent."""
from langchain_core.tools import tool
from backend.services import UserService, MaintenanceService
from backend.ai.prompts import TOOL_DESCRIPTIONS


def create_payment_tool(user_service: UserService):
    """
    Create payment check tool for LangChain agent.
    
    Args:
        user_service: UserService instance
        
    Returns:
        LangChain tool
    """
    @tool
    def check_payment(cil: str) -> str:
        """يستخدم للتحقق من حالة الدفع والرصيد المستحق للعميل. يتطلب رقم CIL (مثال: 1071324-101).
        
        Check payment status and outstanding balance for a customer by CIL number.
        
        Args:
            cil: Customer Identification Number (format: 1071324-101)
            
        Returns:
            str: Payment status information in Arabic
        """
        result = user_service.check_payment(cil)
        return result.message
    
    return check_payment


def create_maintenance_tool(maintenance_service: MaintenanceService):
    """
    Create maintenance check tool for LangChain agent.
    
    Args:
        maintenance_service: MaintenanceService instance
        
    Returns:
        LangChain tool
    """
    @tool
    def check_maintenance(cil: str) -> str:
        """يستخدم للتحقق من أعمال الصيانة والانقطاعات في منطقة العميل. يتطلب رقم CIL.
        
        Check for maintenance and outages in customer's zone. Requires CIL number.
        
        Args:
            cil: Customer Identification Number (format: 1071324-101)
            
        Returns:
            str: Maintenance information in Arabic
        """
        result = maintenance_service.check_maintenance(cil)
        return result.message
    
    return check_maintenance


