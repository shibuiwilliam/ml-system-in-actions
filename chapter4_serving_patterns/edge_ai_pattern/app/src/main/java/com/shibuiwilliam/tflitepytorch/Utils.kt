package com.shibuiwilliam.tflitepytorch

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Rect
import android.graphics.YuvImage
import android.util.Log
import androidx.camera.core.ImageProxy
import java.io.*
import java.util.*
import kotlin.Comparator

object Utils{
    private val TAG: String = Utils::class.java.simpleName

    fun loadLabelList(context: Context, labelPath: String = Constants.LABEL_PATH): List<String> {
        Log.v(TAG, "Loading ${labelPath}")
        val labelList: MutableList<String> = mutableListOf()
        try {
            BufferedReader(InputStreamReader(context.assets.open(labelPath))).use { reader ->
                var line = reader.readLine()
                while (line != null) {
                    labelList.add(line)
                    line = reader.readLine()
                }
            }
        }
        catch (e: IOException) {
            Log.e(TAG, "Failed to read label list.", e)
        }

        return labelList
    }

    fun assetFilePath(context: Context, assetName: String): String? {
        val file = File(context.filesDir, assetName)
        if (file.exists() && file.length() > 0) {
            return file.absolutePath
        }
        try {
            context.assets.open(assetName).use { `is` ->
                FileOutputStream(file).use { os ->
                    val buffer = ByteArray(4 * 1024)
                    var read: Int
                    while (`is`.read(buffer).also { read = it } != -1) {
                        os.write(buffer, 0, read)
                    }
                    os.flush()
                }
                return file.absolutePath
            }
        } catch (e: IOException) {
            Log.e(TAG, "Error process asset $assetName to file path")
        }
        return null
    }

    fun imageToBitmap(image: ImageProxy): Bitmap {
        val yBuffer = image.planes[0].buffer
        val uBuffer = image.planes[1].buffer
        val vBuffer = image.planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)

        yBuffer.get(nv21, 0, ySize)
        vBuffer.get(nv21, ySize, vSize)
        uBuffer.get(nv21, ySize + vSize, uSize)

        val yuvImage = YuvImage(nv21, Constants.IMAGE_FORMAT_NV21, image.width, image.height, null)
        val out = ByteArrayOutputStream()
        yuvImage.compressToJpeg(Rect(0, 0, yuvImage.width, yuvImage.height), 100, out)
        val imageBytes = out.toByteArray()
        return BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
    }

    fun prioritizeByProbability(labeledProbability: Map<String, Float>): MutableMap<String, Float> {
        val priorityMap: MutableMap<String, Float> = mutableMapOf()
        val priorityQueue = PriorityQueue(
            Constants.TOPK,
            Comparator<String> {a,b ->
                val aProb = labeledProbability.getOrDefault(a, 0f)
                val bProb = labeledProbability.getOrDefault(b, 0f)
                when {
                    aProb > bProb -> 1
                    aProb < bProb -> -1
                    else -> 0
                }
            }
        )
        for (k in labeledProbability.keys){
            priorityQueue.add(k)
            if (priorityQueue.size > Constants.TOPK) priorityQueue.remove()
        }
        for (i in 0 until Constants.TOPK){
            val p = priorityQueue.poll()
            priorityMap[p] = labeledProbability.getOrDefault(p, 0f)
        }
        return priorityMap
    }

}