"""User service for payment and user information operations."""
from typing import Optional
from backend.models import User, PaymentStatus
from backend.repositories.base import BaseRepository


class PaymentCheckResult:
    """Result of a payment check operation."""
    
    def __init__(
        self,
        user: Optional[User],
        message: str,
        is_paid: bool
    ):
        """
        Initialize payment check result.
        
        Args:
            user: User object if found, None otherwise
            message: Formatted message in Arabic
            is_paid: Whether payment is up to date
        """
        self.user = user
        self.message = message
        self.is_paid = is_paid


class UserService:
    """Service for user-related operations."""
    
    def __init__(self, repository: BaseRepository):
        """
        Initialize user service.
        
        Args:
            repository: Repository for data access
        """
        self.repository = repository
    
    def get_user(self, cil: str) -> Optional[User]:
        """
        Get user by CIL.
        
        Args:
            cil: Customer Identification Number
            
        Returns:
            User if found, None otherwise
        """
        return self.repository.get_user_by_cil(cil)
    
    def check_payment(self, cil: str) -> PaymentCheckResult:
        """
        Check payment status for a customer.
        
        Args:
            cil: Customer Identification Number
            
        Returns:
            PaymentCheckResult with payment information
        """
        user = self.get_user(cil)
        
        if not user:
            return PaymentCheckResult(
                user=None,
                message=f"لم يتم العثور على عميل برقم CIL: {cil}. الرجاء التحقق من الرقم.",
                is_paid=False
            )
        
        name = user.name
        payment_status = user.payment_status
        outstanding_balance = user.outstanding_balance
        last_payment = user.last_payment_date.strftime('%Y-%m-%d')
        service_status = user.service_status.value
        service_type = user.service_type.value
        
        if payment_status == PaymentStatus.PAID:
            message = f"""
معلومات العميل {name}:
- نوع الخدمة: {service_type}
- حالة الدفع: ✅ {payment_status.value}
- آخر دفعة: {last_payment}
- الرصيد المستحق: {outstanding_balance} درهم
- حالة الخدمة: {service_status}

الدفعات محدثة. إذا كانت الخدمة مقطوعة، قد يكون السبب صيانة في المنطقة.
"""
            return PaymentCheckResult(
                user=user,
                message=message.strip(),
                is_paid=True
            )
        else:
            message = f"""
معلومات العميل {name}:
- نوع الخدمة: {service_type}
- حالة الدفع: ⚠️ {payment_status.value}
- آخر دفعة: {last_payment}
- الرصيد المستحق: {outstanding_balance} درهم
- حالة الخدمة: {service_status}

يوجد رصيد مستحق بقيمة {outstanding_balance} درهم. الرجاء سداد المبلغ لاستعادة الخدمة.
يمكنك الدفع عبر:
1. التطبيق المحمول لـ SRM
2. وكالات الأداء (وفا كاش، كاش بلس)
3. البنك
"""
            return PaymentCheckResult(
                user=user,
                message=message.strip(),
                is_paid=False
            )


