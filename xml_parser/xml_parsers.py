from cgitb import text
from dataclasses import asdict
from distutils import text_file
import xml.etree.ElementTree as xml


def generateXMLSample(fileName, text_info):
    """
    function that creates a xml file for the "sample" import
    One dictionary for each sub level of tags
    """
    root = xml.Element('import')
    root.set("type", "sample")
    root.set("ssdm_version", "0.9.0")
    root.set("xmlns", "http://sshade.eu/schema/import")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://sshade.eu/schema/import http://sshade.eu/schema/import-0.9.xsd")
    
    # create elements to add
    sample = xml.Element("sample")
    root.append(sample)

    # array of all "sample" direct children
    sample_sub_one = ["import_mode", "uid", "owner_databases", "experimentalists",
                   "name", "date", "provider", "is_generic", "body", "geolocation",
                   "surface_roughness", "size_unit", "comments", "substrate_material",
                   "substrate_comments", "parameters_environment", "layers"]

    # dictionary of arrays of all the sub-sub elements
    sample_sub_two = {
        "owner_databases": ["database_uid"],
        "experimentalists": ["experimentalist_uid"],
        "body": ["uid", "terrain_type", "coordinate_system"],
        "geolocation": ["place", "region", "country_code", "type", "coordinates"],
        "parameters_environment": ["time_unit", "temperature", "fluid"],
        "layers": ["layer"],
    }

    # dictionary of arrays of all the sub x 2 elements
    sample_sub_three = {
        "coordinates": ["coordinate"],
        "temperature": ["unit", "value", "error", "time", "time_error", "max", "max_error",
                        "max_time", "comments"],
        "fluid": ["type", "temperature", "temperature_error", "pressure_unit", "pressure", "pressure_error",
                  "ph", "ph_error", "time", "time_error", "comments"],
        "layer": ["import_mode", "name", "order", "type", "thickness", "thickness_error",
                  "mass", "mass_error", "texture", "porosity_type", "compacity", "compacity_error",
                  "density", "density_error", "comments", "formation_mode", "formation_rate",
                  "formation_temperature", "formation_temperature_error", "formation_pressure",
                  "formation_pressure_error", "formation_fluid_pressure",
                  "formation_fluid_pressure_error", "formation_comments", "materials_mixing",
                  "materials"],
    }

    # dictionary of arrays of all the sub x 3 elements
    sample_sub_four = {
        "coordinate": ["latitude", "longitude", "altitude"],
        "materials": ["material"],
    }

    # dictionary of arrays of all the sub x 4 elements
    sample_sub_five = {
        "material": ["import_mode", "uid", "relevance", "arrangement", "mass", "mass_error", "mass_fraction", "mass_fraction_error",
                     "abundance_comments", "name", "family", "local_reference_code", "origin", "comments", "constituents_mixing",
                     "basic_constituents"]
    }

    # dictionary of arrays of all the sub x 5 elements
    sample_sub_six = {
        "basic_constituents": ["basic_constituent"]
    }

    # dictionary of arrays of all the sub x 5 elements
    sample_sub_seven = {
        "basic_constituent": ["import_mode", "uid", "relevance", "arrangement", "mass", "mass_error", "mass_fraction", "mass_fraction_error",
                              "mole", "mole_error", "mole_fraction", "mole_fraction_error", "abundance_comments", "name", "fundamental_phase_uid",
                              "texture", "comments"]
    }

    first_sub_level = []

    for sub_el in sample_sub_one:
        elm = xml.SubElement(sample, sub_el)
        first_sub_level.append(elm)

    elements_array = []
    elements_array_two = []
    elements_array_three = []
    elements_array_four = []
    elements_array_five = []

    # adding sub elements to the children of sample
    # saving element reference in array for next 
    for key in sample_sub_two:
        for child in sample:
            if child.tag == key:
                for val in sample_sub_two[key]:
                    xml.SubElement(child, val)
                    # add element to array
                    if val in sample_sub_three.keys():
                        elements_array.append(child.find(val))

    def generate_sub_elements(array, dict, dict_next, array_add, section):
        for i in array:
            for key in dict.keys():
                if i.tag == key+section:

                    if len(section) > 0:
                        tag = i.tag[0:-4]
                    else:
                        tag = i.tag

                    for val in dict[tag]:
                        xml.SubElement(i, val+section)
                        # add element to array two
                        if dict_next:
                            if val in dict_next.keys():
                                array_add.append(i.find(val+section))
    
    generate_sub_elements(elements_array, sample_sub_three, sample_sub_four,
                          elements_array_two, "")
    generate_sub_elements(elements_array_two, sample_sub_four, sample_sub_five,
                          elements_array_three, "")
    generate_sub_elements(elements_array_three, sample_sub_five, sample_sub_six,
                          elements_array_four, "")                   
    generate_sub_elements(elements_array_four, sample_sub_six, sample_sub_seven,
                          elements_array_five, "")
    generate_sub_elements(elements_array_five, sample_sub_seven, None, None, "")

    # if there are major added sections we add them
    # reuses flow from above, but starting from sub_three list, as they are all placed there 
    def add_section(section_parent, section_child, number_of_sections):
        # set section
        if number_of_sections >= 0:

            for number in range(0, number_of_sections+1):

                for child in sample:
                    if child.tag == section_parent:
                        section = xml.SubElement(child, f'{section_child}_{number}')

                for tag in sample_sub_three[section_child]:
                    tag_element = xml.SubElement(section, f'{tag}_{number}')

                    if tag in sample_sub_four.keys():
                        for i in sample_sub_four[tag]:
                            j = xml.SubElement(tag_element, f'{i}_{number}')

                            if i in sample_sub_five.keys():
                                for k in sample_sub_five[i]:
                                    l = xml.SubElement(j, f'{k}_{number}')

                                    if k in sample_sub_six.keys():
                                        for m in sample_sub_six[k]:
                                            n = xml.SubElement(l, f'{m}_{number}')

                                            if m in sample_sub_seven.keys():
                                                for o in sample_sub_seven[m]:
                                                    xml.SubElement(n, f'{o}_{number}')

    # there are three major sections possible to add
    # we count how many should be
    # layer_x_import_mode_zer_0
    large_sections = ["_zer", "_one", "_two", "_thre", "_fou"]
    layer_count = -1
    for key in text_info.keys():
        tag_name = text_info[key][1]
        wrong_sample = False
        for section in large_sections:
            if section in tag_name:
                wrong_sample = True
        if not wrong_sample:
            if tag_name[-1].isdigit() and tag_name[-2] == "_" and not "_added" in tag_name and not "_inner" in tag_name:
                if text_info[key][0] == "layer":
                    if int(tag_name[-1]) > layer_count:
                        layer_count = int(tag_name[-1])
    
    # call the function above with the parent tag, section tag, and the count
    add_section("layers", "layer", layer_count)

    # explain changes in function
    def add_inner_section(specified_sample, placement, added_section):

        for child in root.iter(specified_sample):
            correct_sample = child

        for place in placement:
            if not added_section:
                if place[0] == "_" and place[1].isdigit():
                    for child in correct_sample.iter(f'layer{place[0:2]}'):
                        correct_layer = child
                        number = place[0:2]
                else:
                    for child in correct_sample.iter('layer'):
                        correct_layer = child
                        number = ""
            else:
                if place[5].isdigit():
                    add_section_specifier = place[0:6]
                    number = place[0:6]
                else:
                    add_section_specifier = place[0:4]
                    number = place[0:4]

                for child in correct_sample.iter(f'layer{add_section_specifier}'):
                    correct_layer = child

            for child in correct_layer.iter(f'materials{number}'):
                correct_materials = child

                material_inner = xml.SubElement(correct_materials, f'material{place}')
                xml.SubElement(material_inner, f'import_mode{place}')
                xml.SubElement(material_inner, f'uid{place}')
                xml.SubElement(material_inner, f'relevance{place}')
                xml.SubElement(material_inner, f'arrangement{place}')
                xml.SubElement(material_inner, f'mass{place}')
                xml.SubElement(material_inner, f'mass_error{place}')
                xml.SubElement(material_inner, f'mass_fraction{place}')
                xml.SubElement(material_inner, f'mass_fraction_error{place}')
                xml.SubElement(material_inner, f'abundance_comments{place}')
                xml.SubElement(material_inner, f'name{place}')
                xml.SubElement(material_inner, f'family{place}')
                xml.SubElement(material_inner, f'local_reference_code{place}')
                xml.SubElement(material_inner, f'origin{place}')
                xml.SubElement(material_inner, f'comments{place}')
                xml.SubElement(material_inner, f'constituents_mixing{place}')
                basic_constituents = xml.SubElement(material_inner, f'basic_constituents{place}')
                basic_constituent = xml.SubElement(basic_constituents, f'basic_constituent{place}')
                xml.SubElement(basic_constituent, f'import_mode{place}')
                xml.SubElement(basic_constituent, f'uid{place}')
                xml.SubElement(basic_constituent, f'relevance{place}')
                xml.SubElement(basic_constituent, f'arrangement{place}')
                xml.SubElement(basic_constituent, f'mass{place}')
                xml.SubElement(basic_constituent, f'mass_error{place}')
                xml.SubElement(basic_constituent, f'mass_fraction{place}')
                xml.SubElement(basic_constituent, f'mass_fraction_error{place}')
                xml.SubElement(basic_constituent, f'mole{place}')
                xml.SubElement(basic_constituent, f'mole_error{place}')
                xml.SubElement(basic_constituent, f'mole_fraction{place}')
                xml.SubElement(basic_constituent, f'mole_fraction_error{place}')
                xml.SubElement(basic_constituent, f'abundance_comments{place}')
                xml.SubElement(basic_constituent, f'name{place}')
                xml.SubElement(basic_constituent, f'fundamental_phase_uid{place}')
                xml.SubElement(basic_constituent, f'texture{place}')
                xml.SubElement(basic_constituent, f'comments{place}')

    material_inner_to_add = []
    
    for key in text_info.keys():
        tag_name = text_info[key][1]

        is_added_sample = False
        for section in large_sections:
            if section in tag_name:
                is_added_sample = True

        if not is_added_sample:
            if tag_name[-1].isdigit() and tag_name[-2] == "_" and not "_added" in tag_name and "_inner" in tag_name:

                for i in range(0, len(tag_name)):

                    if tag_name[i] == "_" and tag_name[i+1].isdigit() and i < len(tag_name)-1:

                        if text_info[key][0] == "material" and not tag_name[i:] in material_inner_to_add:
                            material_inner_to_add.append(tag_name[i:])
                        
                    elif tag_name[i:i+6] == "_inner":
                        
                        if text_info[key][0] == "material" and not tag_name[i:] in material_inner_to_add:
                            material_inner_to_add.append(tag_name[i:])
                        break
    
    if len(material_inner_to_add) > 0:
        add_inner_section("sample", material_inner_to_add, False)

    # loop to add "_added" fields
    for key in text_info.keys():
        tag_name = text_info[key][1]
        is_added_sample = False

        for section in large_sections:
            if section in tag_name:
                is_added_sample = True
        

        # look for the "_added" mark
        if "_added" in tag_name and not is_added_sample:
            parent = text_info[key][0]
            # original_parent = parent

            section_specifier = ""
            rest_to_add = ""
            
            # # import_mode_inner_0_added_0
            for i in range(0, len(tag_name)):
                # see if it's a section with inner
                if tag_name[i] == "_" and tag_name[i+1].isdigit() and tag_name[i+2:i+8] == "_inner":
                    section_specifier = tag_name[i:i+10]
                    rest_to_add = tag_name[i:]
                    break
                elif tag_name[i:i+6] == "_inner" and not tag_name[i-1].isdigit():
                    section_specifier = tag_name[i:i+8]
                    rest_to_add = tag_name[i:]
                    break
                elif tag_name[i] == "_" and tag_name[i+1].isdigit() and not tag_name[i+2:i+8] == "_inner":
                    section_specifier = tag_name[i:i+2]
                    rest_to_add = tag_name[i:]
                    break
                # if it's not in an added section
                elif tag_name[i:i+6] == "_added" and not tag_name[i-1].isdigit():
                    rest_to_add = tag_name[i:]
                    break
                elif tag_name[i:i+6] == "_added" and tag_name[i-1].isdigit():
                    section_specifier = tag_name[i-2:i]
                    rest_to_add = tag_name[i-2:]
                    break

            iteration_name = parent+"s"+section_specifier
            single_field = False

            if "owner_databases" in parent or "experimentalists" in parent:
                iteration_name = parent+section_specifier
                single_field = True

            for el in sample.iter(iteration_name):
                # Check if the basic constituents (parent) tag is already created, if not create it
                if not single_field:
                    if len(el.findall(parent+"s"+rest_to_add)) == 0:
                        added_fields_section = xml.SubElement(el, parent+"s"+rest_to_add)
                        xml.SubElement(added_fields_section, tag_name)
                    else:
                        for element in sample.iter(parent+"s"+rest_to_add):
                            xml.SubElement(element, tag_name)
                else:
                    for element in sample.iter(parent+section_specifier):
                        xml.SubElement(element, tag_name)

    
    # add additional samples, reusing method from above
    large_sections_to_add = []
    for key in text_info.keys():
        char_count = text_info[key][1]
        if char_count[-4:] in large_sections and not char_count[-4:] in large_sections_to_add:
            large_sections_to_add.append(char_count[-4:])
    
    if len(large_sections_to_add) > 0:
        for section in large_sections_to_add:
            elements_array = []
            elements_array_two = []
            elements_array_three = []
            elements_array_four = []
            elements_array_five = []
            
            new_section = xml.Element(f'sample{section}')
            root.append(new_section)
            for sub_el in sample_sub_one:
                xml.SubElement(new_section, sub_el+section)

            for key in sample_sub_two:
                for child in new_section:
                    if child.tag == key+section:
                        for val in sample_sub_two[key]:
                            xml.SubElement(child, val+section)
                            # add element to array
                            if val in sample_sub_three.keys():
                                elements_array.append(child.find(val+section))


            generate_sub_elements(elements_array, sample_sub_three, sample_sub_four,
                            elements_array_two, section)
            generate_sub_elements(elements_array_two, sample_sub_four, sample_sub_five,
                                elements_array_three, section)
            generate_sub_elements(elements_array_three, sample_sub_five, sample_sub_six,
                                elements_array_four, section)               
            generate_sub_elements(elements_array_four, sample_sub_six, sample_sub_seven,
                                elements_array_five, section)
            generate_sub_elements(elements_array_five, sample_sub_seven, None, None, section)

            # if there are major added sections we add them
            # reuses flow from above, but starting from sub_three list, as they are all placed there 
            def add_extra_section(section_parent, section_child, number_of_sections):
                
                for number in range(0, number_of_sections+1):
                    # new_section is the new sample section created above
                    for child in new_section:
                        if child.tag == section_parent:
                            section = xml.SubElement(child, f'{section_child}_{number}')
                            break

                    for tag in sample_sub_three[section_child[0:-4]]:
                        tag_element = xml.SubElement(section, f'{tag}{section_child[-4:]}_{number}')

                        if tag in sample_sub_four.keys():
                            for i in sample_sub_four[tag]:
                                j = xml.SubElement(tag_element, f'{i}{section_child[-4:]}_{number}')

                                if i in sample_sub_five.keys():
                                    for k in sample_sub_five[i]:
                                        l = xml.SubElement(j, f'{k}{section_child[-4:]}_{number}')

                                        if k in sample_sub_six.keys():
                                            for m in sample_sub_six[k]:
                                                n = xml.SubElement(l, f'{m}{section_child[-4:]}_{number}')

                                                if m in sample_sub_seven.keys():
                                                    for o in sample_sub_seven[m]:
                                                        xml.SubElement(n, f'{o}{section_child[-4:]}_{number}')

            # # we count how many major sections should be added 
            layer_count = -1
            for key in text_info.keys():
                tag_name = text_info[key][1]
                if tag_name[-1].isdigit() and tag_name[-2] == "_" and not "_added" in tag_name and not "_inner" in tag_name:
                    if text_info[key][0] == "layer":
                        if int(tag_name[-1]) > layer_count:
                            layer_count = int(tag_name[-1])

            # call the function above with the parent tag, section tag, and the count
            if layer_count >= 0:
                add_extra_section(f'layers{section}', f'layer{section}', layer_count)

            # import_mode_zer_inner_0
            added_section_material_inner = []
        
            for key in text_info.keys():
                tag_name = text_info[key][1]

                if section in tag_name and "_inner" in tag_name and not "_added" in tag_name:
                    index = tag_name.index(section)
                    if tag_name[index:] not in added_section_material_inner:
                        added_section_material_inner.append(tag_name[index:])
            
            if len(added_section_material_inner) > 0:
                add_inner_section(f'sample{section}', added_section_material_inner, True)

            # loop to add added sections for added sample
            for key in text_info.keys():
                tag_name = text_info[key][1]
                is_added_sample = False

                for section in large_sections:
                    if section in tag_name:
                        is_added_sample = True

                # look for the "_added" mark
                if "_added" in tag_name and is_added_sample:
                    parent = text_info[key][0]
                    original_parent = parent

                    section_specifier = ""
                    rest_to_add = ""

                    # get the section to make the right cut in the string
                    for section in large_sections:
                        if section in tag_name:
                            index = tag_name.index(section)
                            cut_off = tag_name[index:]
                            if cut_off[5].isdigit() and not "_inner" in cut_off:
                                # _zer_0_added_0
                                section_specifier = cut_off[0:6]
                                parent += cut_off[0:6]
                                rest_to_add = cut_off
                                break
                            elif not cut_off[5].isdigit() and not "_inner" in cut_off:
                                # _zer_added_0
                                section_specifier = cut_off[0:4]
                                parent += cut_off[0:4]
                                rest_to_add = cut_off
                                break
                            elif cut_off[5].isdigit() and "_inner" in cut_off:
                                # _zer_0_inner_0_added_0
                                section_specifier = cut_off[0:14]
                                parent = cut_off[0:14]
                                rest_to_add = cut_off
                                break
                            elif not cut_off[5].isdigit() and "_inner" in cut_off:
                                # _zer_inner_0_added_0
                                section_specifier = cut_off[0:12]
                                parent = cut_off[0:12]
                                rest_to_add = cut_off
                                break

                    iteration_name = original_parent+"s"+section_specifier
                    single_field = False

                    if "owner_databases" in parent or "experimentalists" in parent:
                        iteration_name = original_parent+section_specifier
                        single_field = True

                    for el in new_section.iter(iteration_name):
                        # Check if the basic constituents (parent) tag is already created, if not create it
                        if not single_field:
                            if len(el) == 1:
                                added_fields_section = xml.SubElement(el, original_parent+rest_to_add)
                                xml.SubElement(added_fields_section, tag_name)
                            else:
                                for element in el.iter(original_parent+rest_to_add):
                                    xml.SubElement(element, tag_name)
                        else:
                            xml.SubElement(el, tag_name)
    
    # add text
    for key in text_info.keys():
        sample_section = sample

        for section in large_sections:
            if section in text_info[key][1]:
                for child in root.iter(f'sample{section}'):
                    sample_section = child
                    break
                    
        double_check = []
        for element in sample_section.iter(text_info[key][1]):
            if not element.text:
                for child in sample_section.iter():
                    if child.findall(element.tag):
                        if [child.tag[32:], element.tag] not in double_check:
                            double_check.append([child.tag[32:], element.tag])
                            parent = child.tag[32:]
                            element.text = text_info[key][2]
                            break
                        else:
                            continue

    # clean up naming - works!
    names_to_remove = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_added", "_inner", "_zer", "_one", "_two", "_thr", "_fou"]
    for element in root.iter():
        for name in names_to_remove:
            if name in element.tag:
                element.tag = element.tag.replace(name, "")


    # preparing file, adding indent
    tree = xml.ElementTree(root)
    xml.indent(tree, '  ')

    # taking filename parameter and creating xml file
    with open(fileName,"wb") as files:
        tree.write(files, encoding="utf-8", xml_declaration=True)


