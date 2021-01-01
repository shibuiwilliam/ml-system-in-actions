package com.shibuiwilliam.tflitepytorch

import android.os.Bundle
import android.util.Log
import android.view.TextureView
import android.widget.TextView
import androidx.annotation.Nullable
import androidx.annotation.UiThread
import androidx.annotation.WorkerThread
import androidx.camera.core.ImageProxy
import org.pytorch.IValue
import org.pytorch.Module
import org.pytorch.Tensor
import org.pytorch.torchvision.TensorImageUtils
import java.nio.FloatBuffer

class PyTorchActivity : AbstractCameraXActivity() {
    private val TAG: String = PyTorchActivity::class.java.simpleName

    private lateinit var pytorchModule: Module

    private lateinit var mInputTensorBuffer: FloatBuffer
    private lateinit var mInputTensor: Tensor

    override fun getContentView(): Int = R.layout.activity_py_torch
    override fun getCameraTextureView(): TextureView = findViewById(R.id.cameraPreviewTextureView)
    override fun getInferenceTextView(): TextView = findViewById(R.id.inferenceText)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        initializePyTorch()
        mInputTensorBuffer =
            Tensor.allocateFloatBuffer(3 * Constants.INPUT_IMAGE_SIZE * Constants.INPUT_IMAGE_SIZE)

        mInputTensor = Tensor.fromBlob(
            mInputTensorBuffer,
            longArrayOf(
                1,
                3,
                Constants.INPUT_IMAGE_SIZE.toLong(),
                Constants.INPUT_IMAGE_SIZE.toLong()
            )
        )
    }

    private fun initializePyTorch() {
        pytorchModule = Module.load(Utils.assetFilePath(this, Constants.PYTORCH_RESNET18_PATH))
    }

    @WorkerThread
    @Nullable
    override fun analyzeImage(image: ImageProxy, rotationDegrees: Int): String? {
        try {
            TensorImageUtils.imageYUV420CenterCropToFloatBuffer(
                image.image,
                rotationDegrees,
                Constants.INPUT_IMAGE_SIZE,
                Constants.INPUT_IMAGE_SIZE,
                TensorImageUtils.TORCHVISION_NORM_MEAN_RGB,
                TensorImageUtils.TORCHVISION_NORM_STD_RGB,
                mInputTensorBuffer,
                0
            )
            val labeledProbability = classifyImage()
            Log.i(TAG, "top${Constants.TOPK} prediction: ${labeledProbability}")
            return labeledProbability.map { it ->
                val p = "%,.2f".format(it.value)
                "${it.key}: ${p} \n"
            }.joinToString()
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }

    @UiThread
    override fun showResult(result: String) {
        textView.text = result
    }

    private fun classifyImage(): Map<String, Float> {
        val outputModule = pytorchModule.forward(IValue.from(mInputTensor)).toTensor()
        val scores = outputModule.dataAsFloatArray
        val labeledProbability = mapScoreToLabelMap(scores)
        Log.i(TAG, "full prediction: ${labeledProbability}")
        return Utils.prioritizeByProbability(labeledProbability)
    }

    private fun mapScoreToLabelMap(score: FloatArray): Map<String, Float> {
        val labeledProbability: MutableMap<String, Float> = mutableMapOf()
        for (i in 0 until app!!.labels.size - 1) {
            labeledProbability[app!!.labels[i + 1]] = score[i]
        }
        return labeledProbability
    }

    override fun onStop() {
        super.onStop()
    }

    override fun onDestroy() {
        super.onDestroy()
    }

}
