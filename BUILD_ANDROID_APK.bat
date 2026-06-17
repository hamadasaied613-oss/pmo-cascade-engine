@echo off
setlocal enabledelayedexpansion
title PMO CASCADE — Android APK Builder

echo =============================================
echo  PMO CASCADE Sovereign Engine
echo  Android APK Builder
echo =============================================
echo.

set APP_NAME=PMO_Cascade
set PACKAGE=com.pmo.cascade.sovereign
set COMPILE_SDK=34
set MIN_SDK=24
set OUTPUT_DIR=%~dp0build_output

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
set PROJECT=%TEMP%\pmo_cascade_android_%RANDOM%
if exist "%PROJECT%" rmdir /s /q "%PROJECT%"

echo [1/6] Creating project structure...
mkdir "%PROJECT%\app\src\main\java\com\pmo\cascade" 2>nul
mkdir "%PROJECT%\app\src\main\res\layout" 2>nul
mkdir "%PROJECT%\app\src\main\res\values" 2>nul
mkdir "%PROJECT%\app\src\main\res\drawable" 2>nul
mkdir "%PROJECT%\app\src\main\res\xml" 2>nul
mkdir "%PROJECT%\app\src\main\assets" 2>nul
mkdir "%PROJECT%\gradle\wrapper" 2>nul

echo [2/6] Writing AndroidManifest.xml...
> "%PROJECT%\app\src\main\AndroidManifest.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<manifest xmlns:android="http://schemas.android.com/apk/res/android"
echo     package="%PACKAGE%"^>
echo     ^<uses-permission android:name="android.permission.INTERNET" /^>
echo     ^<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" /^>
echo     ^<application
echo         android:allowBackup="true"
echo         android:label="%APP_NAME%"
echo         android:icon="@drawable/ic_launcher"
echo         android:usesCleartextTraffic="true"
echo         android:theme="@style/AppTheme"^>
echo         ^<activity android:name=".MainActivity"
echo             android:exported="true"
echo             android:configChanges="orientation|screenSize|keyboardHidden"
echo             android:screenOrientation="unspecified"^>
echo             ^<intent-filter^>
echo                 ^<action android:name="android.intent.action.MAIN" /^>
echo                 ^<category android:name="android.intent.category.LAUNCHER" /^>
echo             ^</intent-filter^>
echo         ^</activity^>
echo     ^</application^>
echo ^</manifest^>
)

echo [3/6] Writing MainActivity.java...
> "%PROJECT%\app\src\main\java\com\pmo\cascade\MainActivity.java" (
echo package com.pmo.cascade;
echo.
echo import android.app.Activity;
echo import android.app.AlertDialog;
echo import android.content.Context;
echo import android.content.DialogInterface;
echo import android.graphics.Bitmap;
echo import android.net.ConnectivityManager;
echo import android.net.NetworkInfo;
echo import android.os.Bundle;
echo import android.view.KeyEvent;
echo import android.view.View;
echo import android.view.Window;
echo import android.view.WindowManager;
echo import android.webkit.ConsoleMessage;
echo import android.webkit.JsResult;
echo import android.webkit.SslErrorHandler;
echo import android.webkit.WebChromeClient;
echo import android.webkit.WebSettings;
echo import android.webkit.WebView;
echo import android.webkit.WebViewClient;
echo import android.widget.ProgressBar;
echo.
echo public class MainActivity extends Activity {
echo     private WebView webView;
echo     private ProgressBar progressBar;
echo     private static final String SERVER_URL = "http://10.0.2.2:9000";
echo.
echo     @Override
echo     protected void onCreate(Bundle savedInstanceState) {
echo         super.onCreate(savedInstanceState);
echo         requestWindowFeature(Window.FEATURE_NO_TITLE);
echo         getWindow().setFlags(
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN,
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN
echo         );
echo         setContentView(getLayoutInflater().inflate(R.layout.activity_main, null));
echo.
echo         webView = findViewById(R.id.webview);
echo         progressBar = findViewById(R.id.progressbar);
echo.
echo         WebSettings settings = webView.getSettings();
echo         settings.setJavaScriptEnabled(true);
echo         settings.setDomStorageEnabled(true);
echo         settings.setAllowFileAccess(true);
echo         settings.setAllowContentAccess(true);
echo         settings.setLoadWithOverviewMode(true);
echo         settings.setUseWideViewPort(true);
echo         settings.setCacheMode(WebSettings.LOAD_DEFAULT);
echo         settings.setMediaPlaybackRequiresUserGesture(false);
echo.
echo         webView.setWebViewClient(new WebViewClient() {
echo             @Override
echo             public void onPageStarted(WebView view, String url, Bitmap favicon) {
echo                 progressBar.setVisibility(View.VISIBLE);
echo             }
echo             @Override
echo             public void onPageFinished(WebView view, String url) {
echo                 progressBar.setVisibility(View.GONE);
echo                 view.evaluateJavascript(
echo                     "document.body.style.zoom = '1.0';", null
echo                 );
echo             }
echo             @Override
echo             public void onReceivedSslError(WebView view, SslErrorHandler handler, android.net.http.SslError error) {
echo                 handler.proceed();
echo             }
echo         });
echo.
echo         webView.setWebChromeClient(new WebChromeClient() {
echo             @Override
echo             public boolean onConsoleMessage(ConsoleMessage msg) {
echo                 return true;
echo             }
echo             @Override
echo             public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
echo                 new AlertDialog.Builder(MainActivity.this)
echo                     .setMessage(message)
echo                     .setPositiveButton("OK", new DialogInterface.OnClickListener() {
echo                         public void onClick(DialogInterface dialog, int which) { result.confirm(); }
echo                     })
echo                     .show();
echo                 return true;
echo             }
echo         });
echo.
echo         webView.loadUrl(SERVER_URL);
echo     }
echo.
echo     @Override
echo     public boolean onKeyDown(int keyCode, KeyEvent event) {
echo         if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
echo             webView.goBack();
echo             return true;
echo         }
echo         return super.onKeyDown(keyCode, event);
echo     }
echo }
)

