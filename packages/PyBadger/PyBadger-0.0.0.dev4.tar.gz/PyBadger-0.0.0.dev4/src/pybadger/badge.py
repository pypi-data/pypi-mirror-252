"""Abstract base class definition for all badge objects."""


# Standard libraries
import copy
from abc import ABC, abstractmethod
from typing import Literal, Optional

# Non-standard libraries
from markitup import html
from pylinks.url import URL


class ThemedBadge:

    def __init__(
        self,
        url_light: str | URL,
        url_dark: str | URL,
        link: str | URL = "",
        title: str = "",
        alt: str = "",
        width: str = "",
        height: str = "",
        align: Literal["left", "right", "center", ""] = "",
        tag_seperator: str = "",
        content_indent: str = "",
    ):
        self._url_light = url_light
        self._url_dark = url_dark
        self.link = link
        self.title = title
        self.alt = alt
        self.width = width
        self.height = height
        self.align = align
        self.tag_seperator = tag_seperator
        self.content_indent = content_indent
        return

    @property
    def html(self):
        attrs = {
            name: value for name, value in (
                ("title", self.title),
                ("alt", self.alt),
                ("width", self.width),
                ("height", self.height),
                ("align", self.align),
            ) if value
        }
        img = html.img(src=self._url_light, **attrs)
        picture = html.picture(
            img=img,
            sources=[
                html.source(srcset=self._url_light, media="(prefers-color-scheme: light)"),
                html.source(srcset=self._url_dark, media="(prefers-color-scheme: dark)"),
            ],
            tag_seperator=self.tag_seperator,
            content_indent=self.content_indent,
        )
        return picture if not self.link else html.a(
            href=self.link,
            content=[picture],
            tag_seperator=self.tag_seperator,
            content_indent=self.content_indent
        )

    def set(
        self,
        link: str | URL | None = None,
        title: str | None = None,
        alt: str | None = None,
        width: str | None = None,
        height: str | None = None,
        align: Literal["left", "right", "center", ""] | None = None,
        tag_seperator: str | None = None,
        content_indent: str | None = None,
    ):
        for arg, attr in (
            (link, "link"),
            (title, "title"),
            (alt, "alt"),
            (width, "width"),
            (height, "height"),
            (align, "align"),
            (tag_seperator, "tag_seperator"),
            (content_indent, "content_indent"),
        ):
            if arg is not None:
                setattr(self, attr, arg)
        return

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self.html)))
        return

    def __str__(self):
        return str(self.html)


class Badge:

    def __init__(
        self,
        url: str | URL,
        link: str | URL = "",
        title: str = "",
        alt: str = "",
        width: str = "",
        height: str = "",
        align: Literal["left", "right", "center", ""] = "",
        tag_seperator: str = "",
        content_indent: str = "",
    ):
        self._url = url
        self.link = link
        self.title = title
        self.alt = alt
        self.width = width
        self.height = height
        self.align = align
        self.tag_seperator = tag_seperator
        self.content_indent = content_indent
        return

    @property
    def html(self):
        attrs = {
            name: value for name, value in (
                ("title", self.title),
                ("alt", self.alt),
                ("width", self.width),
                ("height", self.height),
                ("align", self.align),
            ) if value
        }
        img = html.img(src=self._url, **attrs)
        return img if not self.link else html.a(
            href=self.link,
            content=[img],
            tag_seperator=self.tag_seperator,
            content_indent=self.content_indent
        )

    def set(
        self,
        link: str | URL | None = None,
        title: str | None = None,
        alt: str | None = None,
        width: str | None = None,
        height: str | None = None,
        align: Literal["left", "right", "center", ""] | None = None,
        tag_seperator: str | None = None,
        content_indent: str | None = None,
    ) -> None:
        for arg, attr in (
            (link, "link"),
            (title, "title"),
            (alt, "alt"),
            (width, "width"),
            (height, "height"),
            (align, "align"),
            (tag_seperator, "tag_seperator"),
            (content_indent, "content_indent"),
        ):
            if arg is not None:
                setattr(self, attr, arg)
        return

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self.html)))
        return

    def __str__(self):
        return str(self.html)

    def __add__(self, other):
        if not isinstance(other, Badge):
            raise TypeError("Only badges can be added to badges.")
        return ThemedBadge(
            url_light=self._url,
            url_dark=other._url,
            link=self.link or other.link,
            title=self.title or other.title,
            alt=self.alt or other.alt,
            width=self.width or other.width,
            height=self.height or other.height,
            align=self.align or other.align,
            tag_seperator=self.tag_seperator or other.tag_seperator,
            content_indent=self.content_indent or other.content_indent,
        )


