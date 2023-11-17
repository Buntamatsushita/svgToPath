import streamlit as st

import streamlit as st

def parse_svg_properties(svg_text):
    svg_dict = {}
    svg_properties = svg_text[svg_text.find("<svg") + 5:svg_text.find(">")]
    svg_properties = svg_properties.replace('" ', ',').replace('"', '')
    svg_properties = dict(item.split("=") for item in svg_properties.split(","))
    return svg_properties

def extract_path(svg_text):
    in_path = False
    path = ""
    for char in svg_text[svg_text.find("<path"):]:
        if char == '"':
            in_path = not in_path
        if in_path and char != '"':
            path += char
    return path

def generate_xaml(svg_properties, path, xaml_property_mapping):
    xaml_code = '<Style x:Key="" TargetType="Path">\n'
    for prop_name, prop_value in svg_properties.items():
        if prop_name in xaml_property_mapping and prop_value != "none":
            xaml_code += f'    <Setter Property="{xaml_property_mapping[prop_name]}" Value="{prop_value}"/>\n'
    xaml_code += f'    <Setter Property="Data" Value="{path}"/>\n'
    xaml_code += '</Style>'
    return xaml_code

def main():
    st.title("SVG to XAML")
    
    input_svg = ""
    result_xaml = ''

    xaml_propaty = {"width":"Width","height":"Height","fill":"Fill","stroke":"Stroke","stroke-width":"StrokeThickness","d":"Data","stroke-linecap":"StrokeLineCap","stroke-linejoin":"StrokeLineJoin","stroke-miterlimit":"StrokeMiterLimit","stroke-dasharray":"StrokeDashArray","stroke-dashoffset":"StrokeDashOffset","stroke-opacity":"StrokeOpacity","fill-rule":"FillRule","font-family":"FontFamily","font-size":"FontSize","font-weight":"FontWeight","font-style":"FontStyle","text-anchor":"TextAlignment","text-decoration":"TextDecorations","text-rendering":"TextRenderingHint","text-transform":"TextTransform","letter-spacing":"CharacterSpacing","word-spacing":"WordSpacing","writing-mode":"TextDirection","alignment-baseline":"BaselineAlignment","baseline-shift":"BaselineOffset","dominant-baseline":"BaselineAlignment","glyph-orientation-horizontal":"GlyphOrientation","glyph-orientation-vertical":"GlyphOrientation"}

    
    choice = st.radio("Select input type", ("text", "svg file"))
    
    if choice == "text":
        input_svg = st.text_area("Enter svg", "")
    elif choice == "svg file":
        uploaded_file = st.file_uploader("Upload svg file", type=['svg'])
        if uploaded_file is not None:
            input_svg = uploaded_file.read().decode("utf-8")
            st.code(input_svg, "svg")

    if input_svg != "":
        # SVGの解析
        svg_properties = parse_svg_properties(input_svg)
        st.write(svg_properties)

        # パスの抽出
        path_data = extract_path(input_svg)

        # XAMLコードの生成
        result_xaml = generate_xaml(svg_properties, path_data, xaml_propaty)

    st.subheader("result(xaml)")
    st.code(result_xaml, "xaml")

if __name__ == "__main__":
    main()