"""Abstract base repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from backend.models import User, Zone


class BaseRepository(ABC):
    """Abstract base class for data repositories."""
    
    @abstractmethod
    def get_user_by_cil(self, cil: str) -> Optional[User]:
        """
        Retrieve user information by CIL.
        
        Args:
            cil: Customer Identification Number
            
        Returns:
            User if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_zone_by_id(self, zone_id: int) -> Optional[Zone]:
        """
        Retrieve zone information by zone ID.
        
        Args:
            zone_id: Zone identification number
            
        Returns:
            Zone if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        """
        Retrieve all users.
        
        Returns:
            List of all users
        """
        pass
    
    @abstractmethod
    def get_all_zones(self) -> List[Zone]:
        """
        Retrieve all zones.
        
        Returns:
            List of all zones
        """
        pass