# class Badge(ABC):
#     """Abstract base class for badges."""
#
#     @abstractmethod
#     def url(self, mode: Literal["dark", "light", "clean"] = "clean") -> str | URL:
#         """
#         URL of the badge image.
#
#         Parameters
#         ----------
#         mode : {'dark', 'light', 'clean'}
#             'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
#             respectively, while 'clean' gives the URL of the badge image without any customization.
#
#         Returns
#         -------
#         Any object whose __str__ method returns the desired URL. This could be a string, or any other object,
#         such as a `pylinks.url.URL` object.
#         """
#         ...
#
#     def __init__(
#         self,
#         alt: Optional[str],
#         title: Optional[str],
#         width: Optional[str],
#         height: Optional[str],
#         align: Optional[str],
#         link: Optional[str | URL],
#         default_theme: Literal["light", "dark"],
#         html_syntax: str | dict[Literal["tag_seperator", "content_indent"], str] = None,
#     ):
#         """
#         Parameters
#         ----------
#         alt : str
#             Alternative text to show if image doesn't load.
#             Corresponds to the 'alt' attribute of the IMG element in HTML.
#         title : str
#             Description to show on mouse hover.
#             Corresponds to the 'title' attribute of the IMG element in HTML.
#         width : str
#             Width of the image, e.g. '100px', '80%'.
#             Corresponds to the 'width' attribute of the IMG element in HTML.
#         height : str
#             Height of the image, e.g. '100px', '80%'.
#             Corresponds to the 'height' attribute of the IMG element in HTML.
#         link : pylinks.URL
#             Link URL, i.e. the URL that opens when clicking on the badge.
#             Corresponds to the 'href' attribute of the A (anchor) element in HTML.
#         default_theme : {'light', 'dark'}
#             The default theme to choose e.g. when the browser doesn't support light/dark themes.
#         """
#         self.alt = alt
#         self.title = title
#         self.width = width
#         self.height = height
#         self.align = align
#         self.link = link
#         self.default_theme = default_theme
#         self._html_syntax = {"tag_seperator": "\n", "content_indent": "\t"}
#         self.html_syntax = html_syntax
#         return
#
#     def as_html_picture(
#         self,
#         link: bool = True,
#         tag_seperator: Optional[str] = None,
#         content_indent: Optional[str] = None,
#     ) -> html.PICTURE | html.A:
#         """
#         The badge as an HTML 'picture' element, that may be wrapped by an anchor ('a') element.
#
#         Parameters
#         ----------
#         link : bool, default: True
#             Whether to wrap the picture element in an anchor element, to link to the address defined in `self.link`.
#
#         Returns
#         -------
#         html_element : pyhtmlit.element.PICTURE | pyhtmlit.element.A
#             An HTML element from the `pyhtmlit` package, which among others, has a __str__ method to
#             output the HTML syntax of the element.
#         """
#         tag_seperator = tag_seperator or self.html_syntax["tag_seperator"]
#         content_indent = content_indent or self.html_syntax["content_indent"]
#         picture = html.PICTURE(
#             img=self.as_html_img(
#                 link=False, tag_seperator=tag_seperator, content_indent=content_indent
#             ),
#             sources=[
#                 html.SOURCE(srcset=self.url("dark"), media="(prefers-color-scheme: dark)"),
#                 html.SOURCE(srcset=self.url("light"), media="(prefers-color-scheme: light)"),
#             ],
#             tag_seperator=tag_seperator,
#             content_indent=content_indent,
#         )
#         return picture if not link or self.link is None else html.A(
#             href=self.link,
#             content=[picture],
#             tag_seperator=tag_seperator,
#             content_indent=content_indent,
#         )
#
#     def as_html_img(
#         self,
#         link: bool = True,
#         tag_seperator: Optional[str] = None,
#         content_indent: Optional[str] = None,
#     ):
#         """
#         The badge as an HTML 'img' element, that may be wrapped by an anchor ('a') element.
#
#         Parameters
#         ----------
#         link : bool, default: True
#             Whether to wrap the img element in an anchor element, to link to the address defined in `self.link`.
#
#         Returns
#         -------
#         html_element : pyhtmlit.element.IMG | pyhtmlit.element.A
#             An HTML element from the `pyhtmlit` package, which among others, has a __str__ method to
#             output the HTML syntax of the element.
#         """
#         tag_seperator = tag_seperator or self.html_syntax["tag_seperator"]
#         content_indent = content_indent or self.html_syntax["content_indent"]
#         img = html.IMG(
#             src=self.url(self.default_theme),
#             alt=self.alt,
#             title=self.title,
#             width=self.width,
#             height=self.height,
#             align=self.align,
#         )
#         return img if not link or self.link is None else html.A(
#             href=self.link,
#             content=[img],
#             tag_seperator=tag_seperator,
#             content_indent=content_indent,
#         )
#
#     def __str__(self):
#         return str(self.as_html_picture())
#
#     @property
#     def link(self) -> URL | None:
#         """URL of the badge's anchor, i.e. where it links to."""
#         return self._link
#
#     @link.setter
#     def link(self, value):
#         self._link = None if not value else URL(str(value))
#         return
#
#     @property
#     def html_syntax(self):
#         return copy.deepcopy(self._html_syntax)
#
#     @html_syntax.setter
#     def html_syntax(self, value):
#         if value is None:
#             return
#         if isinstance(value, str):
#             self._html_syntax = {"tag_seperator": value, "content_indent": value}
#             return
#         if isinstance(value, dict):
#             for key, val in value.items():
#                 if key not in ("tag_seperator", "content_indent"):
#                     raise ValueError()
#                 if not isinstance(val, str):
#                     raise ValueError()
#                 self._html_syntax[key] = val
#             return
#         raise ValueError()
#
#     def display(self):
#         # Non-standard libraries
#         from IPython.display import HTML, display
#
#         display(HTML(str(self)))
#         return

