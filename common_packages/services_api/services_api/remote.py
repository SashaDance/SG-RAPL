from langserve import RemoteRunnable
from langchain_core.runnables import Runnable

from typing import (
    Any,
    AsyncIterator,
    Iterator,
    List,
    Optional,
    Sequence,
    Literal,
)
from langchain_core.runnables.utils import Input, Output
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.schema import StreamEvent
from langchain_core.tracers.log_stream import RunLogPatch


class ExtendedRemoteRunnable(Runnable[Input, Output]):
    def __init__(self, url, stop: list = []):
        self.url = url
        self.remote_runnable = RemoteRunnable(self.url)
        self.stop = stop

    def invoke(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Output:
        if self.stop:
            chunks = []
            for chunk in self.stream(input):
                chunks.append(chunk)
                if any(token in chunk for token in self.stop):
                    break
            return "".join(chunks)
        else:
            return self.remote_runnable.invoke(input, config, **kwargs)

    async def ainvoke(self, input: Input, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Output:
        return await self.remote_runnable.ainvoke(input, config, **kwargs)

    def batch(
        self,
        inputs: List[Input],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> List[Output]:
        return self.remote_runnable.batch(inputs, config, **kwargs)

    async def abatch(
        self,
        inputs: List[Input],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> List[Output]:
        return await self.remote_runnable.abatch(inputs, config, **kwargs)

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        del self.remote_runnable
        self.remote_runnable = RemoteRunnable(self.url)
        return self.remote_runnable.stream(input, config, **kwargs)

    async def astream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> AsyncIterator[Output]:
        del self.remote_runnable
        self.remote_runnable = RemoteRunnable(self.url)
        return await self.remote_runnable.astream(input, config, **kwargs)

    async def astream_log(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        *,
        include_names: Optional[Sequence[str]] = None,
        include_types: Optional[Sequence[str]] = None,
        include_tags: Optional[Sequence[str]] = None,
        exclude_names: Optional[Sequence[str]] = None,
        exclude_types: Optional[Sequence[str]] = None,
        exclude_tags: Optional[Sequence[str]] = None,
        **kwargs: Optional[Any],
    ) -> AsyncIterator[RunLogPatch]:
        del self.remote_runnable
        self.remote_runnable = RemoteRunnable(self.url)
        return await self.remote_runnable.astream_log(
            input,
            config,
            include_names=include_names,
            include_types=include_types,
            include_tags=include_tags,
            exclude_names=exclude_names,
            exclude_types=exclude_types,
            exclude_tags=exclude_tags,
            **kwargs,
        )

    async def astream_events(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        *,
        version: Literal["v1"],
        include_names: Optional[Sequence[str]] = None,
        include_types: Optional[Sequence[str]] = None,
        include_tags: Optional[Sequence[str]] = None,
        exclude_names: Optional[Sequence[str]] = None,
        exclude_types: Optional[Sequence[str]] = None,
        exclude_tags: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        del self.remote_runnable
        self.remote_runnable = RemoteRunnable(self.url)
        return await self.remote_runnable.astream_events(
            input,
            config,
            version=version,
            include_names=include_names,
            include_types=include_types,
            include_tags=include_tags,
            exclude_names=exclude_names,
            exclude_types=exclude_types,
            exclude_tags=exclude_tags,
            **kwargs,
        )


# Input, Output

# - **invoke/ainvoke**: Transforms a single input into an output.
# - **batch/abatch**: Efficiently transforms multiple inputs into outputs.
# - **stream/astream**: Streams output from a single input as it's produced.
# - **astream_log**: Streams output and selected intermediate results from an input.
