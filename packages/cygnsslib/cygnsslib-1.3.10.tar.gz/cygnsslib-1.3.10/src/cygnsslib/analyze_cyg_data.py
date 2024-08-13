import argparse
import json
import os
from collections import defaultdict
from cygnsslib.plotting import plot_varying_sp_inc_angle, plot_varying_sc_az_angle, plot_reflectivity_x_az_lg_inc_angle


# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to group data by 'smap_sm', 'sc_alt', 'sp_inc_angle', and 'sc_az_angle' values
def group_data(data):
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for _, item in data.items():
        smap_sm = item.get('smap_sm')
        sc_alt = item.get('sc_alt')
        sp_inc_angle = item.get('sp_inc_angle')
        sc_az_angle = item.get('sc_az_angle')

        if smap_sm is not None and sc_alt is not None and sp_inc_angle is not None and sc_az_angle is not None:
            # Determine the smap_sm group by 0.05 ranges
            smap_sm_group = int(smap_sm // 0.05) * 0.05
            # Determine the sc_alt group by 10000 ranges
            sc_alt_group = int(sc_alt // 10000) * 10000
            # Determine the sp_inc_angle group by 5 ranges
            sp_inc_angle_group = int(sp_inc_angle // 5) * 5
            # Determine the sc_az_angle group by 5 ranges
            sc_az_angle_group = int(sc_az_angle // 5) * 5

            grouped_data[smap_sm_group][sc_alt_group][sp_inc_angle_group][sc_az_angle_group].append(item)

    return grouped_data



def analyze_cyg(json_fp, fig_save_types=None):
    if fig_save_types is None:
        fig_save_types = ['png']
    fn_split = os.path.basename(json_fp).split('_')
    _tag_idx = [idx for idx, txt in enumerate(fn_split) if txt.isnumeric()]
    if not _tag_idx:
        _tag_idx = 2
    else:
        _tag_idx = _tag_idx[0]
    img_tag = '_'.join(fn_split[:(_tag_idx+1)])

    data = load_json(json_fp)
    img_folder_name = f'{img_tag}_plots'
    folder_path = os.path.join(os.path.dirname(json_fp), img_folder_name)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    grouped_data = group_data(data)
    # plot_varying_sp_inc_angle(grouped_data, folder_path, img_tag, fig_save_types)
    # plot_varying_sc_az_angle(grouped_data, folder_path, img_tag, fig_save_types)
    plot_reflectivity_x_az_lg_inc_angle(grouped_data, folder_path, img_tag, fig_save_types)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot reflectivity')
    parser.add_argument('input_path', type=str, help='Path to JSON file or folder has json files')
    parser.add_argument('--img_save_type', nargs='+', default=None, type=str, help='Image save types, i.e. png svg pdf')

    args = parser.parse_args()
    if os.path.isdir(args.input_path):
        fps = [f.path for f in os.scandir(args.input_path) if f.name.endswith('.json')]
    else:
        fps = [args.input_path]
    for fp in fps:
        print(fp)
        analyze_cyg(fp, args.img_save_type)
