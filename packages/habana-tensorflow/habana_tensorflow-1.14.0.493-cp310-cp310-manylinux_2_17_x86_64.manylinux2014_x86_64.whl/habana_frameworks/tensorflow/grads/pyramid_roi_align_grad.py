###############################################################################
# Copyright (C) 2021 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################
from tensorflow.python.framework import ops


def _register_grad(habana_ops):
    @ops.RegisterGradient("PyramidRoiAlign")
    def _PyramidRoiAlignGrad(op, grad):
        # get op tensor indices
        num_pyramid_levels = len(op.inputs) - 3
        num_boxes_tensor_index = num_pyramid_levels
        box_coords_tensor_index = num_pyramid_levels + 1
        box_to_level_map_tensor_index = num_pyramid_levels + 2
        # get image_pyramid shapes
        image_pyramid_shapes = []
        image_pyramid = []
        for pyramid_level in range(num_pyramid_levels):
            image = op.inputs[pyramid_level]
            if image.get_shape()[1:3].is_fully_defined():
                image_shape = image.get_shape()[1:3]
            else:
                raise ValueError(
                    '_pyramid_roi_align_grad: supports only static shapes with image_pyramid')
            image_pyramid_shapes.append(image_shape)
            image_pyramid.append(image)
        # gradient computation
        image_pyramid_grads = habana_ops.pyramid_roi_align_grad_images(image_pyramid, grad, op.inputs[num_boxes_tensor_index],
                                                                       op.inputs[box_coords_tensor_index], op.inputs[
                                                                           box_to_level_map_tensor_index],
                                                                       image_pyramid_shapes=image_pyramid_shapes,
                                                                       sampling_ratio=op.get_attr(
            'sampling_ratio'),
            use_abs_coords=op.get_attr(
            'use_abs_coords'),
            scale_to_level=op.get_attr(
            'scale_to_level'),
            border_replicate=op.get_attr('border_replicate'))
        return image_pyramid_grads + [None, None, None]