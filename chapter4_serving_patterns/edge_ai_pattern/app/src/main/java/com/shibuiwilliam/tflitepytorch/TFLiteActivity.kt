package com.shibuiwilliam.tflitepytorch

import android.graphics.Bitmap
import android.graphics.Matrix
import android.os.Bundle
import android.util.Log
import android.view.TextureView
import android.widget.TextView
import androidx.annotation.Nullable
import androidx.annotation.UiThread
import androidx.annotation.WorkerThread
import androidx.camera.core.ImageProxy
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.gpu.GpuDelegate
import org.tensorflow.lite.nnapi.NnApiDelegate
import org.tensorflow.lite.support.common.FileUtil
import org.tensorflow.lite.support.common.TensorOperator
import org.tensorflow.lite.support.common.TensorProcessor
import org.tensorflow.lite.support.common.ops.NormalizeOp
import org.tensorflow.lite.support.image.ImageProcessor
import org.tensorflow.lite.support.image.TensorImage
import org.tensorflow.lite.support.image.ops.ResizeOp
import org.tensorflow.lite.support.image.ops.ResizeOp.ResizeMethod
import org.tensorflow.lite.support.image.ops.ResizeWithCropOrPadOp
import org.tensorflow.lite.support.label.TensorLabel
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer
import java.nio.MappedByteBuffer


class TFLiteActivity : AbstractCameraXActivity() {
    private val TAG: String = TFLiteActivity::class.java.simpleName

    private lateinit var tfliteModel: MappedByteBuffer
    private lateinit var tfliteInterpreter: Interpreter
    private val tfliteOptions = Interpreter.Options()
    private var gpuDelegate: GpuDelegate? = null
    private var nnApiDelegate: NnApiDelegate? = null

    private lateinit var inputImageBuffer: TensorImage
    private lateinit var outputProbabilityBuffer: TensorBuffer
    private lateinit var probabilityProcessor: TensorProcessor

    override fun getContentView(): Int = R.layout.activity_t_f_lite
    override fun getCameraTextureView(): TextureView = findViewById(R.id.cameraPreviewTextureView)
    override fun getInferenceTextView(): TextView = findViewById(R.id.inferenceText)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        initializeTFLite(Constants.Device.NNAPI, Constants.NUM_THREAD)

        inputImageBuffer = TensorImage(tfliteInterpreter.getInputTensor(0).dataType())
        outputProbabilityBuffer = TensorBuffer.createFixedSize(
            tfliteInterpreter.getOutputTensor(0).shape(),
            tfliteInterpreter.getInputTensor(0).dataType()
        )
        probabilityProcessor = TensorProcessor
            .Builder()
            .add(postprocessNormalizeOp())
            .build()
    }

    private fun initializeTFLite(device: Constants.Device, numThreads: Int) {
        when (device) {
            Constants.Device.NNAPI -> {
                nnApiDelegate = NnApiDelegate()
                tfliteOptions.addDelegate(nnApiDelegate)
            }
            Constants.Device.GPU -> {
                gpuDelegate = GpuDelegate()
                tfliteOptions.addDelegate(gpuDelegate)
            }
            Constants.Device.CPU -> {
            }
        }
        tfliteOptions.setNumThreads(numThreads)
        tfliteModel = FileUtil.loadMappedFile(this, Constants.TFLITE_MOBILENET_V2_PATH)
        tfliteInterpreter = Interpreter(tfliteModel, tfliteOptions)
    }

    @WorkerThread
    @Nullable
    override fun analyzeImage(image: ImageProxy, rotationDegrees: Int): String? {
        try {
            var bitmap = Utils.imageToBitmap(image)
            bitmap = rotateBitmap(bitmap, 90f)
            val labeledProbability = classifyImage(bitmap)
            Log.i(TAG, "top${Constants.TOPK} prediction: ${labeledProbability}")
            return labeledProbability.map{it ->
                val p = "%,.2f".format(it.value)
                "${it.key}: ${p} \n"
            }.joinToString()
        }
        catch (e: Exception){
            e.printStackTrace()
            return null
        }
    }

    @UiThread
    override fun showResult(result: String) {
        textView.text = result
    }

    private fun classifyImage(bitmap: Bitmap): Map<String, Float> {
        val inputImageBuffer = loadImage(bitmap)
        tfliteInterpreter.run(
            inputImageBuffer!!.buffer,
            outputProbabilityBuffer.buffer.rewind()
        )
        val labeledProbability: Map<String, Float> = TensorLabel(
            app!!.labels,
            probabilityProcessor.process(outputProbabilityBuffer)
        ).mapWithFloatValue
        Log.i(TAG, "full prediction: ${labeledProbability}")
        return Utils.prioritizeByProbability(labeledProbability)
    }

    private fun loadImage(bitmap: Bitmap): TensorImage? {
        inputImageBuffer.load(bitmap)

        val cropSize = Math.min(bitmap.width, bitmap.height)

        val imageProcessor = ImageProcessor
            .Builder()
            .add(ResizeWithCropOrPadOp(cropSize, cropSize))
            .add(
                ResizeOp(
                    Constants.INPUT_IMAGE_SIZE,
                    Constants.INPUT_IMAGE_SIZE,
                    ResizeMethod.NEAREST_NEIGHBOR
                )
            )
            .add(preprocessNormalizeOp())
            .build()
        return imageProcessor.process(inputImageBuffer)
    }

    private fun rotateBitmap(bitmap: Bitmap, degrees: Float): Bitmap {
        val matrix = Matrix()
        matrix.postRotate(degrees)
        return Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
    }

    private fun preprocessNormalizeOp(): TensorOperator? {
        return NormalizeOp(Constants.IMAGE_MEAN, Constants.IMAGE_STD)
    }

    protected fun postprocessNormalizeOp(): TensorOperator? {
        return NormalizeOp(Constants.PROBABILITY_MEAN, Constants.PROBABILITY_STD)
    }

    override fun onStop() {
        super.onStop()
        if (::tfliteInterpreter.isInitialized) {
            tfliteInterpreter.close()
        }
        if (gpuDelegate != null) {
            gpuDelegate!!.close()
            gpuDelegate = null
        }
        if (nnApiDelegate != null) {
            nnApiDelegate!!.close()
            nnApiDelegate = null
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (::tfliteInterpreter.isInitialized) {
            tfliteInterpreter.close()
        }
        if (gpuDelegate != null) {
            gpuDelegate!!.close()
            gpuDelegate = null
        }
        if (nnApiDelegate != null) {
            nnApiDelegate!!.close()
            nnApiDelegate = null
        }

    }
}
