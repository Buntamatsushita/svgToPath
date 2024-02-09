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


def extract_path(svg_text):
    path_datas = []
    fills = []
    
    times = svg_text.count("<path")
    
    while times > 0:
        path_data = svg_text[svg_text.find("<path") + 5:svg_text.find("/>")]
        path_data = path_data[path_data.find("d=") + 3:]
        path_data = path_data[:path_data.find('"')]
        path_datas.append(path_data)

        fill = svg_text[svg_text.find("<path") + 5:svg_text.find("/>")]
        if "fill" in fill:
            fill = fill[fill.find("fill=") + 6:]
            fill = fill[:fill.find('"')]
        else:
            fill = "none"
        fills.append(fill)

        svg_text = svg_text[svg_text.find("/>") + 2:]
        times -= 1

    return path_datas, fills

def generate_xaml(xaml_code, file_name, svg_properties, xaml_property_mapping, svg_properties_is_checked):
    xaml_code = f'<Style x:Key="{file_name}" TargetType="Path">\n'
    for prop_name, prop_value in svg_properties.items():
        if prop_name in xaml_property_mapping and prop_value != "none" and prop_name in svg_properties_is_checked:
            if prop_name == "d":
                data = ""
                for i in range(0, len(svg_properties["d"])):
                    if i == 0:
                        data += f'    <Setter Property="{"Data"}" Value="{svg_properties["data"][i]}'
                    else:
                        data += f' {svg_properties["data"][i]}'
                xaml_code += f'{data}"/>\n'
            elif prop_name == "fill":
                for i in range(0, len(svg_properties["fill"])):
                    if i == 0:
                        xaml_code += f'    <Setter Property="{"Fill"}" Value="{svg_properties["fill"][i]}"/>\n'
            else:
                xaml_code += f'    <Setter Property="{xaml_property_mapping[prop_name]}" Value="{prop_value}"/>\n'
    xaml_code += '</Style>\n'
    return xaml_code

def main():
    st.title("SVG to XAML")
    input_svg = ""
    result_xaml = ""
    files = {}

    ignore_properties = ["xmlns", "class"]

    xaml_propaty = {"width":"Width","height":"Height","fill":"Fill","stroke":"Stroke","stroke-width":"StrokeThickness","data":"Data","stroke-linecap":"StrokeLineCap","stroke-linejoin":"StrokeLineJoin","stroke-miterlimit":"StrokeMiterLimit","stroke-dasharray":"StrokeDashArray","stroke-dashoffset":"StrokeDashOffset","stroke-opacity":"StrokeOpacity","fill-rule":"FillRule","font-family":"FontFamily","font-size":"FontSize","font-weight":"FontWeight","font-style":"FontStyle","text-anchor":"TextAlignment","text-decoration":"TextDecorations","text-rendering":"TextRenderingHint","text-transform":"TextTransform","letter-spacing":"CharacterSpacing","word-spacing":"WordSpacing","writing-mode":"TextDirection","alignment-baseline":"BaselineAlignment","baseline-shift":"BaselineOffset","dominant-baseline":"BaselineAlignment","glyph-orientation-horizontal":"GlyphOrientation","glyph-orientation-vertical":"GlyphOrientation"}
    xaml_proparty_required = ["width", "height", "data"]
    choice = st.radio("Select input type", ("text", "svg file"))

    if choice == "text":
        input_svg = st.text_area("Enter svg", "")
    elif choice == "svg file":
        uploaded_file = st.file_uploader("Upload svg file", type=['svg'],accept_multiple_files=True)
        for i in uploaded_file:
            input_svg = i.read().decode("utf-8")
            files[i.name] = input_svg

    if files != "":
        svg_properties_is_checked = st.multiselect("xamlに変換する要素を選択してください。", list(xaml_propaty.keys()), list(xaml_proparty_required))
        change = False
        if change != st.button("convert"):
            # XAMLコードの生成
            change = not change
            for file in files:
                input_svg = files[file]
                file_name = file
                # SVGの解析
                svg_properties = parse_svg_properties(input_svg)

                # パスの抽出
                path_datas, fills = extract_path(input_svg)
                svg_properties["d"] = path_datas
                svg_properties["fill"] = fills

                show_xaml = st.checkbox("xamlの要素を見る", False)
                if show_xaml:
                    st.write(svg_properties)

                for i in ignore_properties:
                    if i in svg_properties:
                        del svg_properties[i]

                    result_xaml = generate_xaml(result_xaml, file_name, svg_properties, xaml_propaty, svg_properties_is_checked)

    st.subheader("result(xaml)")
    st.code(result_xaml, "xaml")

if __name__ == "__main__":
    main()