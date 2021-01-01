package com.shibuiwilliam.tflitepytorch

import android.graphics.ImageFormat

object Constants{
    const val LABEL_PATH = "imagenet_labels.txt"
    const val TFLITE_MOBILENET_V2_PATH = "mobilenet_v2_1.0_224.tflite"
    const val PYTORCH_MOBILENET_QUANTIZED_PATH = "mobilenet_quantized_scripted_925.pt"
    const val PYTORCH_RESNET18_PATH = "resnet18.pt"

    const val INPUT_IMAGE_SIZE = 224
    const val IMAGE_FORMAT_NV21 = ImageFormat.NV21

    const val IMAGE_MEAN = 127.5f
    const val IMAGE_STD = 127.5f
    const val PROBABILITY_MEAN = 0.0f
    const val PROBABILITY_STD = 1.0f

    const val TOPK = 3

    const val NUM_THREAD = 4

    enum class Device{
        CPU,
        NNAPI,
        GPU
    }
}