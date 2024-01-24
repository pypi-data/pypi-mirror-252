###############################################################################
# Copyright (C) 2022 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################
import os

from habana_frameworks.tensorflow.media.habana_dataset import HabanaDataset
from habana_frameworks.tensorflow.multinode_helpers import comm_size, comm_rank
import tensorflow as tf
import logging
import json
log = logging.getLogger(__file__)

force_fallback = os.environ.get("FORCE_HABANA_IMAGENET_LOADER_FALLBACK") is not None
media_import_error_msg = ""
try:
    from habana_frameworks.medialoaders.tensorflow.media_resnet_pipe import ResnetPipe
    from habana_frameworks.mediapipe.media_types import randomCropType
except ImportError as e:
    media_import_error_msg = e.msg

def _get_pytorch_dataset_dir(is_training, data_dir):
    if is_training:
        return os.path.join(data_dir, 'train')
    else:
        return os.path.join(data_dir, 'val')


def _get_tfrecord_dataset_pattern(is_training, data_dir):
    if is_training:
        return os.path.join(data_dir, 'train', 'train-*')
    else:
        return os.path.join(data_dir, 'validation', 'validation-*')


def log_fallback(device_type, jpeg_data_dir):
    reasons = []
    log_level = logging.WARNING
    if not device_type.startswith("GAUDI2"):
        log_level = logging.DEBUG
        reasons.append("Incorrect device type")
    if force_fallback:
        reasons.append("Fallback was forced")
    if jpeg_data_dir is None:
        reasons.append("jpeg_data_dir not provided")
    if media_import_error_msg:
        reasons.append(media_import_error_msg)
    log.log(log_level, "Resnet dataset was fallbacked. Reasons: {%s}", ", ".join(reasons))


def habana_imagenet_dataset(fallback,
                            is_training,
                            tf_data_dir,
                            jpeg_data_dir,
                            batch_size,
                            num_channels,
                            img_size,
                            dtype,
                            use_distributed_eval,
                            use_pytorch_style_crop=False,
                            manifest_path=None,
                            **fallback_kwargs):
    """Function responsible for preparing TF dataset with media loader
        Args:
            fallback: Function to return native TF dataset in case we cannot create one with media loader.
            is_training: A boolean denoting whether the input is for training.
            tf_data_dir: The directory containing the input data in tf_record format - used for fallback.
            jpeg_data_dir: The directory containing the input data in jpeg format - used for media loader.
            batch_size: The number of samples per batch.
            num_channels: Number of channels.
            img_size: Image size.
            dtype: Data type to use for images/features.
            use_distributed_eval: Whether or not to use distributed evaluation.
            use_pytorch_style_crop: Whether or not to use pytorch style crop function (using tf algorithm by default)
            fallback_kwargs: other kwargs to pass to fallback function.

        Returns:
          A dataset that can be used for iteration.
        """

    from habana_frameworks.tensorflow import habana_device
    device_type = habana_device.get_type()
    if device_type.startswith("GAUDI2") and not force_fallback and not media_import_error_msg:
        if dtype == tf.float32:
            m_dtype = 'float32'
        elif dtype == tf.bfloat16:
            m_dtype = 'bfloat16'
        else:
            m_dtype = 'uint8'

        if comm_size() > 1 and (is_training or use_distributed_eval):
            num_slices = comm_size()
            slice_index = comm_rank()
        else:
            num_slices = 1
            slice_index = 0

        if not is_training:
            crop_type = randomCropType.CENTER_CROP
        elif use_pytorch_style_crop:
            crop_type = randomCropType.RANDOMIZED_AREA_AND_ASPECT_RATIO_CROP
        else:
            crop_type = randomCropType.RANDOMIZED_ASPECT_RATIO_CROP

        if jpeg_data_dir is not None:
            dataset_manifest = {}
            if manifest_path is not None and os.path.isfile(manifest_path):
                with open(manifest_path, "r") as f:
                    dataset_manifest = json.load(f)

            pipe = ResnetPipe("hpu", 3, batch_size, num_channels,
                              img_size, img_size, is_training,
                              _get_pytorch_dataset_dir(is_training, jpeg_data_dir),
                              m_dtype, num_slices, slice_index, crop_type, False,
                              dataset_manifest=dataset_manifest)
        elif tf_data_dir is not None:
            pipe = ResnetPipe("hpu", 3, batch_size, num_channels,
                              img_size, img_size, is_training,
                              _get_tfrecord_dataset_pattern(is_training, tf_data_dir),
                              m_dtype, num_slices, slice_index, crop_type, True,
                              dataset_manifest={})
        else:
            raise RuntimeError("Neither --data_dir nor --jpeg_data_dir provided")

        pipe.set_repeat_count(-1)

        dataset = HabanaDataset(output_shapes=[(batch_size,
                                                img_size,
                                                img_size,
                                                num_channels),
                                               (batch_size,)],
                                output_types=[dtype, tf.float32], pipeline=pipe)
        dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
        return dataset
    else:
        log_fallback(device_type, jpeg_data_dir)
        if tf_data_dir is not None:
            return fallback(is_training=is_training,
                            data_dir=tf_data_dir,
                            batch_size=batch_size,
                            dtype=dtype,
                            use_distributed_eval=use_distributed_eval,
                            **fallback_kwargs)
        else:
            raise RuntimeError("Tried to run fallback dataset without --data_dir provided")