echo [4/6] Writing layout and resources...
> "%PROJECT%\app\src\main\res\layout\activity_main.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
echo     android:layout_width="match_parent"
echo     android:layout_height="match_parent"
echo     android:background="#0a0a0f"^>
echo     ^<ProgressBar
echo         android:id="@+id/progressbar"
echo         style="?android:attr/progressBarStyleHorizontal"
echo         android:layout_width="match_parent"
echo         android:layout_height="3dp"
echo         android:layout_alignParentTop="true"
echo         android:indeterminate="false"
echo         android:max="100"
echo         android:visibility="gone" /^>
echo     ^<WebView
echo         android:id="@+id/webview"
echo         android:layout_width="match_parent"
echo         android:layout_height="match_parent"
echo         android:layout_below="@id/progressbar" /^>
echo ^</RelativeLayout^>
)

> "%PROJECT%\app\src\main\res\values\styles.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<resources^>
echo     ^<style name="AppTheme" parent="android:Theme.Material.NoActionBar"^>
echo         ^<item name="android:windowFullscreen"^>true^</item^>
echo         ^<item name="android:colorPrimary"^>#00B4D8^</item^>
echo         ^<item name="android:colorPrimaryDark"^>#0a0a0f^</item^>
echo         ^<item name="android:colorAccent"^>#00B4D8^</item^>
echo         ^<item name="android:windowBackground"^>#0a0a0f^</item^>
echo     ^</style^>
echo ^</resources^>
)

> "%PROJECT%\app\src\main\res\values\strings.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<resources^>
echo     ^<string name="app_name"^>PMO Cascade^</string^>
echo ^</resources^>
)

echo [5/6] Writing Gradle configs...
> "%PROJECT%\build.gradle" (
echo buildscript {
echo     repositories { google^(^); mavenCentral^(^) }
echo     dependencies { classpath 'com.android.tools.build:gradle:8.1.0' }
echo }
echo allprojects { repositories { google^(^); mavenCentral^(^) } }
)

> "%PROJECT%\app\build.gradle" (
echo plugins { id 'com.android.application' }
echo android {
echo     namespace '%PACKAGE%'
echo     compileSdk %COMPILE_SDK%
echo     defaultConfig {
echo         applicationId "%PACKAGE%"
echo         minSdk %MIN_SDK%
echo         targetSdk %COMPILE_SDK%
echo         versionCode 1
echo         versionName "1.0"
echo     }
echo     buildTypes {
echo         release {
echo             minifyEnabled false
echo             proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
echo         }
echo     }
echo }
echo dependencies { implementation 'androidx.appcompat:appcompat:1.6.1' }
)

> "%PROJECT%\settings.gradle" (
echo rootProject.name = "%APP_NAME%"
echo include ':app'
)

> "%PROJECT%\gradle\wrapper\gradle-wrapper.properties" (
echo distributionBase=GRADLE_USER_HOME
echo distributionPath=wrapper/dists
echo distributionUrl=https\://services.gradle.org/distributions/gradle-8.2-bin.zip
echo zipStoreBase=GRADLE_USER_HOME
echo zipStorePath=wrapper/dists
)

echo [6/6] Building APK...
echo.
echo  NOTE: This requires Android SDK installed.
echo  If ANDROID_HOME is not set, the APK will be
echo  generated as a ready-to-build project.
echo.

if not "%ANDROID_HOME%"=="" (
    cd /d "%PROJECT%"
    call gradlew.bat assembleDebug 2>&1
    for /r "%PROJECT%" %%f in (*.apk) do (
        copy "%%f" "%OUTPUT_DIR%\%APP_NAME%_v1.0.apk" /y
        echo --------------------------------------------
        echo  BUILD SUCCESS
        echo  APK: %OUTPUT_DIR%\%APP_NAME%_v1.0.apk
        echo --------------------------------------------
    )
) else (
    echo  Copying project to output...
    xcopy /E /I /Y "%PROJECT%" "%OUTPUT_DIR%\%APP_NAME%_Android_Project"
    echo --------------------------------------------
    echo  PROJECT READY
    echo  Location: %OUTPUT_DIR%\%APP_NAME%_Android_Project
    echo.
    echo  To build APK:
    echo  1. Install Android Studio
    echo  2. Open the project folder
    echo  3. Build ^> Build APK
    echo --------------------------------------------
)

cd /d "%OUTPUT_DIR%"
dir *.apk 2>nul
dir /s /b "%APP_NAME%_Android_Project" 2>nul
pause
