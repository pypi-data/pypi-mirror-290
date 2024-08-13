from typing import TYPE_CHECKING, Any, Callable, cast  # noqa: I001
from .component import Component, weba_html_context
from .tag.context_manager import TagContextManager

if TYPE_CHECKING:
    from bs4 import Tag


class UIFactory:
    """
    A factory class for creating UI elements dynamically based on tag names.
    """

    def __getattr__(self, tag_name: str) -> Callable[..., TagContextManager]:
        def create_tag(*args: Any, **kwargs: Any) -> TagContextManager:
            html_context = weba_html_context.get(None)

            if html_context is None or str(html_context) == "None" or not callable(html_context.new_tag):
                html_context = Component()

            if tag_name == "text":
                tag: Tag = html_context.new_string(str(args[0]))  # type: ignore
            else:
                tag: Tag = html_context.new_tag(tag_name, **kwargs)  # type: ignore
                if args:
                    tag.string = str(args[0])

            html_context._append_to_context(tag._tag)  # type:ignore

            html_context._last_component = tag # type: ignore

            return cast(
                TagContextManager,
                tag,
            )

        return create_tag


ui = UIFactory()
