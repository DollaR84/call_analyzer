from .base import BaseModel
from .data import GroqParamsData


class GroqModel(BaseModel):

    def __init__(self, base_url: str, api_key: str, model: str):
        super().__init__(base_url, api_key, model)

        self._params = GroqParamsData()

    def get_model_id(self) -> str:
        if not self.model:
            raise ValueError("no set Groq AI model in .env")

        return self.model
