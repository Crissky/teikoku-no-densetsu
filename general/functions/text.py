import re
from typing import Literal, Optional

from general.constants.text import (
    LEFT_SUBSECTION_GENERAL,
    SECTION_FILLCHAR,
    SECTION_LINE_LENGTH,
    SECTION_HEAD_GENERAL_END,
    SECTION_HEAD_GENERAL_START,
    SUBSECTION_FILLCHAR,
    SUBSECTION_LINE_LENGTH,
)


def escape_markdown_v2(text: str):
    for char in r"\_*[]()~`>#+-=|{}.!":
        escaped_char = f"\{char}"  # noqa
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def escape_basic_markdown_v2(text: str):
    for char in r"_[](){}>#+-=|.!":
        escaped_char = f"\{char}"  # noqa
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def escape_for_citation_markdown_v2(text: str):
    for char in r"_[](){}#+-=|.!":
        escaped_char = f"\{char}"  # noqa
        text = text.replace(escaped_char, char)
        text = text.replace(char, escaped_char)

    return text


def remove_bold(text: str):
    return text.replace("*", "")


def remove_italic(text: str):
    return re.sub(r"_\b|\b_", "", text)


def remove_code(text: str):
    return text.replace("`", "")


def create_text_in_box(
    text: str,
    section_name: str,
    section_start: str = SECTION_HEAD_GENERAL_START,
    section_end: str = SECTION_HEAD_GENERAL_END,
    fillchar: str = SECTION_FILLCHAR,
    clean_func: callable = escape_basic_markdown_v2,
) -> str:
    text = text.strip()
    section_start = format_section(
        text=section_name, section=section_start, fillchar=fillchar
    )
    section_end = format_section(
        text=section_name, section=section_end, fillchar=fillchar
    )
    result = f"{section_start}\n\n{text}\n\n{section_end}"
    if callable(clean_func):
        result = clean_func(result)

    return result


def format_section(
    text: str,
    section: Optional[str] = None,
    fillchar: str = SECTION_FILLCHAR,
    line_length: int = SECTION_LINE_LENGTH,
    text_position: Literal["left", "center", "right"] = "center",
) -> str:
    result = ""
    if isinstance(section, str) and section.count("{}") == 1:
        result = section.format(text)
    else:
        result = text

    if text_position.lower() == "left":
        result = result.ljust(line_length, fillchar)
    elif text_position.lower() == "center":
        result = result.center(line_length, fillchar)
    elif text_position.lower() == "right":
        result = result.rjust(line_length, fillchar)
    else:
        raise ValueError("text_position precisa ser left, center ou right")

    return result


def format_subsection(
    text: str,
    section: Optional[str] = LEFT_SUBSECTION_GENERAL,
    fillchar: str = SUBSECTION_FILLCHAR,
    line_length: int = SUBSECTION_LINE_LENGTH,
    text_position: Literal["left", "center", "right"] = "left",
    break_row: bool = True,
) -> str:
    br = "\n" if break_row is True else ""
    result = format_section(
        text=text,
        section=section,
        fillchar=fillchar,
        line_length=line_length,
        text_position=text_position,
    )
    result = result + br

    return result
