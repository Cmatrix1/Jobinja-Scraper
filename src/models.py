from pydantic import BaseModel
from typing import Optional


class JobListItem(BaseModel):
    # job_id: str           
    title: str        
    company_name: str 
    location: Optional[str]
    published_at: str   
    job_type: Optional[str] 
    job_link: str


class JobDetail(BaseModel):
    job_id: str
    title: str
    company_link: Optional[str] 
    location: Optional[str]    
    job_description: str       
    requirements: str          
    benefits: Optional[str]
    experience_level: Optional[str]
    job_type: Optional[str]    
    salary: Optional[str]          
