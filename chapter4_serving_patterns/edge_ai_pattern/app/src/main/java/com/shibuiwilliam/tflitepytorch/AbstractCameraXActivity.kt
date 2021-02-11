package com.shibuiwilliam.tflitepytorch

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Matrix
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.util.Log
import android.util.Rational
import android.util.Size
import android.view.Surface
import android.view.TextureView
import android.view.ViewGroup
import android.widget.TextView
import androidx.annotation.Nullable
import androidx.annotation.UiThread
import androidx.annotation.WorkerThread
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

abstract class AbstractCameraXActivity : AppCompatActivity(){
    private val TAG: String = AbstractCameraXActivity::class.java.simpleName

    protected var app: App? = null

    private val REQUEST_CODE_PERMISSIONS = 101
    private val REQUIRED_PERMISSIONS = arrayOf<String>(
        Manifest.permission.CAMERA
    )
    protected var mBackgroundThread: HandlerThread? = null
    protected var mBackgroundHandler: Handler? = null

    protected lateinit var textureView: TextureView
    internal lateinit var textView: TextView

    private var mLastAnalysisResultTime: Long = System.currentTimeMillis()

    protected abstract fun getContentView(): Int
    protected abstract fun getCameraTextureView(): TextureView
    protected abstract fun getInferenceTextView(): TextView

    @WorkerThread
    @Nullable
    protected abstract fun analyzeImage(image: ImageProxy, rotationDegrees: Int): String?

    @UiThread
    protected abstract fun showResult(result: String)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(getContentView())

        if (app==null) app = application as App

        textureView = getCameraTextureView()
        textView = getInferenceTextView()

        if (allPermissionsGranted()) {
            startBackgroundThread()
            textureView.post { setupCameraX() }
            textureView.addOnLayoutChangeListener { _, _, _, _, _, _, _, _, _ ->
                updateTransform()
            }
        } else {
            ActivityCompat.requestPermissions(
                this,
                REQUIRED_PERMISSIONS,
                REQUEST_CODE_PERMISSIONS
            )
        }
    }

    private fun setupCameraX() {
        CameraX.unbindAll()

        val screenSize = Size(textureView.width, textureView.height)
        val screenAspectRatio = Rational(1, 1)

        val previewConfig = PreviewConfig
            .Builder()
            .apply {
                setLensFacing(CameraX.LensFacing.BACK)
                setTargetResolution(screenSize)
                setTargetAspectRatio(screenAspectRatio)
                setTargetRotation(windowManager.defaultDisplay.rotation)
            }
            .build()
        val preview = Preview(previewConfig)

        preview.setOnPreviewOutputUpdateListener {
            val parent = textureView.parent as ViewGroup
            parent.removeView(textureView)
            textureView.surfaceTexture = it.surfaceTexture
            parent.addView(textureView, 0)
        }

        val imageAnalysisConfig = ImageAnalysisConfig
            .Builder()
            .apply {
                setCallbackHandler(mBackgroundHandler!!)
                setImageReaderMode(ImageAnalysis.ImageReaderMode.ACQUIRE_LATEST_IMAGE)
            }
            .build()

        val imageAnalysis = ImageAnalysis(imageAnalysisConfig)
        imageAnalysis.analyzer =
            ImageAnalysis.Analyzer { image: ImageProxy?, rotationDegrees: Int ->
                if (System.currentTimeMillis() - mLastAnalysisResultTime < 500) return@Analyzer
                if (image == null) return@Analyzer
                val result = analyzeImage(image, rotationDegrees)

                if (result != null){
                    runOnUiThread(Runnable { showResult(result) })
                }
                mLastAnalysisResultTime = System.currentTimeMillis()
            }

        CameraX.bindToLifecycle(this, preview, imageAnalysis)
    }

    private fun updateTransform() {
        val matrix = Matrix()
        val centerX = textureView.width / 2f
        val centerY = textureView.height / 2f

        val rotationDegrees = when (textureView.display.rotation) {
            Surface.ROTATION_0 -> 0
            Surface.ROTATION_90 -> 90
            Surface.ROTATION_180 -> 180
            Surface.ROTATION_270 -> 270
            else -> return
        }
        matrix.postRotate(-rotationDegrees.toFloat(), centerX, centerY)
        textureView.setTransform(matrix)
    }

    protected fun startBackgroundThread() {
        mBackgroundThread = HandlerThread("BackgroundThread")
        mBackgroundThread!!.start()
        mBackgroundHandler = Handler(mBackgroundThread!!.looper)
    }

    protected fun stopBackgroundThread() {
        if (mBackgroundHandler != null) {
            mBackgroundThread!!.quitSafely()
            mBackgroundThread!!.join()
        }
        try {
            mBackgroundThread = null
            mBackgroundHandler = null
        } catch (e: InterruptedException) {
            Log.e(TAG, "Error on stopping background thread", e)
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (!allPermissionsGranted()) {
                finish()
            }
        }
    }

    protected fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        for (permission in REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission)
                != PackageManager.PERMISSION_GRANTED
            ) {
                return false
            }
        }
        Log.i(TAG, "Permitted to use camera and internet")
        return true
    }

    override fun onStop() {
        stopBackgroundThread()
        super.onStop()
    }

    override fun onDestroy() {
        stopBackgroundThread()
        super.onDestroy()
    }
}