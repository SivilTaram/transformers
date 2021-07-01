# coding=utf-8
# Copyright 2021 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

import numpy as np

from transformers.file_utils import is_torch_available, is_vision_available
from transformers.testing_utils import require_torch, require_vision

from .test_feature_extraction_common import FeatureExtractionSavingTestMixin, prepare_image_inputs


if is_torch_available():
    import torch

if is_vision_available():
    from PIL import Image

    from transformers import SegFormerFeatureExtractor


class SegFormerFeatureExtractionTester(unittest.TestCase):
    def __init__(
        self,
        parent,
        batch_size=7,
        num_channels=3,
        min_resolution=30,
        max_resolution=400,
        do_resize=True,
        keep_ratio=True,
        image_scale=(100,20),
        align=True,
        size_divisor=10,
        do_random_crop=True,
        crop_size=(20,20),
        do_normalize=True,
        image_mean=[0.5, 0.5, 0.5],
        image_std=[0.5, 0.5, 0.5],
    ):
        self.parent = parent
        self.batch_size = batch_size
        self.num_channels = num_channels
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.do_resize = do_resize
        self.keep_ratio = keep_ratio
        self.image_scale = image_scale
        self.align = align
        self.size_divisor = size_divisor
        self.do_random_crop = do_random_crop
        self.crop_size = crop_size
        self.do_normalize = do_normalize
        self.image_mean = image_mean
        self.image_std = image_std

    def prepare_feat_extract_dict(self):
        return {
            "do_resize": self.do_resize,
            "keep_ratio": self.keep_ratio,
            "image_scale": self.image_scale,
            "align": self.align,
            "size_divisor": self.size_divisor,
            "do_random_crop": self.do_random_crop,
            "crop_size": self.crop_size,
            "do_normalize": self.do_normalize,
            "image_mean": self.image_mean,
            "image_std": self.image_std,
        }


