package com.shibuiwilliam.tflitepytorch

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    private val TAG: String = MainActivity::class.java.simpleName
    private val REQUEST_CODE_PERMISSIONS = 101
    private val REQUIRED_PERMISSIONS = arrayOf<String>(
        Manifest.permission.CAMERA
    )

    private lateinit var tfliteButton: Button
    private lateinit var pytorchButton: Button

    private var app: App? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (app==null){
            app = application as App
            app!!.initialize(this)
        }

        tfliteButton = findViewById(R.id.TFLite)
        tfliteButton.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View?) {
                startActivity(Intent(application, TFLiteActivity::class.java))
            }
        })

        pytorchButton = findViewById(R.id.PyTorch)
        pytorchButton.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View?) {
                startActivity(Intent(application, PyTorchActivity::class.java))
            }
        })

    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray) {
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (!allPermissionsGranted()) {
                finish()
            }
        }
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        for (permission in REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission)
                != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        Log.i(TAG, "Permitted to use camera and internet")
        return true
    }

    override fun onDestroy() {
        super.onDestroy()
        if (app != null) app!!.close()
    }
}
