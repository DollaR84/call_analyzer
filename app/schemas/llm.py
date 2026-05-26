from pydantic import BaseModel


class CheckList(BaseModel):
    proper_greeting: int
    knows_body_type: int
    knows_year: int
    knows_mileage: int
    offered_complex_diagnostics: int
    knows_history: int
    proper_goodbye: int
    followed_top_100_rules: int


class Report(BaseModel):
    file_name: str
    requested_work: str
    manager_score: str
    comment: str
    red_flag: bool
    checklist: CheckList
