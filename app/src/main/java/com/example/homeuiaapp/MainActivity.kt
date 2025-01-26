package com.example.homeuiaapp

import android.app.Activity
import android.os.Bundle
import android.view.View
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.WindowInsets
import androidx.core.view.WindowInsetsCompat
import androidx.privacysandbox.tools.core.model.Type

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        setContentView(R.layout.activity_main)


        val windowInsetsController =
            WindowCompat.getInsetsController(window, window.decorView)

        // Hide the system bars.
        windowInsetsController.hide(WindowInsetsCompat.Type.systemBars())


        val openWebsiteButton: Button = findViewById(R.id.openWebsiteButton)
        val webView: WebView = findViewById(R.id.webView)
        val urlInput: EditText = findViewById(R.id.urlInput)


        // Set up WebView
        webView.settings.apply {
            javaScriptEnabled = true
            cacheMode = WebSettings.LOAD_NO_CACHE
        }
        webView.setInitialScale(100)
        webView.webViewClient = WebViewClient()
        val websiteUrl = urlInput.text.toString()
        webView.loadUrl(websiteUrl)

        webView.visibility = View.VISIBLE
        openWebsiteButton.visibility = View.GONE
        urlInput.visibility = View.GONE


    }

}