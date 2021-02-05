# coding=utf-8
# Copyright Facebook AI Research and The HuggingFace Inc. team. All rights reserved.
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
""" DETR model configuration """

from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

DETR_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "facebook/detr-resnet-50": "https://huggingface.co/facebook/detr-resnet-50/resolve/main/config.json",
    # See all DETR models at https://huggingface.co/models?filter=detr
}


class DetrConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a :class:`~transformers.DetrModel`.
    It is used to instantiate a DETR model according to the specified arguments, defining the model
    architecture. Instantiating a configuration with the defaults will yield a similar configuration to that of
    the DETR `facebook/detr-resnet-50 <https://huggingface.co/facebook/detr-resnet-50>`__ architecture.

    Configuration objects inherit from  :class:`~transformers.PretrainedConfig` and can be used
    to control the model outputs. Read the documentation from  :class:`~transformers.PretrainedConfig`
    for more information.


    Args:
        num_queries (:obj:`int`, `optional`, defaults to 100):
            Number of object queries, i.e. detection slots. This is the maximal number of objects
            :class:`~transformers.DetrModel` can detect in a single image. For COCO, we recommend 100 queries.
        d_model (:obj:`int`, `optional`, defaults to 256):
            Dimensionality of the layers.
        encoder_layers (:obj:`int`, `optional`, defaults to 6):
            Number of encoder layers.
        decoder_layers (:obj:`int`, `optional`, defaults to 6):
            Number of decoder layers.
        encoder_attention_heads (:obj:`int`, `optional`, defaults to 8):
            Number of attention heads for each attention layer in the Transformer encoder.
        decoder_attention_heads (:obj:`int`, `optional`, defaults to 8):
            Number of attention heads for each attention layer in the Transformer decoder.
        decoder_ffn_dim (:obj:`int`, `optional`, defaults to 2048):
            Dimensionality of the "intermediate" (often named feed-forward) layer in decoder.
        encoder_ffn_dim (:obj:`int`, `optional`, defaults to 2048):
            Dimensionality of the "intermediate" (often named feed-forward) layer in decoder.
        activation_function (:obj:`str` or :obj:`function`, `optional`, defaults to :obj:`"relu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string,
            :obj:`"gelu"`, :obj:`"relu"`, :obj:`"silu"` and :obj:`"gelu_new"` are supported.
        dropout (:obj:`float`, `optional`, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for the attention probabilities.
        activation_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for activations inside the fully connected layer.
        classifier_dropout (:obj:`float`, `optional`, defaults to 0.0):
            The dropout ratio for classifier.
        max_position_embeddings (:obj:`int`, `optional`, defaults to 1024):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 512 or 1024 or 2048).
        init_std (:obj:`float`, `optional`, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        encoder_layerdrop: (:obj:`float`, `optional`, defaults to 0.0):
            The LayerDrop probability for the encoder. See the `LayerDrop paper <see
            https://arxiv.org/abs/1909.11556>`__ for more details.
        decoder_layerdrop: (:obj:`float`, `optional`, defaults to 0.0):
            The LayerDrop probability for the decoder. See the `LayerDrop paper <see
            https://arxiv.org/abs/1909.11556>`__ for more details.
        use_cache (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether or not the model should return the last key/values attentions (not used by all models).
        auxiliary_loss (:obj:`bool`, `optional`, defaults to :obj:`False`):
            Whether auxiliary decoding losses (loss at each decoder layer) are to be used.
        position_embedding_type (:obj:`str`, `optional`, defaults to :obj:`sine`):
            Type of position embeddings to be used on top of the image features. One of 'sine' or 'learned'.
        backbone (:obj:`bool`, `optional`, defaults to :obj:`resnet50`): 
            Name of convolutional backbone to use. Currently only resnet of the Torchvision package is supported. 
        train_backbone (:obj:`bool`, `optional`, defaults to :obj:`True`): 
            Whether to train (fine-tune) the backbone. 
        dilation (:obj:`bool`, `optional`, defaults to :obj:`False`): 
            Whether to replace stride with dilation in the last convolutional block (DC5).
        masks (:obj:`bool`, `optional`, defaults to :obj:`False`): 
            Whether to train the segmentation head.
        class_cost (:obj:`float`, `optional`, defaults to 1):
            Relative weight of the classification error in the Hungarian matching cost.
        bbox_cost (:obj:`float`, `optional`, defaults to 5):
            Relative weight of the L1 error of the bounding box coordinates in the Hungarian matching cost.
        giou_cost (:obj:`float`, `optional`, defaults to 2):
            Relative weight of the generalized IoU loss of the bounding box in the Hungarian matching cost.
        mask_loss_coefficient (:obj:`float`, `optional`, defaults to 1):
            Relative weight of the Focal loss in the panoptic segmentation loss.
        dice_loss_coefficient (:obj:`float`, `optional`, defaults to 1):
            Relative weight of the DICE/F-1 loss in the panoptic segmentation loss.
        bbox_loss_coefficient (:obj:`float`, `optional`, defaults to 5):
            Relative weight of the L1 bounding box loss in the object detection loss.
        giou_loss_coefficient (:obj:`float`, `optional`, defaults to 2):
            Relative weight of the generalized IoU loss in the object detection loss.
        eos_coefficient (:obj:`float`, `optional`, defaults to 0.1):
            Relative classification weight of the 'no-object' class in the object detection loss.

    Examples::

        >>> from transformers import DetrModel, DetrConfig

        >>> # Initializing a DETR facebook/detr-resnet-50 style configuration
        >>> configuration = DetrConfig()

        >>> # Initializing a model from the facebook/detr-resnet-50 style configuration
        >>> model = DetrModel(configuration)

        >>> # Accessing the model configuration
        >>> configuration = model.config
    """
    model_type = "detr"
    keys_to_ignore_at_inference = ["past_key_values"]
    def __init__(
        self,
        num_queries=100,
        max_position_embeddings=1024,
        encoder_layers=6,
        encoder_ffn_dim=2048,
        encoder_attention_heads=8,
        decoder_layers=6,
        decoder_ffn_dim=2048,
        decoder_attention_heads=8,
        encoder_layerdrop=0.0,
        decoder_layerdrop=0.0,
        use_cache=True,
        is_encoder_decoder=True,
        activation_function="relu",
        d_model=256,
        dropout=0.1,
        attention_dropout=0.0,
        activation_dropout=0.0,
        init_std=0.02,
        decoder_start_token_id=2,
        classifier_dropout=0.0,
        scale_embedding=False,
        gradient_checkpointing=False,
        pad_token_id=1,
        bos_token_id=0,
        eos_token_id=2,
        auxiliary_loss=False,
        position_embedding_type='sine',
        backbone='resnet50',
        train_backbone=True,
        dilation=False,
        masks=False,
        class_cost=1,
        bbox_cost=5,
        giou_cost=2,
        mask_loss_coefficient=1,
        dice_loss_coefficient=1,
        bbox_loss_coefficient=5,
        giou_loss_coefficient=2,
        eos_coefficient=0.1,
        **kwargs
    ):
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            is_encoder_decoder=is_encoder_decoder,
            decoder_start_token_id=decoder_start_token_id,
            **kwargs
        )

        self.num_queries = num_queries
        self.max_position_embeddings = max_position_embeddings
        self.d_model = d_model
        self.encoder_ffn_dim = encoder_ffn_dim
        self.encoder_layers = encoder_layers
        self.encoder_attention_heads = encoder_attention_heads
        self.decoder_ffn_dim = decoder_ffn_dim
        self.decoder_layers = decoder_layers
        self.decoder_attention_heads = decoder_attention_heads
        self.dropout = dropout
        self.attention_dropout = attention_dropout
        self.activation_dropout = activation_dropout
        self.activation_function = activation_function
        self.init_std = init_std
        self.encoder_layerdrop = encoder_layerdrop
        self.decoder_layerdrop = decoder_layerdrop
        self.classifier_dropout = classifier_dropout
        self.use_cache = use_cache
        self.num_hidden_layers = encoder_layers
        self.gradient_checkpointing = gradient_checkpointing
        self.scale_embedding = scale_embedding  # scale factor will be sqrt(d_model) if True
        self.auxiliary_loss = auxiliary_loss
        self.position_embedding_type = position_embedding_type
        self.backbone = backbone
        self.train_backbone = train_backbone
        self.dilation = dilation
        self.masks = masks
        # Hungarian matcher
        self.class_cost = class_cost
        self.bbox_cost = bbox_cost
        self.giou_cost = giou_cost
        # Loss coefficients
        self.mask_loss_coefficient = mask_loss_coefficient
        self.dice_loss_coefficient = dice_loss_coefficient
        self.bbox_loss_coefficient = bbox_loss_coefficient
        self.giou_loss_coefficient = giou_loss_coefficient
        self.eos_coefficient = eos_coefficient


        
    @property
    def num_attention_heads(self) -> int:
        return self.encoder_attention_heads

    @property
    def hidden_size(self) -> int:
        return self.d_model