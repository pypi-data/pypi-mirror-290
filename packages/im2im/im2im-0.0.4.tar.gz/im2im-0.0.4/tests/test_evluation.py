from src.im2im import get_possible_metadata, im2im_code, find_target_metadata


def test_a():
    source = get_possible_metadata("opencv.bgr")
    target = get_possible_metadata("skimage.gray")

    actual_code = im2im_code("source_image", source, "target_image", {**target, 'image_data_type': 'uint8'})
    expected_code = 'import cv2\ntarget_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)'
    assert actual_code == expected_code

def test():
    import numpy as np
    from im2im import Image, im2im

    # Create a numpy.ndarray with shape (h, w, 3) in uint8 format
    image = np.random.randint(0, 256, (20, 20, 3), dtype=np.uint8)

    # Initialize the image with corresponding metadata preset
    from_im = Image(image, "skimage.rgb_uint8")

    # Convert the image to a torch tensor with shape (1, 3, h, w), float32 format,
    # normalized to the range [0, 1], and transferred to the GPU
    to_im = im2im(from_im, "torch.gpu")

    # The converted image data is accessible via to_im.raw_image

def test_b():
    source = get_possible_metadata("skimage.gray")
    target = get_possible_metadata("pil.rgb_uint8")
    actual_code = im2im_code("source_image", {**source, 'image_data_type': 'double'}, "target_image", {**source, 'image_data_type': 'uint8'})
    actual_code = im2im_code("source_image", {**source, 'image_data_type': 'double'}, "target_image", target)
    assert actual_code is None


def test_c():
    source = get_possible_metadata("numpy.gray")
    source['image_data_type'] = 'float64(0to1)'
    target = get_possible_metadata("torch.gray_gpu")
    actual_code = im2im_code("source_image", source, "target_image", target)
    expected_code = ('import torch\n'
                     'image = torch.from_numpy(source_image)\n'
                     'image = image.permute(2, 0, 1)\n'
                     'image = image.unsqueeze(0)\n'
                     'target_image = image / 255.0')
    assert actual_code == expected_code

def test_e():
    source = get_possible_metadata("numpy.gray")
    source['image_data_type'] = 'float64(0to1)'
    target =get_possible_metadata("numpy.gray")
    target['image_data_type'] = 'float32(0to1)'
    actual_code = im2im_code("source_image", source, "target_image", target)
    expected_code = ('import torch\n'
                     'image = torch.from_numpy(source_image)\n'
                     'image = image.permute(2, 0, 1)\n'
                     'image = image.unsqueeze(0)\n'
                     'target_image = image / 255.0')
    assert actual_code == expected_code



def test_d():
    source = get_predefined_metadata("torch.gray")

    target = get_predefined_metadata("numpy.gray")
    target['image_data_type'] = 'float32(0to1)'

    actual_code = im2im_code("source_image", source, "target_image", target)
    expected_code = ('import torch\n'
                     'image = torch.from_numpy(source_image)\n'
                     'image = image.permute(2, 0, 1)\n'
                     'image = image.unsqueeze(0)\n'
                     'target_image = image / 255.0')
    assert actual_code == expected_code



def test_f():
    a = {**get_possible_metadata('skimage.gray'), 'image_data_type': 'uint8'}

    b = find_target_metadata(a, 'skimage.before_gaussian')
    c = {**b, 'image_data_type': 'float64(0to1)'}


    d = find_target_metadata(c, "torch.gpu")

    actual_code = im2im_code("source_image", c, "target_image", d)



    e = find_target_metadata(d, 'skimage.before_gaussian')
    actual_code2 = im2im_code("source_image", d, "target_image", e)
    print('h')
#
#     before_equalize_adapthist = find_target_metadata(target, "before_equalize_adapthist")
#     actual_code = im2im_code("source_image", target, "target_image", before_equalize_adapthist)
#
#     assert actual_code == None
#
# raw_image = Image(imread('image.tif', as_gray=True), )
#
#
# out_im = Image(gaussian_filtered, {**in_im.metadata, 'image_data_type': 'float64(0to1)'})
#

#
# in_im = im2im(out_im2, 'before_equalize_adapthist')
# contrast_enhanced = equalize_adapthist(in_im.raw_image)
# out_im3 = Image(contrast_enhanced, {**in_im.metadata, 'image_data_type': 'float64(0to1)'})