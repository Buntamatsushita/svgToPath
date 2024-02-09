import streamlit as st

def parse_svg_properties(svg_text):
    svg_dict = {}
    svg_properties_start = svg_text.find("<svg") + 5
    svg_properties_end = svg_text.find(">")
    
    if svg_properties_start != -1 and svg_properties_end != -1:
        svg_properties = svg_text[svg_properties_start:svg_properties_end]
        svg_properties = svg_properties.replace('" ', ',').replace('"', '')
        svg_dict = dict(item.split("=") for item in svg_properties.split(","))
    
    return svg_dict

def extract_paths(svg_text):
    path_datas = []
    fills = []
    paths = svg_text.split("<path")[1:]
    
    for path in paths:
        path_data_start = path.find("d=") + 3
        path_data_end = path.find('"', path_data_start)
        path_datas.append(path[path_data_start:path_data_end])
        
        fill_start = path.find("fill=") + 6
        fill_end = path.find('"', fill_start)
        fills.append(path[fill_start:fill_end])

    return path_datas, fills

def generate_xaml(file_name, svg_properties, xaml_property_mapping, svg_properties_is_checked):
    xaml_code = f'<Style x:Key="{file_name}" TargetType="Path">\n'
    
    for prop_name, prop_value in svg_properties.items():
        if prop_name in xaml_property_mapping and prop_value != "none" and prop_name in svg_properties_is_checked:
            if prop_name == "d":
                data_value = " ".join(prop_value)
                xaml_code += f'    <Setter Property="{xaml_property_mapping[prop_name]}" Value="{data_value}"/>\n'
            elif prop_name == "fill":
                for fill_value in prop_value:
                    xaml_code += f'    <Setter Property="{xaml_property_mapping[prop_name]}" Value="{fill_value}"/>\n'
            else:
                xaml_code += f'    <Setter Property="{xaml_property_mapping[prop_name]}" Value="{prop_value}"/>\n'
    
    xaml_code += '</Style>'
    return xaml_code

def main():
    st.title("SVG to XAML")

    input_svg = ""
    result_xaml = ""
    file_name = ""

    xaml_property_mapping = {
        "width": "Width", "height": "Height", "fill": "Fill", "stroke": "Stroke",
        "stroke-width": "StrokeThickness", "d": "Data", "stroke-linecap": "StrokeLineCap",
        "stroke-linejoin": "StrokeLineJoin", "stroke-miterlimit": "StrokeMiterLimit",
        "stroke-dasharray": "StrokeDashArray", "stroke-dashoffset": "StrokeDashOffset",
        "stroke-opacity": "StrokeOpacity", "fill-rule": "FillRule", "font-family": "FontFamily",
        "font-size": "FontSize", "font-weight": "FontWeight", "font-style": "FontStyle",
        "text-anchor": "TextAlignment", "text-decoration": "TextDecorations",
        "text-rendering": "TextRenderingHint", "text-transform": "TextTransform",
        "letter-spacing": "CharacterSpacing", "word-spacing": "WordSpacing",
        "writing-mode": "TextDirection", "alignment-baseline": "BaselineAlignment",
        "baseline-shift": "BaselineOffset", "dominant-baseline": "BaselineAlignment",
        "glyph-orientation-horizontal": "GlyphOrientation", "glyph-orientation-vertical": "GlyphOrientation"
    }

    choice = st.radio("Select input type", ("text", "svg file"))

    if choice == "text":
        input_svg = st.text_area("Enter svg", "")
    elif choice == "svg file":
        uploaded_file = st.file_uploader("Upload svg file", type=['svg'])
        if uploaded_file is not None:
            input_svg = uploaded_file.read().decode("utf-8")
            file_name = uploaded_file.name
            file_name = file_name[:file_name.find(".")]
            st.code(input_svg, "svg")

    if input_svg:
        svg_properties = parse_svg_properties(input_svg)
        path_datas, fills = extract_paths(input_svg)
        svg_properties["d"] = path_datas
        svg_properties["fill"] = fills

        show_xaml = st.checkbox("Show XAML elements", False)
        if show_xaml:
            st.write(svg_properties)

        svg_properties_is_checked = st.multiselect("Select elements to convert to XAML", list(svg_properties.keys()), list(svg_properties.keys()))

        if st.button("Convert"):
            result_xaml = generate_xaml(file_name, svg_properties, xaml_property_mapping, svg_properties_is_checked)

    st.subheader("Result (XAML)")
    st.code(result_xaml, "xml")

if __name__ == "__main__":
    main()
