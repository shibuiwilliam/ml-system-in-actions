package com.shibuiwilliam.tflitepytorch

import android.app.Activity
import android.app.Application
import android.content.Context


class App: Application(){
    private val TAG: String = App::class.java.simpleName

    internal lateinit var labels: List<String>

    override fun onCreate() {
        super.onCreate()
    }

    internal fun initialize(context: Context){
        labels = Utils.loadLabelList(context, Constants.LABEL_PATH)
    }

    internal fun close() {
    }
}