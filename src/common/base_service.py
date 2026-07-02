from src.audit.service import AuditService

class BaseService:
    audit_service = AuditService()
    
    def create_audit(
        self,
        bg_tasks,
        action,
        entity_type,
        entity_id,
        user_id,
        session,
    ):
        bg_tasks.add_task(
            self.audit_service.log,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            session=session,
        )