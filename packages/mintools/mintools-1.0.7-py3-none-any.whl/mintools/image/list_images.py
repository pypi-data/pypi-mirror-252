import os
import pandas as pd
from pathlib import Path


class listFiles(object):
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def list_single_folder(self, absolute_path=False):
        filenames = os.listdir(self.root_dir)
        if absolute_path:
            filenames = [os.path.join(self.root_dir, filename) for filename in filenames]
        return filenames

    def list_subfolders(self, relpath=None):
        file_paths = []
        for root, directories, files in os.walk(self.root_dir):
            for filename in files:
                absolute_path = os.path.join(root, filename)
                file_paths.append(absolute_path)

        if relpath is not None:
            file_paths = [os.path.relpath(absolute, relpath) for absolute in file_paths]
        return file_paths

    def csv_generator_for_segmentation_dataset(self, subPaths=None, custom_key=None, csv_param=None):
        if csv_param is None:
            csv_param = {'image_column': 'image', 'encoding': 'gbk'}
        if subPaths is None:
            subPaths = ['train', 'val', 'test']
        meta_dir = os.path.join(self.root_dir, 'meta')
        for choice in subPaths:
            path = os.path.join(self.root_dir, choice, 'images')
            if os.path.exists(path):
                # filename_list = [filename for filename in path.glob("*")]
                filenames = os.listdir(path)
                if custom_key is not None:
                    filenames = sorted(filenames, reverse=False, key=custom_key)
                dataframe = pd.DataFrame({csv_param['image_column']: filenames})
                csv_name = os.path.join(meta_dir, f'{choice}.csv')
                dataframe.to_csv(csv_name, index=False, encoding=csv_param['encoding'])


def gen_txt_from_dir(root_dir, custom_key=None):
    """
    save image names of a fold in txt
    :param root_dir:
    :param custom_key:
    :return:
    """
    path = Path(root_dir)
    filename_list = [p for p in path.glob("*")]
    if custom_key is not None:
        filename_list = sorted(filename_list, reverse=False, key=custom_key)

    txt = os.path.join(path.parent, f'{path.name}.txt')
    with open(txt, mode='w') as file:
        for filename in filename_list:
            file.write(filename.name + '\n')
            # img = cv2.imread(str(filename), -1)


# if __name__ == '__main__':
#     aa = get_image_names(path, base_path=path)
#     bb = 0
