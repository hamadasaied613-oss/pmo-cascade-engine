@echo off
setlocal enabledelayedexpansion
title PMO CASCADE — Android APK Builder v2.0

echo =============================================
echo  PMO CASCADE Sovereign Engine
echo  Android APK Builder v2.0
echo  Railway-Connected + Offline Ready
echo =============================================
echo.

set APP_NAME=PMO_Cascade
set PACKAGE=com.pmo.cascade.sovereign
set COMPILE_SDK=34
set MIN_SDK=24
set RAILWAY_URL=https://web-production-c8682.up.railway.app
set LOCAL_URL=http://10.0.2.2:9000
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
mkdir "%PROJECT%\gradle\wrapper" 2>nul

echo [2/6] Writing AndroidManifest.xml...
> "%PROJECT%\app\src\main\AndroidManifest.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<manifest xmlns:android="http://schemas.android.com/apk/res/android"
echo     package="%PACKAGE%"^>
echo     ^<uses-permission android:name="android.permission.INTERNET" /^>
echo     ^<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" /^>
echo     ^<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" /^>
echo     ^<application
echo         android:allowBackup="true"
echo         android:label="%APP_NAME%"
echo         android:icon="@drawable/ic_launcher"
echo         android:usesCleartextTraffic="true"
echo         android:theme="@style/AppTheme"^>
echo         ^<activity android:name=".SplashActivity"
echo             android:exported="true"
echo             android:theme="@style/SplashTheme"^>
echo             ^<intent-filter^>
echo                 ^<action android:name="android.intent.action.MAIN" /^>
echo                 ^<category android:name="android.intent.category.LAUNCHER" /^>
echo             ^</intent-filter^>
echo         ^</activity^>
echo         ^<activity android:name=".MainActivity"
echo             android:exported="false"
echo             android:configChanges="orientation|screenSize|keyboardHidden"
echo             android:screenOrientation="unspecified"^>
echo         ^</activity^>
echo     ^</application^>
echo ^</manifest^>
)
echo [3/6] Writing SplashActivity.java...
> "%PROJECT%\app\src\main\java\com\pmo\cascade\SplashActivity.java" (
echo package com.pmo.cascade;
echo.
echo import android.app.Activity;
echo import android.content.Intent;
echo import android.content.pm.ActivityInfo;
echo import android.os.Bundle;
echo import android.os.Handler;
echo import android.view.Window;
echo import android.view.WindowManager;
echo import android.widget.TextView;
echo import android.widget.LinearLayout;
echo import android.graphics.Color;
echo import android.view.Gravity;
echo.
echo public class SplashActivity extends Activity {
echo     @Override
echo     protected void onCreate(Bundle savedInstanceState) {
echo         super.onCreate(savedInstanceState);
echo         requestWindowFeature(Window.FEATURE_NO_TITLE);
echo         getWindow().setFlags(
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN,
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN
echo         );
echo         setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
echo.
echo         LinearLayout layout = new LinearLayout(this);
echo         layout.setLayoutParams(new LinearLayout.LayoutParams(
echo             LinearLayout.LayoutParams.MATCH_PARENT,
echo             LinearLayout.LayoutParams.MATCH_PARENT
echo         ));
echo         layout.setBackgroundColor(Color.parseColor("#0a0a0f"));
echo         layout.setGravity(Gravity.CENTER);
echo         layout.setOrientation(LinearLayout.VERTICAL);
echo.
echo         TextView title = new TextView(this);
echo         title.setText("PMO CASCADE");
echo         title.setTextSize(28);
echo         title.setTextColor(Color.parseColor("#00B4D8"));
echo         title.setGravity(Gravity.CENTER);
echo         layout.addView(title);
echo.
echo         TextView subtitle = new TextView(this);
echo         subtitle.setText("Sovereign Engine v2.0");
echo         subtitle.setTextSize(14);
echo         subtitle.setTextColor(Color.parseColor("#8899AA"));
echo         subtitle.setGravity(Gravity.CENTER);
echo         layout.addView(subtitle);
echo.
echo         setContentView(layout);
echo.
echo         new Handler().postDelayed(new Runnable() {
echo             @Override
echo             public void run() {
echo                 Intent intent = new Intent(SplashActivity.this, MainActivity.class);
echo                 startActivity(intent);
echo                 finish();
echo             }
echo         }, 2000);
echo     }
echo }
)
>> "%PROJECT%\app\src\main\java\com\pmo\cascade\MainActivity.java" (
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
echo import android.os.Handler;
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
echo import android.widget.RelativeLayout;
echo import android.widget.TextView;
echo import android.graphics.Color;
echo.
echo public class MainActivity extends Activity {
echo     private WebView webView;
echo     private ProgressBar progressBar;
echo     private TextView statusText;
echo     private static final String RAILWAY_URL = "https://web-production-c8682.up.railway.app";
echo     private static final String LOCAL_URL = "http://10.0.2.2:9000";
echo     private boolean loaded = false;
echo.
echo     @Override
echo     protected void onCreate(Bundle savedInstanceState) {
echo         super.onCreate(savedInstanceState);
echo         requestWindowFeature(Window.FEATURE_NO_TITLE);
echo         getWindow().setFlags(
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN,
echo             WindowManager.LayoutParams.FLAG_FULLSCREEN
echo         );
echo.
echo         RelativeLayout root = new RelativeLayout(this);
echo         root.setLayoutParams(new RelativeLayout.LayoutParams(
echo             RelativeLayout.LayoutParams.MATCH_PARENT,
echo             RelativeLayout.LayoutParams.MATCH_PARENT
echo         ));
echo         root.setBackgroundColor(Color.parseColor("#0a0a0f"));
echo.
echo         progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
echo         progressBar.setId(View.generateViewId());
echo         RelativeLayout.LayoutParams pbParams = new RelativeLayout.LayoutParams(
echo             RelativeLayout.LayoutParams.MATCH_PARENT, 3
echo         );
echo         pbParams.addRule(RelativeLayout.ALIGN_PARENT_TOP);
echo         progressBar.setLayoutParams(pbParams);
echo         progressBar.setVisibility(View.GONE);
echo         progressBar.setMax(100);
echo         root.addView(progressBar);
echo.
echo         statusText = new TextView(this);
echo         statusText.setText("Connecting to server...");
echo         statusText.setTextColor(Color.parseColor("#8899AA"));
echo         statusText.setTextSize(16);
echo         statusText.setGravity(android.view.Gravity.CENTER);
echo         RelativeLayout.LayoutParams stParams = new RelativeLayout.LayoutParams(
echo             RelativeLayout.LayoutParams.WRAP_CONTENT,
echo             RelativeLayout.LayoutParams.WRAP_CONTENT
echo         );
echo         stParams.addRule(RelativeLayout.CENTER_IN_PARENT);
echo         statusText.setLayoutParams(stParams);
echo         root.addView(statusText);
echo.
echo         webView = new WebView(this);
echo         webView.setId(View.generateViewId());
echo         RelativeLayout.LayoutParams wvParams = new RelativeLayout.LayoutParams(
echo             RelativeLayout.LayoutParams.MATCH_PARENT,
echo             RelativeLayout.LayoutParams.MATCH_PARENT
echo         );
echo         wvParams.addRule(RelativeLayout.BELOW, progressBar.getId());
echo         webView.setLayoutParams(wvParams);
echo         webView.setVisibility(View.GONE);
echo         root.addView(webView);
echo.
echo         setContentView(root);
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
echo         settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
echo.
echo         webView.setWebViewClient(new WebViewClient() {
echo             @Override
echo             public void onPageStarted(WebView view, String url, Bitmap favicon) {
echo                 progressBar.setVisibility(View.VISIBLE);
echo                 progressBar.setProgress(0);
echo             }
echo             @Override
echo             public void onPageFinished(WebView view, String url) {
echo                 progressBar.setVisibility(View.GONE);
echo                 if (!loaded) {
echo                     loaded = true;
echo                     statusText.setVisibility(View.GONE);
echo                     webView.setVisibility(View.VISIBLE);
echo                 }
echo             }
echo             @Override
echo             public void onReceivedSslError(WebView view, SslErrorHandler handler, android.net.http.SslError error) {
echo                 handler.proceed();
echo             }
echo             @Override
echo             public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
echo                 if (!loaded) {
echo                     statusText.setText("Cannot connect to cloud server.\nCheck internet or try again.");
echo                     new Handler().postDelayed(new Runnable() {
echo                         @Override
echo                         public void run() {
echo                             webView.loadUrl(RAILWAY_URL);
echo                         }
echo                     }, 3000);
echo                 }
echo             }
echo         });
echo.
echo         webView.setWebChromeClient(new WebChromeClient() {
echo             @Override
echo             public void onProgressChanged(WebView view, int newProgress) {
echo                 progressBar.setProgress(newProgress);
echo             }
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
echo         if (isNetworkAvailable()) {
echo             statusText.setText("Connecting to PMO CASCADE cloud...");
echo             webView.loadUrl(RAILWAY_URL);
echo         } else {
echo             statusText.setText("No internet connection.\nPlease connect to the internet and restart.");
echo         }
echo     }
echo.
echo     private boolean isNetworkAvailable() {
echo         ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
echo         NetworkInfo netInfo = cm.getActiveNetworkInfo();
echo         return netInfo != null && netInfo.isConnected();
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

echo [4/6] Writing resources...
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
echo     ^<style name="SplashTheme" parent="AppTheme"^>
echo         ^<item name="android:windowBackground"^>@drawable/splash_bg^</item^>
echo     ^</style^>
echo ^</resources^>
)
> "%PROJECT%\app\src\main\res\values\strings.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<resources^>
echo     ^<string name="app_name"^>PMO Cascade^</string^>
echo ^</resources^>
)
> "%PROJECT%\app\src\main\res\drawable\splash_bg.xml" (
echo ^<?xml version="1.0" encoding="utf-8"?^>
echo ^<layer-list xmlns:android="http://schemas.android.com/apk/res/android"^>
echo     ^<item android:drawable="@android:color/black" /^>
echo ^</layer-list^>
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
echo         versionCode 2
echo         versionName "2.0"
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
echo  Target: %RAILWAY_URL%
echo.
echo  NOTE: Requires Android SDK + JDK 17.
echo  If ANDROID_HOME/JAVA_HOME not set, outputs project folder instead.
echo.

if not "%ANDROID_HOME%"=="" (
    if not "%JAVA_HOME%"=="" (
        cd /d "%PROJECT%"
        call gradlew.bat assembleDebug 2>&1
        for /r "%PROJECT%" %%f in (*.apk) do (
            copy "%%f" "%OUTPUT_DIR%\%APP_NAME%_v2.0.apk" /y
            echo --------------------------------------------
            echo  BUILD SUCCESS
            echo  APK: %OUTPUT_DIR%\%APP_NAME%_v2.0.apk
            echo --------------------------------------------
        )
        goto :done
    )
)

echo  ANDROID_HOME or JAVA_HOME not set.
echo  Generating Android project for manual build...
xcopy /E /I /Y "%PROJECT%" "%OUTPUT_DIR%\%APP_NAME%_Android_Project"
echo --------------------------------------------
echo  PROJECT READY
echo  Location: %OUTPUT_DIR%\%APP_NAME%_Android_Project
echo.
echo  To build APK:
echo  1. Install Android Studio (developer.android.com/studio)
echo  2. Open the project folder
echo  3. Build ^> Build APK
echo --------------------------------------------

:done
cd /d "%OUTPUT_DIR%"
dir *.apk 2>nul
echo.
echo  PMO CASCADE Android APK Builder Complete
echo  GitHub: https://github.com/hamadasaied613-oss/pmo-cascade-engine
echo  Cloud:  %RAILWAY_URL%
pause