@require_torch
@require_vision
class SegFormerFeatureExtractionTest(FeatureExtractionSavingTestMixin, unittest.TestCase):

    feature_extraction_class = SegFormerFeatureExtractor if is_vision_available() else None

    def setUp(self):
        self.feature_extract_tester = SegFormerFeatureExtractionTester(self)

    @property
    def feat_extract_dict(self):
        return self.feature_extract_tester.prepare_feat_extract_dict()

    def test_feat_extract_properties(self):
        feature_extractor = self.feature_extraction_class(**self.feat_extract_dict)
        self.assertTrue(hasattr(feature_extractor, "do_resize"))
        self.assertTrue(hasattr(feature_extractor, "keep_ratio"))
        self.assertTrue(hasattr(feature_extractor, "image_scale"))
        self.assertTrue(hasattr(feature_extractor, "align"))
        self.assertTrue(hasattr(feature_extractor, "size_divisor"))
        self.assertTrue(hasattr(feature_extractor, "do_random_crop"))
        self.assertTrue(hasattr(feature_extractor, "crop_size"))
        self.assertTrue(hasattr(feature_extractor, "do_normalize"))
        self.assertTrue(hasattr(feature_extractor, "image_mean"))
        self.assertTrue(hasattr(feature_extractor, "image_std"))
        

    def test_batch_feature(self):
        pass

    def test_call_pil(self):
        # Initialize feature_extractor
        feature_extractor = self.feature_extraction_class(**self.feat_extract_dict)
        # create random PIL images
        image_inputs = prepare_image_inputs(self.feature_extract_tester, equal_resolution=False)
        for image in image_inputs:
            self.assertIsInstance(image, Image.Image)

        # Test not batched input
        encoded_images = feature_extractor(image_inputs[0], return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                1,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size,
            ),
        )

        # Test batched
        encoded_images = feature_extractor(image_inputs, return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                self.feature_extract_tester.batch_size,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size[::-1],
            ),
        )

    def test_call_numpy(self):
        # Initialize feature_extractor
        feature_extractor = self.feature_extraction_class(**self.feat_extract_dict)
        # create random numpy tensors
        image_inputs = prepare_image_inputs(self.feature_extract_tester, equal_resolution=False, numpify=True)
        for image in image_inputs:
            self.assertIsInstance(image, np.ndarray)

        # Test not batched input
        encoded_images = feature_extractor(image_inputs[0], return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                1,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size[::-1],
            ),
        )

        # Test batched
        encoded_images = feature_extractor(image_inputs, return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                self.feature_extract_tester.batch_size,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size[::-1],
            ),
        )

    def test_call_pytorch(self):
        # Initialize feature_extractor
        feature_extractor = self.feature_extraction_class(**self.feat_extract_dict)
        # create random PyTorch tensors
        image_inputs = prepare_image_inputs(self.feature_extract_tester, equal_resolution=False, torchify=True)
        for image in image_inputs:
            self.assertIsInstance(image, torch.Tensor)

        # Test not batched input
        encoded_images = feature_extractor(image_inputs[0], return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                1,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size[::-1],
            ),
        )

        # Test batched
        encoded_images = feature_extractor(image_inputs, return_tensors="pt").pixel_values
        self.assertEqual(
            encoded_images.shape,
            (
                self.feature_extract_tester.batch_size,
                self.feature_extract_tester.num_channels,
                *self.feature_extract_tester.crop_size[::-1],
            ),
        )

    @require_torch
    def test_resize(self):
        # Initialize feature_extractor: version 1 (no align, keep_ratio=True)
        feature_extractor = SegFormerFeatureExtractor(image_scale=(1333, 800), align=False, do_random_crop=False)

        # Create random PyTorch tensor
        image = torch.randn((3, 288, 512))

        # Verify shape
        encoded_images = feature_extractor(image, return_tensors="pt").pixel_values
        expected_shape = (1, 3, 750, 1333)
        self.assertEqual(encoded_images.shape, expected_shape)

        # Initialize feature_extractor: version 2 (keep_ratio=False)
        feature_extractor = SegFormerFeatureExtractor(image_scale=(1280, 800), align=False, keep_ratio=False, do_random_crop=False)

        # Verify shape
        encoded_images = feature_extractor(image, return_tensors="pt").pixel_values
        expected_shape = (1, 3, 800, 1280)
        self.assertEqual(encoded_images.shape, expected_shape)

    @require_torch
    def test_aligned_resize(self):
        # Initialize feature_extractor: version 1
        feature_extractor = SegFormerFeatureExtractor(do_random_crop=False)
        # Create random PyTorch tensor
        image = torch.randn((3, 256, 304))

        # Verify shape
        encoded_images = feature_extractor(image, return_tensors="pt").pixel_values
        expected_shape = (1, 3, 512, 608)
        self.assertEqual(encoded_images.shape, expected_shape)

        # Initialize feature_extractor: version 2
        feature_extractor = SegFormerFeatureExtractor(image_scale=(1024, 2048), do_random_crop=False)
        # create random PyTorch tensor
        image = torch.randn((3, 1024, 2048))

        # Verify shape
        encoded_images = feature_extractor(image, return_tensors="pt").pixel_values
        expected_shape = (1, 3, 1024, 2048)
        self.assertEqual(encoded_images.shape, expected_shape)

    @require_torch
    def test_random_crop(self):
        # Create random PyTorch tensor
        h, w = 256, 304
        image = torch.randn((3, h, w))

        # Initialize feature_extractor
        feature_extractor = SegFormerFeatureExtractor(crop_size= (w - 20, h - 20))

        # Verify shape
        encoded_images = feature_extractor(image, return_tensors="pt").pixel_values
        self.assertEqual(encoded_images.shape[-2:], (h - 20, w - 20))

        # TODO: verify corresponding segmentation mask

    @require_torch
    def test_pad(self):
        # TODO
        pass
