import os
import cv2
import numpy as np
import SimpleITK as sitk
from pathlib import Path


def readNii(filename: str, data_type=np.uint8, print_size=False):
    img = sitk.ReadImage(filename)
    # print the image size, (Depth, Height, Width)
    if print_size:
        print("nii data size (Depth, Height, Width):", img.GetSize())
    data = sitk.GetArrayFromImage(img)
    return np.array(data, dtype=data_type)


def arr2nii(src, dst_filename, reference_name=None):
    """
    save a numpy array as nifty image
    inputs:
        data: a numpy array with shape [Depth, Height, Width]
        filename: the ouput file name
        reference_name: file name of the reference image of which affine and header are used
    outputs: None
    """
    img = sitk.GetImageFromArray(src)
    if (reference_name is not None):
        img_ref = sitk.ReadImage(reference_name)
        img.CopyInformation(img_ref)
    sitk.WriteImage(img, dst_filename)


# def nii2img_from_txt(nii_filename, txt, saved_img_suffix=None, is_gt=False, foreground_pixel=255):
#     """
#     save img from nii file using a name list in txt file
#     :param nii_filename:
#     :param txt:
#     :param saved_img_suffix:
#     :param foreground_pixel:
#     :return:
#     """
#     with open(txt, mode='r', encoding='utf-8') as f:
#         lines = f.readlines()
#     filename_list = [Path(line.strip()) for line in lines if line.strip() != '']
#     nii_filename = Path(nii_filename)
#     nii_data = readNii(str(nii_filename), np.uint8)
#     assert len(filename_list) == nii_data.shape[0]
#     save_dir_name = Path(os.path.join(nii_filename.parent, nii_filename.name.split('.')[0]))
#     save_dir_name.mkdir(parents=True, exist_ok=True)
#
#     for i, filename in enumerate(filename_list):
#         data = nii_data[i]
#         if data.ndim == 3:
#             data = data[:, :, ::-1]
#         if is_gt:
#             data[data != 0] = foreground_pixel
#         name = filename.name if saved_img_suffix is None else (filename.stem + saved_img_suffix)
#         temp_path = os.path.join(save_dir_name, name)
#         cv2.imwrite(temp_path, data)


# def img2nii_from_txt(root_dir, txt, nii_filename, data_type=np.uint8, is_gt=False, foreground_pixel=1, na='fill', img_size=(512,512)):
#     """
#     save img to nii file using a name list in txt file
#     :param nii_filename:
#     :param txt:
#     :param saved_img_suffix:
#     :param foreground_pixel:
#     :return:
#     """
#     with open(txt, mode='r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     filename_list = [Path(root_dir).joinpath(Path(line.strip())) for line in lines if line.strip() != '']
#     nii_file = []
#     for i, filename in enumerate(filename_list):
#         img = None
#         if filename.is_file():
#             img = cv2.imread(str(filename), -1)
#         elif na == 'fill':
#             img = np.zeros(img_size)
#         elif na == 'skip':
#             continue
#         nii_file.append(img)
#     nii_file = np.array(nii_file, dtype=data_type)
#
#     if is_gt:
#         nii_file[nii_file != 0] = foreground_pixel
#     arr2nii(nii_file, nii_filename)

def nii2img(nii_filename, filename_list, save_dir_name=None, saved_img_suffix=None, is_gt=False, foreground_pixel=255):
    """
    save img from nii file using a name list in txt file
    :param nii_filename:
    :param saved_img_suffix:
    :param foreground_pixel:
    :return:
    """
    nii_filename = Path(nii_filename)
    nii_data = readNii(str(nii_filename), np.uint8)
    assert len(filename_list) == nii_data.shape[0]
    if save_dir_name is None:
        save_dir_name = Path(os.path.join(nii_filename.parent, nii_filename.name.split('.')[0]))
        save_dir_name.mkdir(parents=True, exist_ok=True)

    for i, filename in enumerate(filename_list):
        data = nii_data[i]
        if data.ndim == 3:
            data = data[:, :, ::-1]
        if is_gt:
            data[data != 0] = foreground_pixel
        name = filename.name if saved_img_suffix is None else (filename.stem + saved_img_suffix)
        temp_path = os.path.join(save_dir_name, name)
        cv2.imwrite(temp_path, data)


def img2nii(filename_list, nii_filename, data_type=np.uint8, is_gt=False, foreground_pixel=1, na='fill', img_size=(512,512)):
    """
    save img to nii file using a name list in txt file
    :param nii_filename:
    :param txt:
    :param saved_img_suffix:
    :param foreground_pixel:
    :return:
    """
    nii_file = []
    for i, filename in enumerate(filename_list):
        img = None
        if filename.is_file():
            img = cv2.imread(str(filename), -1)
        elif na == 'fill':
            img = np.zeros(img_size)
        elif na == 'skip':
            continue
        nii_file.append(img)
    nii_file = np.array(nii_file, dtype=data_type)

    if is_gt:
        nii_file[nii_file != 0] = foreground_pixel
    arr2nii(nii_file, nii_filename)



if __name__ == '__main__':
    # gen_txt_for_nii("data/regular/fundus/imgs50", custom_key=lambda x: x.stem)
    nii_file = 'data/regular/trainvaltest/gts_GT.nii.gz'
    # print('0', id(nii_file))
    nii2img(nii_file, 'data/regular/trainvaltest/meta/train.txt', '.png')
    # print('3', id(nii_file))