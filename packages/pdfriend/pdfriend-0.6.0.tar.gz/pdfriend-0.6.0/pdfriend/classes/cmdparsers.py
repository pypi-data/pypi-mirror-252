import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.info as info
import re
from typing import Self

def arg_str(arg_num: int, arg_name: str | None) -> str:
    arg_name_str = "" if arg_name is None else f" (\"{arg_name}\")"

    return f"argument {arg_num}{arg_name_str}"

class CmdParser:
    def __init__(self, cmd_info: str, args: list[str]):
        self.cmd_info = cmd_info
        self.args = args
        self.current_arg = 1

    def name(self) -> str:
        return self.cmd_info.primary_name

    def short(self) -> str:
        return self.cmd_info.short_name

    @classmethod
    def FromArgs(cls,
        program_info: info.ProgramInfo,
        args: list[str],
        no_command_message: str | None = None
    ) -> Self:
        if len(args) == 0:
            raise exceptions.ExpectedError(
                no_command_message or "no command specified"
            )

        command_name = args[0]
        command_info = program_info.get_command_info(command_name)
        if command_info is None:
            raise exceptions.ExpectedError(
                f"command \"{command_name}\" does not exist"
            )

        return CmdParser(command_info, args[1:])

    @classmethod
    def FromString(cls,
        program_info: info.ProgramInfo,
        string: str,
        no_command_message: str | None = None
    ) -> Self:
        whitespace_pattern = re.compile(r"\s+")

        return cls.FromArgs(
            program_info,
            re.split(whitespace_pattern, string),
            no_command_message = no_command_message
        )

    def next_str(self, name: str | None = None):
        if len(self.args) == 0:
            raise exceptions.ExpectedError(
                f"{arg_str(self.current_arg, name)} for command \"{self.name()}\" not provided"
            )

        head, tail = self.args[0], self.args[1:]
        self.args = tail
        self.current_arg += 1

        return head

    def next_str_or(self, default: str, name: str | None = None) -> str:
        try:
            return self.next_str(name)
        except Exception:
            return default

    def next_typed(self, type_name: str, type_converter, name: str | None = None):
        head = self.next_str(name)

        try:
            result = type_converter(head)
            return result
        except Exception:
            self.current_arg -= 1 # it gets incremented in next_str()
            raise exceptions.ExpectedError(
                f"value \"{head}\" of {arg_str(self.current_arg, name)} for command \"{self.name()}\" could not be converted to type \"{type_name}\""
            )

    def next_typed_or(self, type_name: str, type_converter, default, name: str | None = None):
        try:
            return self.next_typed(type_name, type_converter, name)
        except Exception:
            return default

    def next_int(self, name: str | None = None) -> int:
        return self.next_typed("int", int, name)

    def next_int_or(self, default: int, name: str | None = None) -> int:
        try:
            return self.next_int(name)
        except Exception:
            return default

    def next_float(self, name: str | None = None) -> float:
        return self.next_typed("float", float, name)

    def next_float_or(self, default: float, name: str | None = None) -> float:
        try:
            return self.next_float(name)
        except Exception:
            return default

    def next_pdf_slice(self, pdf: wrappers.PDFWrapper, name: str | None = None) -> list[int]:
        return self.next_typed("PDF slice", lambda s: pdf.slice(s), name = name)

    def next_pdf_slice_or(self, pdf: wrappers.PDFWrapper, default: list[int], name: str | None = None) -> list[int]:
        try:
            return self.next_pdf_slice(pdf, name = name)
        except Exception:
            return default


