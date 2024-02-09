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
    st.title("SVG to XAML Converter")

    uploaded_files = st.file_uploader("Upload one or more SVG files", type=['svg'], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name.split('.')[0]
            input_svg = uploaded_file.read().decode("utf-8")

            svg_properties = parse_svg_properties(input_svg)
            path_datas, fills = extract_paths(input_svg)
            svg_properties["d"] = path_datas
            svg_properties["fill"] = fills

            svg_properties_is_checked = st.multiselect("Select elements to convert to XAML", list(svg_properties.keys()), list(svg_properties.keys()))

            if st.button(f"Convert {file_name}"):
                result_xaml = generate_xaml(file_name, svg_properties, xaml_property_mapping, svg_properties_is_checked)
                st.subheader(f"Result (XAML) for {file_name}")
                st.code(result_xaml, "xml")

if __name__ == "__main__":
    main()
