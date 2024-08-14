from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RmsAccount(BaseModel):

    id: Optional[str] = None
    name: Optional[str] = None
    position: Optional[str] = None
    rank: Optional[str] = None
    id_number: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: Optional[datetime] = None
    modificated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created_at:
            self.created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        if self.modificated_at:
            self.modificated_at = self.modificated_at.strftime('%Y-%m-%d %H:%M:%S')

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.position:
            return False
        
        if not self.rank:
            return False
        
        if not self.id_number:
            return False
        
        if not self.email:
            return False
        
        if not self.phone_number:
            return False
        
        if not self.created_at:
            return False
        
        if not self.modificated_at:
            return False   
        
        return True

class RmsDepartment(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    manager_name: Optional[str] = None
    member: Optional[list] = None
    created_at: Optional[datetime] = None
    modificated_at: Optional[datetime] = None
    depart_tel: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created_at:
            self.created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        if self.modificated_at:
            self.modificated_at = self.modificated_at.strftime('%Y-%m-%d %H:%M:%S')

class RmsOrganizaion(BaseModel):

    id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    organTel: Optional[str] = None
    representativeName: Optional[str] = None
    department: Optional[RmsDepartment] = None
    created_at: Optional[datetime] = None
    modificated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created_at:
            self.created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        if self.modificated_at:
            self.modificated_at = self.modificated_at.strftime('%Y-%m-%d %H:%M:%S')

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.location:
            return False
        
        if not self.organTel:
            return False
        
        if not self.representativeName:
            return False
        
        if not self.department.id:
            return False
        
        if not self.department.name:
            return False
        
        if not self.department.manager_name:
            return False
        
        if not self.department.member:
            return False
        
        if not self.department.created_at:
            return False
        
        if not self.department.modificated_at:
            return False
        
        if not self.department.depart_tel:
            return False
        
        if not self.created_at:
            return False
        
        if not self.modificated_at:
            return False
        
        return True