def generateXMLExperiment(fileName, text_info):
    """
    function that creates a xml file for the "experiment" import
    One dictionary for each sub level of tags
    """
    
    root = xml.Element('import')
    root.set("type", "experiment")
    root.set("ssdm_version", "0.9.0")
    root.set("xmlns", "http://sshade.eu/schema/import")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://sshade.eu/schema/import http://sshade.eu/schema/import-0.9.xsd")
    
    # create elements to add
    experiment = xml.Element("experiment")
    root.append(experiment)       

    # array of all experiment direct children
    experiment_sub_one = ["import_mode", "uid", "owner_databases", "experimentalists",
                   "types", "title", "description", "date_begin", "date_end", "parent_experiment_uid",
                   "laboratory_uid", "body", "geolocations", "variable_parameters_types",
                   "variable_parameters_comments", "parameters_instruments", "comments", "preview",
                   "images", "documentations", "publications", "publication_comments", "sponsors",
                   "spectra"]

    first_sub_level = []
    
    for sub_el in experiment_sub_one:
        elm = xml.SubElement(experiment, sub_el)
        first_sub_level.append(elm)

    # dictionary of arrays of all the sub-sub elements
    experiment_sub_two = {
        "owner_databases": ["database_uid"],
        "experimentalists": ["experimentalist_uid"],
        "types": ["type"],
        "body": ["uid", "coordinate_system"],
        "geolocations": ["geolocation"],
        "variable_parameters_types": ["variable_parameters_type"],
        "parameters_instruments": ["parameters_instrument"],
        "preview": ["x", "y", "y2", "filename"],
        "images": ["image"],
        "documentations": ["documentation"],
        "publications": ["publication_uid"],
        "sponsors": ["sponsor"],
        "spectra": ["spectrum"],
    }

    # dictionary of arrays of all the sub x 2 elements
    experiment_sub_three = {
        "geolocation": ["place", "region", "country_code", "type", "coordinates"],
        "parameters_instrument": ["instrument_uid", "instrument_carrier", "instrument_sample_holder",
                                  "spectrum_scan_number", "spectral", "angle", "polarization",
                                  "spatial"],
        "image": ["filename", "caption"],
        "documentation": ["name", "filename"],
        "sponsor": ["acronym", "name", "award"],
        "spectrum": ["import_mode", "uid", "experiment_type", "chronologically_ordered",
                     "previous_spectrum_uid", "title", "type", "intensity_unit", "reference_position",
                     "reference_spectra", "model_parameters", "sample", "parameters_instruments",
                     "date_begin", "time_begin", "date_end", "time_end", "previous_version", "history",
                     "analysis", "quality_flag", "spectrum_validators", "comments", "spectrum_publications",
                     "publication_comments", "files", "export_filename", "experiment_preview", "bands",
                     ]
    }

    # dictionary of arrays of all the sub x 3 elements
    experiment_sub_four = {
        "coordinates": ["coordinate"],
        "spectral": ["unit", "standard", "observation_mode", "range_types", "ranges", "filters",
                     "comments"],
        "angle": ["observation_geometry", "observation_mode", "incidence", "emergence", "azimuth",
                  "phase", "resolution_illumination", "resolution_observation", "comments"],
        "polarization": ["type_illumination", "type_observation", "polarizer_illumination",
                         "polarizer_observation", "rejection_illumination", "rejection_observation",
                         "angle_illumination", "angle_observation", "comments"],
        "spatial": ["observation_mode", "unit", "objective", "spots_number", "sampling_x", "sampling_y",
                    "measures_x", "measures_y", "extent_x", "extent_y", "resolutions", "comments"],
        "reference_spectra": ["spectrum_uid"],
        "sample": ["uid", "changes", "comments", "primary_constituents"],
        "parameters_instruments": ["parameters_instrument"],
        "previous_version": ["status", "comments", "new_spectrum_uid"],
        "spectrum_validators": ["spectrum_experimentalist_uid"],
        "spectrum_publications": ["publication_uid"],
        "files": ["parameter", "file"],
        "experiment_preview": ["flag"],
        "bands": ["band"]
    }

    # dictionary of arrays of all the sub x 4 elements
    experiment_sub_five = {
        "range_types": ["type"],
        "ranges": ["range"],
        "filters": ["filter"],
        "resolutions": ["resolution"],
        "primary_constituents": ["primary_constituent"],
        "parameters_instrument": ["instrument_uid", "spectral"],
        "parameter": ["type", "format", "header_lines_number"],
        "file": ["filename"],
        "band": ["position_min", "position_peak", "position_max", "peak_intensity_relative",
                 "primary_constituent_uid", "primary_specie_uid", "transition_chemical_bonds",
                 "transition_assignment", "vibration_mode", "rotation_mode", "phonon_mode", "label",
                 "comments"],
        "coordinate": ["latitude", "longitude", "altitude"]
    }

    # dictionary of arrays of all the sub x 5 elements
    experiment_sub_six = {
        "range": ["min", "max", "absorption_edge_element_uid", "absorption_edge_type", "sampling",
                  "resolution", "position_error"],
        "filter": ["type", "place", "center", "width"],
        "resolution": ["width", "width_error", "position"],
        "primary_constituent": ["constituent_uid", "constituent_comments"],
        "spectral": ["spectrum_ranges"],
        "transition_chemical_bonds": ["chemical_bond_uid"]
    }

    # dictionary of arrays of all the sub x 6 elements
    experiment_sub_seven = {
        "spectrum_ranges": ["spectrum_range"],
    }

    # dictionary of arrays of all the sub x 7 elements
    experiement_sub_eight = {
        "spectrum_range": ["spectrum_min", "spectrum_max"]
    }

    elements_array = []
    elements_array_two = []
    elements_array_three = []
    elements_array_four = []
    elements_array_five = []
    elements_array_six = []

    # adding sub elements to the children of experiment
    # saving element reference in array for next
    # keys x, y, and y2 get attributes
    for key in experiment_sub_two:
        for child in experiment:
            if child.tag == key:
                for val in experiment_sub_two[key]:
                    xml.SubElement(child, val)
                    # add element to array
                    if val in experiment_sub_three.keys():
                        elements_array.append(child.find(val))
                    if val == 'x' or val == 'y' or val == 'y2':
                        element = child.find(val)
                        element.set("axis", '')
                        element.set("min", '')
                        element.set("max", '')
                    if val == 'x' or val == 'y':
                        element.set('unit', '')
                    if val == 'y' or val == 'y2':
                        element.set('offset', '')
                        

    # create reusale function that adds elements and adds element references to next array
    def generate_sub_elements(array, dict, dict_next, array_add):
        for i in array:
            for key in dict.keys():
                if i.tag == key:    
                    for val in dict[i.tag]:
                        xml.SubElement(i, val)
                        # add element to array two
                        if dict_next:
                            if val in dict_next.keys():
                                array_add.append(i.find(val))
    
    generate_sub_elements(elements_array, experiment_sub_three, experiment_sub_four,
                          elements_array_two)

    generate_sub_elements(elements_array_two, experiment_sub_four, experiment_sub_five,
                          elements_array_three)

    generate_sub_elements(elements_array_three, experiment_sub_five, experiment_sub_six,
                          elements_array_four)
                          
    generate_sub_elements(elements_array_four, experiment_sub_six, experiment_sub_seven,
                          elements_array_five)

    generate_sub_elements(elements_array_five, experiment_sub_seven, None, None)

    generate_sub_elements(elements_array_five, experiment_sub_seven, experiement_sub_eight,
                          elements_array_six)

    generate_sub_elements(elements_array_six, experiement_sub_eight, None, None)

    # if there are major added sections we add them
    # reuses flow from above, but starting from sub_three list, as they are all placed there 
    def add_section(section_parent, section_child, number_of_sections):
        # set section
        if number_of_sections >= 0:

            for number in range(0, number_of_sections+1):

                for child in experiment:
                    if child.tag == section_parent:
                        section = xml.SubElement(child, f'{section_child}_{number}')

                for tag in experiment_sub_three[section_child]:
                    tag_element = xml.SubElement(section, f'{tag}_{number}')

                    if tag in experiment_sub_four.keys():
                        for i in experiment_sub_four[tag]:
                            j = xml.SubElement(tag_element, f'{i}_{number}')

                            if i in experiment_sub_five.keys():
                                for k in experiment_sub_five[i]:
                                    l = xml.SubElement(j, f'{k}_{number}')

                                    if k in experiment_sub_six.keys():
                                        for m in experiment_sub_six[k]:
                                            n = xml.SubElement(l, f'{m}_{number}')

                                            if m in experiment_sub_seven.keys():
                                                for o in experiment_sub_seven[m]:
                                                    p = xml.SubElement(n, f'{o}_{number}')

                                                    if o in experiement_sub_eight.keys():
                                                        for q in experiement_sub_eight[o]:
                                                            xml.SubElement(p, f'{q}_{number}')

    # there are three major sections possible to add
    # we count how many should be 
    geolocation_count = -1
    parameters_instrument_count = -1
    spectrum_count = -1
    for key in text_info.keys():
        tag_name = text_info[key][1]
        if tag_name[-1].isdigit() and tag_name[-2] == "_" and not "_added" in tag_name and not "_inner" in tag_name:
            if text_info[key][0] == "geolocation":
                if int(tag_name[-1]) > geolocation_count:
                    geolocation_count = int(tag_name[-1])
            elif text_info[key][0] == "spectrum":
                if int(tag_name[-1]) > spectrum_count:
                    spectrum_count = int(tag_name[-1])
            elif text_info[key][0] == "parameters_instrument":
                if int(tag_name[-1]) > parameters_instrument_count:
                    parameters_instrument_count = int(tag_name[-1])
    
    # call the function above with the parent tag, section tag, and the count
    add_section("geolocations", "geolocation", geolocation_count)
    add_section("parameters_instruments", "parameters_instrument", parameters_instrument_count)
    add_section("spectra", "spectrum", spectrum_count)


    # function to insert the inner sections inside the spectra tags
    # takes in the section name and an array of placements that specifies section
    # "_{number_of_section}_{number_of_inner_section}"
    def add_inner_section(section, placement):
        # getting the spectra tag
        for child in experiment.iter("spectra"):
            spectra = child

        for place in placement:

            # find specific spectrum
            if place[0] == "_" and place[1].isdigit():
                for child in spectra.iter(f'spectrum{place[0:2]}'):
                    correct_spectrum = child
                    number = place[0:2]
            else:
                for child in spectra.iter('spectrum'):
                    correct_spectrum = child
                    number = ""

            # find specific section
            for tag in correct_spectrum.iter(section+number):
                correct_section = tag

                # insert tags in section
                if section == "parameters_instruments":
                    parameters_instrument_inner = xml.SubElement(correct_section, f'parameters_instrument{place}')
                    xml.SubElement(parameters_instrument_inner, f'instrument_uid{place}')
                    xml.SubElement(parameters_instrument_inner, f'spectral{place}')
                    ranges = xml.SubElement(parameters_instrument_inner, f'spectrum_ranges{place}')
                    range_tag = xml.SubElement(ranges, f'spectrum_range{place}')
                    xml.SubElement(range_tag, f'spectrum_min{place}')
                    xml.SubElement(range_tag, f'spectrum_max{place}')
                elif section == "bands":
                    band_inner = xml.SubElement(correct_section, f'band{place}')
                    xml.SubElement(band_inner, f'position_min{place}')
                    xml.SubElement(band_inner, f'position_peak{place}')
                    xml.SubElement(band_inner, f'position_max{place}')
                    xml.SubElement(band_inner, f'peak_intensity_relative{place}')
                    xml.SubElement(band_inner, f'primary_constituent_uid{place}')
                    xml.SubElement(band_inner, f'primary_specie_uid{place}')
                    transition_chemical_bonds = xml.SubElement(band_inner, f'transition_chemical_bonds{place}')
                    xml.SubElement(transition_chemical_bonds, f'chemical_bond_uid{place}')
                    xml.SubElement(band_inner, f'transition_assignment{place}')
                    xml.SubElement(band_inner, f'vibration_mode{place}')
                    xml.SubElement(band_inner, f'rotation_mode{place}')
                    xml.SubElement(band_inner, f'phonon_mode{place}')
                    xml.SubElement(band_inner, f'label{place}')
                    xml.SubElement(band_inner, f'comments{place}')

    # create the arrays to be added in inner section function
    parameter_instrument_inner_to_add = []
    band_inner_to_add = []
    
    # loop to extract placement of tags
    # will only fill in one element per inner section
    for key in text_info.keys():
        tag_name = text_info[key][1]

        # check if it's an inner section with the "_inner" mark
        if tag_name[-1].isdigit() and tag_name[-2] == "_" and not "_added" in tag_name and "_inner" in tag_name:

            # cut off the placement text according to added section or not
            for i in range(0, len(tag_name)):

                # check if it belongs in an added section to keep the "_{number}" in front of "_inner"
                if tag_name[i] == "_" and tag_name[i+1].isdigit() and i < len(tag_name)-1:

                    if text_info[key][0] == "spectrum_parameters_instrument" and not tag_name[i:] in parameter_instrument_inner_to_add:
                        parameter_instrument_inner_to_add.append(tag_name[i:])
                    
                    elif text_info[key][0] == "band" and not tag_name[i:] in band_inner_to_add:
                        band_inner_to_add.append(tag_name[i:])

                    break
                # else just cut at "_inner"
                elif tag_name[i:i+6] == "_inner":
                    
                    if text_info[key][0] == "spectrum_parameters_instrument" and not tag_name[i:] in parameter_instrument_inner_to_add:
                        parameter_instrument_inner_to_add.append(tag_name[i:])
                    
                    elif text_info[key][0] == "band" and not tag_name[i:] in band_inner_to_add:
                        band_inner_to_add.append(tag_name[i:])
                        
                    break
    # call the function with inner section name and list of where to add it                 
    add_inner_section("parameters_instruments", parameter_instrument_inner_to_add)
    add_inner_section("bands", band_inner_to_add)


    # add added field(s)
    # list of tags that require multiple tags to be added
    list_of_multiple_fields = ["coordinate", "range", "filter", "resolution", "image", "documentation", "sponsor", "spectrum_range", "primary_constituent"]

    # loop to add the "_added" fields
    # chemical_bond_uid_0_inner_0_added_0 is added in transition_chemical_bonds_0
    # spectrum_ranges_0_inner_0_added_0 is added spectrum_ranges_0
    for key in text_info.keys():
        tag_name = text_info[key][1]

        # look for the "_added" mark
        if "_added" in tag_name:
            parent = text_info[key][0]
            multiple = False
            original_parent = ""
            if parent in list_of_multiple_fields:
                multiple = True
                original_parent = parent
            # chemical_bond_uid_0_inner_0_added_0
            # go through the tag to see if it belongs in an inner section
            # changes the parent name if needed
            # spectrum_ranges_0_inner_0_added_0
            for i in range(0, len(tag_name)):
                if tag_name[i] == "_" and tag_name[i+1].isdigit() and tag_name[i+2:i+8] == "_inner":
                    parent += tag_name[i:i+10]
                    break
                elif tag_name[i] == "_" and tag_name[i+1].isdigit() and not tag_name[i-5:i] == "inner" and i < len(tag_name)-2:
                    parent += tag_name[i:i+2]
                    break
                elif tag_name[i:i+6] == "_inner" and tag_name[i+8:i+14] == "_added":
                    parent += tag_name[i:i+8]
                    break
            
            # finds the parent and confirm that it's a single field
            for element in experiment.iter(parent):
                if text_info[key][0] not in list_of_multiple_fields:
                    xml.SubElement(element, tag_name)

            # if there are multiple fields to add
            if multiple:
                section_specifier = ""
                rest_to_add = ""
                for i in range(0, len(tag_name)):
                    # see if it's a section with inner
                    if tag_name[i] == "_" and tag_name[i+1].isdigit() and tag_name[i+2:i+8] == "_inner":
                        section_specifier = tag_name[i:i+10]
                        rest_to_add = tag_name[i:]
                        break
                    elif tag_name[i:i+6] == "_inner" and not tag_name[i-1].isdigit():
                        section_specifier = tag_name[i:i+8]
                        rest_to_add = tag_name[i:]
                        break
                    # if it's not in an added section
                    elif tag_name[i:i+6] == "_added" and not tag_name[i-1].isdigit():
                        rest_to_add = tag_name[i:]
                        break
                    elif tag_name[i:i+6] == "_added" and tag_name[i-1].isdigit():
                        section_specifier = tag_name[i-2:i]
                        rest_to_add = tag_name[i-2:]
                        
                for el in experiment.iter(original_parent+"s"+section_specifier): 
                    # Check if the parent tag is already created, if not create it
                    if len(el.findall(original_parent+"s"+rest_to_add)) == 0:
                        added_fields_section = xml.SubElement(el, original_parent+"s"+rest_to_add)
                        xml.SubElement(added_fields_section, tag_name)
                    else:
                        for element in experiment.iter(original_parent+"s"+rest_to_add):
                            xml.SubElement(element, tag_name)

    # add text
    for key in text_info.keys():
        for element in experiment.iter(text_info[key][1]):
            if not element.text:
                element.text = text_info[key][2]

    # remove names
    names_to_remove = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_added", "_inner"]
    for element in root.iter():
        for name in names_to_remove:
            if name in element.tag:
                element.tag = element.tag.replace(name, "")
            if element.tag[0:9] == "spectrum_":
                element.tag = element.tag[9:]

    # preparing file, adding indent
    tree = xml.ElementTree(root)
    xml.indent(tree, '  ')

    # taking filename parameter and creating xml file
    with open(fileName,"wb") as files:
        tree.write(files, encoding="utf-8", xml_declaration=True)


