import drawsvg as svg

pin_spacing = 50
pin_font_size = 40
pin_desc_spacing = 15

in_arrow = svg.Marker(-1.5, -0.61, 0, 0.6, scale=4, orient='auto')
in_arrow.append(svg.Lines(-1, 0.5, -1, -0.5, 0, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))

out_arrow = svg.Marker(-1.5, -0.61, 0, 0.6, scale=4, orient='auto')
out_arrow.append(svg.Lines(-1, 0, 0, -0.5, 0, 0.5, stroke_width=0.1, close=True, fill='gray', stroke='black'))

bidirectional_arrow = svg.Marker(-2.3, -0.61, 0, 0.6, scale=4, orient='auto')
bidirectional_arrow.append(svg.Lines(-1, 0.5, -1, -0.5, 0, 0, stroke_width=0.1, close=True, fill='gray', stroke='black'))
bidirectional_arrow.append(svg.Lines(-2.3, 0, -1.3, -0.5, -1.3, 0.5, stroke_width=0.1, close=True, fill='gray', stroke='black'))

marker_map = {"In": in_arrow,
              "InAnalog": in_arrow,
              "InDigital": in_arrow,
              "Out": out_arrow,
              "OutAnalog": out_arrow,
              "OutDigital": out_arrow,
              "InOut": bidirectional_arrow}


def generate_symbol_pin(pin):
    group = svg.Group()
    if pin.rotation == 0:
        pin_end = pin.x + pin.length
        group.append(svg.Line(pin.x,
                              pin.y,
                              pin_end,
                              pin.y,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end + pin_desc_spacing,
                                  pin.y + pin_font_size / 4))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin_end - 40,
                                  pin.y - 5,
                                  text_anchor='end'))
    elif pin.rotation == 180:
        pin_end = pin.x - pin.length
        group.append(svg.Line(pin.x ,
                              pin.y,
                              pin.x- pin.length,
                              pin.y,
                              stroke_width=5,
                              stroke='black',
                              marker_end=marker_map[pin.function]))
        if pin.name:
            group.append(svg.Text(pin.name,
                                  pin_font_size,
                                  pin_end - pin_desc_spacing,
                                  pin.y + pin_font_size / 4,
                                  text_anchor='end'))
        if pin.number:
            if isinstance(pin.number, list) and len(pin.number) == 1:
                pin_no_str = str(pin.number[0])
            else:
                pin_no_str = str(pin.number)
            group.append(svg.Text(pin_no_str,
                                  pin_font_size,
                                  pin_end + 40,
                                  pin.y - 5))
    return group
