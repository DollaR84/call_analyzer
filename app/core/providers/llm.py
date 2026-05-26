from dishka import Provider, Scope, provide

from core import Config
from llm import BaseModel, LLMService, PromptLoader


class LLMProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_model(self, config: Config) -> BaseModel:
        return BaseModel.get(
            config.llm.name,
            base_url=config.llm.base_url,
            api_key=config.llm.api_key,
            model=config.llm.model,
        )

    @provide(scope=Scope.APP)
    async def get_prompt_loader(self, config: Config) -> PromptLoader:
        return PromptLoader(config.paths.prompt_system_file, config.paths.prompt_detail_file)

    @provide(scope=Scope.APP)
    async def get_llm_service(self, model: BaseModel, prompter: PromptLoader) -> LLMService:
        return LLMService(model, prompter)
