import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from openai import AsyncOpenAI
import verifiers as vf

from bugfix_agent_env import load_environment


async def main():
    env = load_environment()

    client = AsyncOpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

    vf_client = vf.OpenAIChatCompletionsClient(client)

    results = await env.generate(
        inputs=env.get_dataset(),
        client=vf_client,
        model="openai/gpt-4o-mini",
        sampling_args={
            "temperature": 0.2,
            "max_tokens": 2000,
        },
        max_concurrent=1,
    )

    print(results)


if __name__ == "__main__":
    asyncio.run(main())