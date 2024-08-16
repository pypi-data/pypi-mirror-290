import sys
from enum import StrEnum
from pydantic import BaseModel
from typing import List, Literal, Any, Optional
from dialtone.config import DEFAULT_BASE_URL


class Tool(BaseModel):
    type: Literal["function"]
    function: dict[str, Any]


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class ChoiceDeltaToolCallFunction(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: ToolCallFunction


class ChoiceDeltaToolCall(BaseModel):
    index: int
    id: Optional[str] = None
    type: Optional[Literal["function"]] = None
    function: Optional[ChoiceDeltaToolCallFunction] = None


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_calls: list[ToolCall] = []
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ChoiceDelta(BaseModel):
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None


class Provider(StrEnum):
    OpenAI = "openai"
    Groq = "groq"
    DeepInfra = "deepinfra"
    Fireworks = "fireworks"
    Together = "together"
    Replicate = "replicate"
    Anthropic = "anthropic"
    Google = "google"
    Cohere = "cohere"

    def __str__(self):
        return self.value


class LLM(StrEnum):
    claude_3_5_sonnet = "claude-3-5-sonnet-20240620"
    claude_3_haiku = "claude-3-haiku-20240307"
    gpt_4o = "gpt-4o-2024-05-13"
    gpt_4o_mini = "gpt-4o-mini-2024-07-18"
    gemini_1_5_pro = "gemini-1.5-pro"
    gemini_1_5_flash = "gemini-1.5-flash"
    command_r_plus = "command-r-plus"
    command_r = "command-r"
    llama_3_70b = "llama3-70b-8192"
    llama_3_1_8b = "llama3.1-8b"
    llama_3_1_70b = "llama3.1-70b"
    llama_3_1_405b = "llama3.1-405b"

    def __str__(self):
        return self.value


class Choice(BaseModel):
    message: ChatMessage


class ChunkChoice(BaseModel):
    delta: ChoiceDelta
    finish_reason: Optional[
        Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
    ] = None


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Cost(BaseModel):
    prompt_cost: float = 0
    completion_cost: float = 0
    total_cost: float = 0


COST_PER_1M_TOKENS = {
    LLM.gpt_4o: (5, 15),
    LLM.gemini_1_5_pro: (3.50, 10.50),
    LLM.claude_3_5_sonnet: (3, 15),
    LLM.command_r_plus: (3, 15),
    LLM.llama_3_1_405b: (5, 5),
    LLM.llama_3_1_70b: (0.88, 0.88),
    LLM.llama_3_70b: (0.59, 0.79),
    LLM.command_r: (0.50, 1.50),
    LLM.gemini_1_5_flash: (0.35, 1.05),
    LLM.claude_3_haiku: (0.25, 1.25),
    LLM.gpt_4o_mini: (0.15, 0.60),
    LLM.llama_3_1_8b: (0.15, 0.15),
}


def calculate_cost(model: LLM, usage: TokenUsage) -> Cost:
    round_precision = 8

    prompt_cost_per_token, completion_cost_per_token = COST_PER_1M_TOKENS[model]

    prompt_cost = round(
        usage.prompt_tokens * prompt_cost_per_token / 1_000_000, round_precision
    )
    completion_cost = round(
        usage.completion_tokens * completion_cost_per_token / 1_000_000, round_precision
    )
    total_cost = round(prompt_cost + completion_cost, round_precision)

    return Cost(
        prompt_cost=prompt_cost, completion_cost=completion_cost, total_cost=total_cost
    )


class ChatCompletion(BaseModel):
    choices: list[Choice]
    model: LLM
    provider: Provider
    usage: TokenUsage
    cost: Cost

    def __init__(
        self, choices: list[Choice], model: LLM, provider: Provider, usage: TokenUsage
    ):
        cost = calculate_cost(model, usage)
        super().__init__(
            choices=choices, model=model, provider=provider, usage=usage, cost=cost
        )


class ChatCompletionChunk(BaseModel):
    choices: list[ChunkChoice]
    model: LLM
    provider: Provider
    usage: TokenUsage | None
    cost: Cost | None

    def __init__(
        self,
        choices: list[ChunkChoice],
        model: LLM,
        provider: Provider,
        usage: TokenUsage | None,
    ):
        if usage is not None:
            cost = calculate_cost(model, usage)
        else:
            cost = None
        super().__init__(
            choices=choices, model=model, provider=provider, usage=usage, cost=cost
        )


class OpenAIProviderConfig(BaseModel):
    api_key: str


class AnthropicProviderConfig(BaseModel):
    api_key: str


class GoogleProviderConfig(BaseModel):
    api_key: str


class CohereProviderConfig(BaseModel):
    api_key: str


class GroqProviderConfig(BaseModel):
    api_key: str


class ReplicateProviderConfig(BaseModel):
    api_key: str


class FireworksProviderConfig(BaseModel):
    api_key: str


class TogetherProviderConfig(BaseModel):
    api_key: str


class DeepInfraProviderConfig(BaseModel):
    api_key: str


CohereProviders = [Provider.Cohere]

OpenAiProviders = [Provider.OpenAI]

Llama_3_NoToolsProviders = [
    Provider.Groq,
    Provider.Fireworks,
    Provider.Together,
    Provider.DeepInfra,
    Provider.Replicate,
]

Llama_3_ToolsProviders = [Provider.Groq, Provider.DeepInfra]

Llama_3_1_NoToolsProviders = [
    Provider.Groq,
    Provider.Fireworks,
    Provider.Together,
    Provider.DeepInfra,
]

Llama_3_1_ToolsProviders = [Provider.Groq, Provider.DeepInfra]

# TODO: Add Groq here once Groq default supports 405B for all users
Llama_3_1_405B_ToolsProviders = []

# TODO: Add Groq here once Groq default supports 405B for all users
Llama_3_1_405B_NoToolsProviders = [
    Provider.Fireworks,
    Provider.Together,
    Provider.DeepInfra,
]

AnthropicProviders = [Provider.Anthropic]

GoogleProviders = [Provider.Google]


class OpenAIModelConfig(BaseModel):
    providers: list[Provider] = OpenAiProviders


class AnthropicModelConfig(BaseModel):
    providers: list[Provider] = AnthropicProviders


class GoogleModelConfig(BaseModel):
    providers: list[Provider] = GoogleProviders


class CohereModelConfig(BaseModel):
    providers: list[Provider] = CohereProviders


class Llama_3_70B_ModelConfig(BaseModel):
    tools_providers: list[Provider] = Llama_3_ToolsProviders
    no_tools_providers: list[Provider] = Llama_3_NoToolsProviders


class Llama_3_1_8B_ModelConfig(BaseModel):
    tools_providers: list[Provider] = Llama_3_1_ToolsProviders
    no_tools_providers: list[Provider] = Llama_3_1_NoToolsProviders


class Llama_3_1_70B_ModelConfig(BaseModel):
    tools_providers: list[Provider] = Llama_3_1_ToolsProviders
    no_tools_providers: list[Provider] = Llama_3_1_NoToolsProviders


class Llama_3_1_405B_ModelConfig(BaseModel):
    tools_providers: list[Provider] = Llama_3_1_405B_ToolsProviders
    no_tools_providers: list[Provider] = Llama_3_1_405B_NoToolsProviders


class ProviderConfig(BaseModel):
    openai: Optional[OpenAIProviderConfig] = None
    anthropic: Optional[AnthropicProviderConfig] = None
    google: Optional[GoogleProviderConfig] = None
    cohere: Optional[CohereProviderConfig] = None
    groq: Optional[GroqProviderConfig] = None
    replicate: Optional[ReplicateProviderConfig] = None
    fireworks: Optional[FireworksProviderConfig] = None
    together: Optional[TogetherProviderConfig] = None
    deepinfra: Optional[DeepInfraProviderConfig] = None

    @classmethod
    def OpenAI(cls, api_key: str) -> OpenAIProviderConfig:
        return OpenAIProviderConfig(api_key=api_key)

    @classmethod
    def Anthropic(cls, api_key: str) -> AnthropicProviderConfig:
        return AnthropicProviderConfig(api_key=api_key)

    @classmethod
    def Google(cls, api_key: str) -> GoogleProviderConfig:
        return GoogleProviderConfig(api_key=api_key)

    @classmethod
    def Cohere(cls, api_key: str) -> CohereProviderConfig:
        return CohereProviderConfig(api_key=api_key)

    @classmethod
    def Groq(cls, api_key: str) -> GroqProviderConfig:
        return GroqProviderConfig(api_key=api_key)

    @classmethod
    def Replicate(cls, api_key: str) -> ReplicateProviderConfig:
        return ReplicateProviderConfig(api_key=api_key)

    @classmethod
    def Fireworks(cls, api_key: str) -> FireworksProviderConfig:
        return FireworksProviderConfig(api_key=api_key)

    @classmethod
    def Together(cls, api_key: str) -> TogetherProviderConfig:
        return TogetherProviderConfig(api_key=api_key)

    @classmethod
    def DeepInfra(cls, api_key: str) -> DeepInfraProviderConfig:
        return DeepInfraProviderConfig(api_key=api_key)


class RouterModelConfig(BaseModel):
    include_models: list[LLM | str] = []
    exclude_models: list[LLM | str] = []

    gpt_4o: OpenAIModelConfig = OpenAIModelConfig(providers=OpenAiProviders)
    gpt_4o_mini: OpenAIModelConfig = OpenAIModelConfig(providers=OpenAiProviders)
    llama_3_70b: Llama_3_70B_ModelConfig = Llama_3_70B_ModelConfig(
        tools_providers=Llama_3_ToolsProviders,
        no_tools_providers=Llama_3_NoToolsProviders,
    )
    llama_3_1_8b: Llama_3_1_8B_ModelConfig = Llama_3_1_8B_ModelConfig(
        tools_providers=Llama_3_1_ToolsProviders,
        no_tools_providers=Llama_3_1_NoToolsProviders,
    )
    llama_3_1_70b: Llama_3_1_70B_ModelConfig = Llama_3_1_70B_ModelConfig(
        tools_providers=Llama_3_1_ToolsProviders,
        no_tools_providers=Llama_3_1_NoToolsProviders,
    )
    llama_3_1_405b: Llama_3_1_405B_ModelConfig = Llama_3_1_405B_ModelConfig(
        tools_providers=Llama_3_1_ToolsProviders,
        no_tools_providers=Llama_3_1_NoToolsProviders,
    )
    claude_3_5_sonnet: AnthropicModelConfig = AnthropicModelConfig(
        providers=AnthropicProviders
    )
    claude_3_haiku: AnthropicModelConfig = AnthropicModelConfig(
        providers=AnthropicProviders
    )
    gemini_1_5_pro: GoogleModelConfig = GoogleModelConfig(providers=GoogleProviders)
    gemini_1_5_flash: GoogleModelConfig = GoogleModelConfig(providers=GoogleProviders)
    command_r_plus: CohereModelConfig = CohereModelConfig(providers=CohereProviders)
    command_r: CohereModelConfig = CohereModelConfig(providers=CohereProviders)

    @classmethod
    def OpenAI(cls, providers: list[Provider] = OpenAiProviders) -> OpenAIModelConfig:
        return OpenAIModelConfig(providers=providers)

    @classmethod
    def Anthropic(
        cls, providers: list[Provider] = AnthropicProviders
    ) -> AnthropicModelConfig:
        return AnthropicModelConfig(providers=providers)

    @classmethod
    def Google(cls, providers: list[Provider] = GoogleProviders) -> GoogleModelConfig:
        return GoogleModelConfig(providers=providers)

    @classmethod
    def Cohere(cls, providers: list[Provider] = CohereProviders) -> CohereModelConfig:
        return CohereModelConfig(providers=providers)

    @classmethod
    def Llama_3_70B(
        cls,
        tools_providers: list[Provider] = Llama_3_1_ToolsProviders,
        no_tools_providers: list[Provider] = Llama_3_1_NoToolsProviders,
    ) -> Llama_3_70B_ModelConfig:
        return Llama_3_70B_ModelConfig(
            tools_providers=tools_providers, no_tools_providers=no_tools_providers
        )

    @classmethod
    def Llama_3_1_8B(
        cls,
        tools_providers: list[Provider] = Llama_3_1_ToolsProviders,
        no_tools_providers: list[Provider] = Llama_3_1_NoToolsProviders,
    ) -> Llama_3_1_8B_ModelConfig:
        return Llama_3_1_8B_ModelConfig(
            tools_providers=tools_providers, no_tools_providers=no_tools_providers
        )

    @classmethod
    def Llama_3_1_70B(
        cls,
        tools_providers: list[Provider] = Llama_3_1_ToolsProviders,
        no_tools_providers: list[Provider] = Llama_3_1_NoToolsProviders,
    ) -> Llama_3_1_70B_ModelConfig:
        return Llama_3_1_70B_ModelConfig(
            tools_providers=tools_providers, no_tools_providers=no_tools_providers
        )

    @classmethod
    def Llama_3_1_405B(
        cls,
        tools_providers: list[Provider] = Llama_3_1_405B_ToolsProviders,
        no_tools_providers: list[Provider] = Llama_3_1_405B_NoToolsProviders,
    ) -> Llama_3_1_405B_ModelConfig:
        return Llama_3_1_405B_ModelConfig(
            tools_providers=tools_providers, no_tools_providers=no_tools_providers
        )


class FallbackConfig(BaseModel):
    # By default just fall back through models recommended by the router from best to worst.
    fallback_model: Optional[LLM] = None

    # By default don't fall back at all and only try the top model recommended by the router.
    max_model_fallback_attempts: int = 0

    # By default use all available providers until a successful response is received.
    max_provider_fallback_attempts: int = sys.maxsize


class ToolsConfig(BaseModel):
    # By default assume no parallel tool use
    parallel_tool_use: bool = False


class Dials(BaseModel):
    quality: float = 1
    cost: float = 0

    def sum_to_one(self) -> bool:
        return (self.quality + self.cost) == 1


class DialtoneClient(BaseModel):
    api_key: str
    provider_config: ProviderConfig
    dials: Dials = Dials()
    router_model_config: RouterModelConfig = RouterModelConfig()
    fallback_config: FallbackConfig = FallbackConfig()
    tools_config: ToolsConfig = ToolsConfig()
    base_url: str = DEFAULT_BASE_URL


class RouteDecision(BaseModel):
    model: LLM
    providers: list[Provider]
    quality_predictions: dict[str, float]
    routing_strategy: str
