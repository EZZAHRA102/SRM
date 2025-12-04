"""Mock repository implementation using Pandas DataFrames."""
import logging
import pandas as pd
from typing import Optional, List
from datetime import datetime

from backend.models import User, Zone, PaymentStatus, ServiceStatus, ServiceType, MaintenanceStatus
from backend.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class MockRepository(BaseRepository):
    """Mock repository using Pandas DataFrames (simulates Azure SQL)."""
    
    def __init__(self):
        """Initialize mock data."""
        self._users_table = pd.DataFrame({
            'cil': ['1071324-101', '1300994-101', '3095678-303', '4017890-404', '5029012-505'],
            'name': ['Abdenbi EL MARZOUKI', 'Ahmed Sabil', 'محمد الإدريسي', 'خديجة العلوي', 'يوسف السباعي'],
            'address': [
                '967, Lot. Sala Al Jadida Zone (1), Sala Al Jadida',
                '2 Rue BATTIT I Ghizlaine Imm 2 apt 03',
                'شارع محمد الخامس، فاس',
                'حي النخيل، مراكش',
                'شارع الزرقطوني، طنجة'
            ],
            'phone': ['0612345678', '0698765432', '0611223344', '0655667788', '0699887766'],
            'service_type': ['ماء وكهرباء', 'ماء', 'ماء', 'كهرباء', 'ماء وكهرباء'],
            'zone_id': [1, 2, 1, 3, 2],
            'payment_status': ['مدفوع', 'مدفوع', 'مدفوع', 'مدفوع', 'غير مدفوع'],
            'last_payment_date': ['2024-11-15', '2024-11-08', '2024-11-28', '2024-11-10', '2024-08-15'],
            'outstanding_balance': [0.0, 0.0, 0.0, 0.0, 890.0],
            'service_status': ['نشط', 'نشط', 'نشط', 'نشط', 'مقطوع']
        })
        
        self._zones_table = pd.DataFrame({
            'zone_id': [1, 2, 3, 4],
            'zone_name': [
                'الدار البيضاء - وسط المدينة',
                'الرباط - حي المحمدي',
                'مراكش - القليعة',
                'طنجة - المدينة القديمة'
            ],
            'maintenance_status': ['جاري الصيانة', 'لا توجد صيانة', 'لا توجد صيانة', 'جاري الصيانة'],
            'outage_reason': [
                'إصلاح أنابيب المياه الرئيسية',
                None,
                None,
                'صيانة محولات الكهرباء'
            ],
            'estimated_restoration': ['2024-12-04 18:00', None, None, '2024-12-05 14:00'],
            'affected_services': ['ماء', None, None, 'كهرباء'],
            'status_updated': ['2024-12-03 08:00', '2024-12-01 10:00', '2024-12-01 10:00', '2024-12-03 06:00']
        })
    
    def get_user_by_cil(self, cil: str) -> Optional[User]:
        """
        Retrieve user information by CIL.
        
        Args:
            cil: Customer Identification Number
            
        Returns:
            User if found, None otherwise
        """
        logger.info(f"Database query: get_user_by_cil(CIL='{cil}')")
        logger.debug(f"Searching in {len(self._users_table)} users")
        
        user_row = self._users_table[self._users_table['cil'] == cil]
        
        if user_row.empty:
            logger.warning(f"Database query: User NOT FOUND for CIL='{cil}'")
            logger.debug(f"Available CILs in database: {list(self._users_table['cil'].values)}")
            return None
        
        row = user_row.iloc[0]
        logger.info(f"Database query: User FOUND for CIL='{cil}'")
        logger.debug(f"User data retrieved: name='{row['name']}', zone_id={row['zone_id']}, "
                    f"payment_status='{row['payment_status']}', outstanding_balance={row['outstanding_balance']}")
        
        # Map payment status string to enum
        payment_status = PaymentStatus.PAID if row['payment_status'] == 'مدفوع' else PaymentStatus.UNPAID
        
        # Map service status string to enum
        service_status = ServiceStatus.ACTIVE if row['service_status'] == 'نشط' else ServiceStatus.DISCONNECTED
        
        # Map service type string to enum
        service_type_map = {
            'ماء': ServiceType.WATER,
            'كهرباء': ServiceType.ELECTRICITY,
            'ماء وكهرباء': ServiceType.BOTH
        }
        service_type = service_type_map.get(row['service_type'], ServiceType.WATER)
        
        # Parse date
        last_payment_date = datetime.strptime(row['last_payment_date'], '%Y-%m-%d').date()
        
        return User(
            cil=row['cil'],
            name=row['name'],
            address=row['address'],
            phone=row['phone'],
            service_type=service_type,
            zone_id=int(row['zone_id']),
            payment_status=payment_status,
            last_payment_date=last_payment_date,
            outstanding_balance=float(row['outstanding_balance']),
            service_status=service_status
        )
    
    def get_zone_by_id(self, zone_id: int) -> Optional[Zone]:
        """
        Retrieve zone information by zone ID.
        
        Args:
            zone_id: Zone identification number
            
        Returns:
            Zone if found, None otherwise
        """
        logger.info(f"Database query: get_zone_by_id(zone_id={zone_id})")
        
        zone_row = self._zones_table[self._zones_table['zone_id'] == zone_id]
        
        if zone_row.empty:
            logger.warning(f"Database query: Zone NOT FOUND for zone_id={zone_id}")
            return None
        
        row = zone_row.iloc[0]
        logger.info(f"Database query: Zone FOUND for zone_id={zone_id}")
        logger.debug(f"Zone data retrieved: name='{row['zone_name']}', "
                    f"maintenance_status='{row['maintenance_status']}'")
        
        # Map maintenance status string to enum
        maintenance_status = (
            MaintenanceStatus.IN_PROGRESS 
            if row['maintenance_status'] == 'جاري الصيانة' 
            else MaintenanceStatus.NONE
        )
        
        return Zone(
            zone_id=int(row['zone_id']),
            zone_name=row['zone_name'],
            maintenance_status=maintenance_status,
            outage_reason=row['outage_reason'] if pd.notna(row['outage_reason']) else None,
            estimated_restoration=row['estimated_restoration'] if pd.notna(row['estimated_restoration']) else None,
            affected_services=row['affected_services'] if pd.notna(row['affected_services']) else None,
            status_updated=row['status_updated']
        )
    
    def get_all_users(self) -> List[User]:
        """
        Retrieve all users.
        
        Returns:
            List of all users
        """
        users = []
        for _, row in self._users_table.iterrows():
            user = self.get_user_by_cil(row['cil'])
            if user:
                users.append(user)
        return users
    
    def get_all_zones(self) -> List[Zone]:
        """
        Retrieve all zones.
        
        Returns:
            List of all zones
        """
        zones = []
        for _, row in self._zones_table.iterrows():
            zone = self.get_zone_by_id(int(row['zone_id']))
            if zone:
                zones.append(zone)
        return zones


