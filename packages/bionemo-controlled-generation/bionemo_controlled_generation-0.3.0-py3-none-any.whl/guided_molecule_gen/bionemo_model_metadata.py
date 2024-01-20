# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
# Data lookup for known supported models.

bionemo_model_info = {
    "molmim": {
        "num_latent_dimensions": 512,
        "default_sampling_radius": 1.0,
        "decode_endpoint_name": "molmim_decode_sync",
        "encode_endpoint_name": "molmim_embeddings_sync",
    },
    "moflow": {
        "num_latent_dimensions": 6800,
        "default_sampling_radius": 0.25,
        "decode_endpoint_name": "moflow_decode_sync",
        "encode_endpoint_name": "moflow_embeddings_sync",
    },
}
