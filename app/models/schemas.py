from pydantic import BaseModel, Field


class Classification(BaseModel):
    category: str
    urgency: str
    reason: str
    confidence: float = Field(ge=0, le=1)


class Extraction(BaseModel):
    customer_name: str
    email: str
    order_id: str
    issue: str
    confidence: float = Field(ge=0, le=1)


class Email(BaseModel):
    subject: str
    body: str
    confidence: float = Field(ge=0, le=1)