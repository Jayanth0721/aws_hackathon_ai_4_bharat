"""Access control service for role-based permissions"""
from typing import List, Optional
from src.utils.logging import logger


class AccessControlService:
    """Manages role-based access control for dashboard features"""
    
    FEATURE_PERMISSIONS = {
        'Overview': ['admin', 'creator', 'viewer'],
        'Content Intelligence': ['admin', 'creator', 'viewer'],
        'Transform': ['admin', 'creator'],
        'Monitoring': ['admin', 'creator', 'viewer'],
        'Alerts': ['admin', 'creator', 'viewer'],
        'Security': ['admin']
    }
    
    def __init__(self):
        # Lazy load auth_service to avoid circular import
        self.auth_service = None
    
    def _get_auth_service(self):
        """Lazy load auth service"""
        if self.auth_service is None:
            from src.services.auth_service import auth_service
            self.auth_service = auth_service
        return self.auth_service
    
    def can_access_feature(self, user_id: str, feature_name: str) -> bool:
        """
        Check if user can access feature based on role
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature to check access for
            
        Returns:
            True if user can access the feature, False otherwise
        """
        user_role = self.get_user_role(user_id)
        
        if not user_role:
            logger.warning(f"Unable to determine role for user {user_id}")
            return False
        
        allowed_roles = self.FEATURE_PERMISSIONS.get(feature_name, [])
        can_access = user_role in allowed_roles
        
        logger.debug(f"Access check: user={user_id}, role={user_role}, feature={feature_name}, allowed={can_access}")
        return can_access
    
    def get_user_role(self, user_id: str) -> Optional[str]:
        """
        Get user role from auth service
        
        Args:
            user_id: User identifier
            
        Returns:
            User role string (admin, creator, viewer) or None if not found
        """
        auth_service = self._get_auth_service()
        role = auth_service.get_user_role(user_id)
        
        if not role:
            logger.warning(f"No role found for user {user_id}")
            return None
        
        return role
    
    def get_accessible_features(self, user_id: str) -> List[str]:
        """
        Get list of features user can access
        
        Args:
            user_id: User identifier
            
        Returns:
            List of feature names the user can access
        """
        user_role = self.get_user_role(user_id)
        
        if not user_role:
            return []
        
        accessible = []
        for feature_name, allowed_roles in self.FEATURE_PERMISSIONS.items():
            if user_role in allowed_roles:
                accessible.append(feature_name)
        
        logger.debug(f"Accessible features for user {user_id} (role={user_role}): {accessible}")
        return accessible
    
    def is_feature_locked(self, user_id: str, feature_name: str) -> bool:
        """
        Check if feature should display lock icon for user
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature
            
        Returns:
            True if feature should show lock icon, False otherwise
        """
        return not self.can_access_feature(user_id, feature_name)


# Global instance
access_control_service = AccessControlService()
