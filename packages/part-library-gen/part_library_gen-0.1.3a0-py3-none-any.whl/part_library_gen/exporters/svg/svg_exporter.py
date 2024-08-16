import drawsvg as svg
from .pin import generate_symbol_pin
from src.part_library_gen.generators.components.rectangle import Rectangle


def export(symbol, filename):
    d = svg.Drawing(symbol.width, symbol.height, origin='center')

    for element in symbol.body:
        if isinstance(element, Rectangle):
            d.append(svg.Rectangle(element.x,
                                   element.y,
                                   element.width,
                                   element.height,
                                   stroke_width=3,
                                   fill='yellow',
                                   stroke='black'))

    for pin in symbol.pins:
        d.append(generate_symbol_pin(pin))

    d.append(svg.Text(symbol.designator.designator,
                      40,
                      symbol.designator.x,
                      symbol.designator.y))

    d.append(svg.Text(symbol.part_number.text,
                      40,
                      symbol.part_number.x,
                      symbol.part_number.y))

    d.save_svg(f"{filename}.svg")
