from pydantic import BaseModel, Field

class AgentState(BaseModel):
    TCR: float | None = Field(default=None, description="Task Completion Ratio")
    SPI: float | None = Field(default=None, description="Sentiment Polarity Index")
    DCR: float | None = Field(default=None, description="Disclosure Compliance Rate")
    CI: float | None = Field(default=None, description="Collaboration Index")
    OCS: float | None = Field(default=None, description="Outcome Correlation Score")