def generateXMLPublication(fileName, text_info):
    """
    function that creates a xml file for the "sample" import
    One dictionary for each sub level of tags
    """
    
    root = xml.Element('import')
    root.set("type", "publication")
    root.set("ssdm_version", "0.9.0")
    root.set("xmlns", "http://sshade.eu/schema/import")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://sshade.eu/schema/import http://sshade.eu/schema/import-0.9.xsd")
    
    # create elements to add
    publication = xml.Element("publication")
    root.append(publication)

    # array of all publication direct children
    publication_sub_one = ["import_mode", "uid", "type", "document_type",
                   "state", "access_right", "access_free_date", "authors", "year", "title",
                   "journal", "volume", "number", "first_page", "last_page", "pages_number",
                   "abstract", "keywords", "conference", "book", "editor", "publisher",
                   "publisher_city", "dataset", "doi", "identifiers", "filename", "contents",
                   "cited_publications", "used_experiments", "used_bandlists", "comments"]
    first_sub_level = []

    for sub_el in publication_sub_one:
        elm = xml.SubElement(publication, sub_el)
        first_sub_level.append(elm)

    # dictionary of arrays of all the sub-sub elements
    publication_sub_two = {
        "authors": ["author"],
        "keywords": ["keyword"],
        "conference": ["name", "location", "date"],
        "book": ["chapter_number", "title", "series", "edition_number"],
        "dataset": ["database_name", "database_url"],
        "identifiers": ["identifier"],
        "contents": ["content"],
        "cited_publications": ["publication_uid"],
        "used_experiments": ["experiment_uid"],
        "used_bandlists": ["bandlist_uid"],
    }

    # dictionary of arrays of all the sub x 2 elements
    publication_sub_three = {
        "author": ["first_name", "family_name"],
        "identifier": ["type", "code", "url"],
    }

    elements_array = []

    # adding sub elements to the children of publication
    # saving element reference in array for next
    for key in publication_sub_two:
        for child in publication:
            if child.tag == key:
                for val in publication_sub_two[key]:
                    xml.SubElement(child, val)
                    # add element to array
                    if val in publication_sub_three.keys():
                        elements_array.append(child.find(val))

    for i in elements_array:
        for key in publication_sub_three.keys():
            if i.tag == key:
                for val in publication_sub_three[i.tag]:
                    xml.SubElement(i, val)

    large_sections = ["_zer", "_one", "_two", "_thre", "_fou"]
    # loop to add "_added" fields
    for key in text_info.keys():
        tag_name = text_info[key][1]
        is_added_sample = False

        for section in large_sections:
            if section in tag_name:
                is_added_sample = True
        

        # look for the "_added" mark
        if "_added" in tag_name and not is_added_sample:
            parent = text_info[key][0]
            index = tag_name.index("_added")
            to_add = tag_name[index:]
            single_field = True

            if parent == "identifier" or parent == "author":
                single_field = False

            if not single_field:
                for main_parent in publication.iter(parent+"s"):
                    if len(main_parent.findall(parent+to_add)) == 0:
                        # only the identifier is a section
                        identifier_section = xml.SubElement(main_parent, parent+to_add)
                        xml.SubElement(identifier_section, tag_name)
                    else:
                        for element in publication.iter(parent+to_add):
                            xml.SubElement(element, tag_name)
            else:
                for child in publication.iter(parent):
                    xml.SubElement(child, tag_name)
            


    large_sections_to_add = []
    for key in text_info.keys():
        char_count = text_info[key][1]
        if char_count[-4:] in large_sections and not char_count[-4:] in large_sections_to_add:
            large_sections_to_add.append(char_count[-4:])

    if len(large_sections_to_add) > 0:
        for section in large_sections_to_add:
            elements_array = []
            
            new_section = xml.Element(f'publication{section}')
            root.append(new_section)
            for sub_el in publication_sub_one:
                xml.SubElement(new_section, sub_el+section)

            for key in publication_sub_two:
                for child in new_section:
                    if child.tag == key+section:
                        for val in publication_sub_two[key]:
                            xml.SubElement(child, val+section)
                            # add element to array
                            if val in publication_sub_three.keys():
                                elements_array.append(child.find(val+section))

            for i in elements_array:
                for key in publication_sub_three.keys():
                    if i.tag[0:-4] == key:
                        for val in publication_sub_three[i.tag[0:-4]]:
                            xml.SubElement(i, val+section)

            for key in text_info.keys():
                tag_name = text_info[key][1]
                is_added_sample = False

                if section in tag_name:
                    is_added_sample = True
                

                # look for the "_added" mark
                if "_added" in tag_name and is_added_sample:
                    parent = text_info[key][0]
                    index = tag_name.index("_added")
                    to_add = tag_name[index:]
                    single_field = True
                    if parent == "identifier" or parent == "author":
                        single_field = False
                    
                    # single_field = False
                    if not single_field:
                        for main_parent in new_section.iter(parent+"s"+section):

                            if len(main_parent.findall(parent+section+to_add)) == 0:
                                # only the identifier is a section
                                identifier_section = xml.SubElement(main_parent, parent+section+to_add)
                                xml.SubElement(identifier_section, tag_name)
                            else:
                                for element in new_section.iter(parent+section+to_add):
                                    xml.SubElement(element, tag_name)
                    else:
                        for child in new_section.iter(parent+section):
                            xml.SubElement(child, tag_name)

    # add text
    for key in text_info.keys():
        publication_section = publication

        for section in large_sections:
            if section in text_info[key][1]:
                for child in root.iter(f'publication{section}'):
                    publication_section = child
                    break
        
        for element in publication_section.iter(text_info[key][1]):
            if not element.text:
                element.text = text_info[key][2]


    names_to_remove = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_added", "_zer", "_one", "_two", "_thr", "_fou"]
    for element in root.iter():
        for name in names_to_remove:
            if name in element.tag:
                element.tag = element.tag.replace(name, "")

    # preparing file, adding indent
    tree = xml.ElementTree(root)
    xml.indent(tree, '  ')

    # taking filename parameter and creating xml file
    with open(fileName,"wb") as files:
        tree.write(files, encoding="utf-8", xml_declaration=True)