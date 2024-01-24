import typing

import mathml2omml
import latex2mathml.converter
from docx.oxml import parse_xml


def _formula(latex_string: str) -> typing.Any:
    mathml_output = latex2mathml.converter.convert(latex_string)
    omml_output = mathml2omml.convert(mathml_output)
    xml_output = (
        f'<p xmlns:m="http://schemas.openxmlformats.org/officeDocument'
        f'/2006/math">{omml_output}</p>'
    )
    return parse_xml(xml_output)[0]


def add_math(p, latex_string) -> None:
    p._p.append(_formula(latex_string))
