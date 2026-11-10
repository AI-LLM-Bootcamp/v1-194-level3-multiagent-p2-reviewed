import re

import tiktoken
from langchain_core.messages import AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk
from langchain_openai import ChatOpenAI

# Original version: this app used gpt-4-turbo-preview.
# OpenAI has since shut that model down. Today we use gpt-6-luna.
# Check available models at developers.openai.com/api/docs/deprecations
MODEL = "gpt-6-luna"  # small, fast and affordable current OpenAI model

# CrewAI counts the tokens of each request with the tiktoken library.
# This version of tiktoken does not know gpt-6-luna yet, so it would print
# a warning ("Could not automatically map gpt-6-luna to a tokeniser") on
# every call. We tell it to use cl100k_base, an encoding this version
# includes. It is only used to estimate tokens; nothing sent to OpenAI changes.
tiktoken.model.MODEL_TO_ENCODING[MODEL] = "cl100k_base"


class CrewChatOpenAI(ChatOpenAI):
    """ChatOpenAI adapted so this version of CrewAI works with current OpenAI models."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        # This version of CrewAI asks the model to stop writing when it reaches
        # "Observation" (the "stop" parameter), so the agent can run the tool and
        # write the real observation itself. Recent OpenAI models do not accept
        # the "stop" parameter, so we do not send it, and we cut the answer at
        # that same word here instead. The agent sees exactly what it saw before.
        result = super()._generate(messages, stop=None, run_manager=run_manager, **kwargs)
        for generation in result.generations:
            text = generation.message.content
            if stop:
                text = re.split("|".join(map(re.escape, stop)), text, maxsplit=1)[0]
            # Recent OpenAI models mark the sources they use with citation markers.
            # Each agent passes its work to the rest of the crew, so we remove
            # the markers here, before any other agent reads them.
            text = re.sub(r"cite.*?", "", text).strip()
            generation.message.content = text
            generation.text = text
        return result

    def _stream(self, messages, stop=None, run_manager=None, **kwargs):
        # If this version of CrewAI reads the model's answer as a stream, we get
        # the whole answer with _generate (to apply the two changes above)
        # and pass it on as a single piece.
        result = self._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
        text = result.generations[0].message.content
        yield ChatGenerationChunk(message=AIMessageChunk(content=text))


def create_llm():
    """Create the model that the agents of the crew share."""
    return CrewChatOpenAI(
        model=MODEL,
        # This version of langchain-openai sends temperature=0.7 by default,
        # but recent OpenAI models only accept the default value (1),
        # so we set temperature=1 explicitly.
        temperature=1,
        # The tasks of this crew turn their answer into JSON (output_json).
        # When the OpenAI address is not written explicitly, this version of
        # CrewAI does that with an OpenAI function, and recent OpenAI models
        # only accept functions here when reasoning is turned off. With the
        # address written explicitly, CrewAI asks the model for the JSON in
        # plain text instead, describing the fields it needs. Same address,
        # same model: only the way CrewAI asks for the JSON changes.
        openai_api_base="https://api.openai.com/v1",
    )
