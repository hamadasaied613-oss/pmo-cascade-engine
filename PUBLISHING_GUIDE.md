# ═══════════════════════════════════════════════════════════════
# PMO CASCADE — خطوة بخطوة للنشر
# ═══════════════════════════════════════════════════════════════

## الخطوة 0: اختبار نهائي (افتح Chrome الآن)

```
1. افتح Chrome
2. اكتب في الشريط: http://localhost:9000
3. يجب أن ترى الصفحة الرئيسية مع:
   - زر "Open Design Catalog" → اضغط عليه → يجب أن يفتح نافذة منبثقة
   - اختر أي طراز → Next → اختر تشطيبات → Finish
   - اضغط "Run Full Cascade" → يجب أن يظهر النتيجة
4. جرب "Export" → Excel Report → يجب أن يُحمّل ملف
5. جرب "Save Project" → احفظ → ثم "Load"
```

**إذا لم يعمل:** شغّل `LAUNCH_APP.bat` كمدير

---

## الخطوة 1: تطبيق أندرويد (مجاناً — اليوم)

### ما تحتاجه:
- حساب Google Developer (25$ مرة واحدة فقط)
- Android Studio (مجاني)

### خطوات التنفيذ:

#### أ) تجهيز مشروع أندرويد:
```
1. اضغط Windows+R → اكتب: cmd
2. اكتب:
   cd D:\Work\DOMAINS
   BUILD_ANDROID_APK.bat
3. سيُنشأ مشروع في:
   %TEMP%\pmo_cascade_android_xxx\ أو
   D:\Work\DOMAINS\build_output\PMO_Cascade_Android_Project
```

#### ب) فتح المشروع في Android Studio:
```
1. حمّل Android Studio من: https://developer.android.com/studio
2. افتح Android Studio → Open → اختر المجلد الذي أنشأناه
3. انتظر حتى يكمل Gradle Sync
4. Build → Build Bundle(s) / APK(s) → Build APK(s)
5. سيُنشأ APK في: app/build/outputs/apk/debug/app-debug.apk
```

#### ج) رفع APK على Google Play:
```
1. اذهب إلى: https://play.google.com/console
2. سجّل حساب مطور (25$)
3. Create App → اختر اسم ووصف
4. Production → Create new release
5. ارفع ملف APK
6. أكمل الأسئلة (خصوصية، تصنيف، إلخ)
7. اضغط Review → Rollout to production
```

#### ملاحظة مهمة:
التطبيق يحتاج خادم (server) للعمل. للإصدار المحلي:
- ارفع الخادم على Railway.app (مجاني — 500 ساعة/شهر)
- غيّر `SERVER_URL` في MainActivity.java إلى رابط Railway

---

## الخطوة 2: تطبيق سطح مكتب (مجاناً — اليوم)

### ملفات جاهزة:
- `SOVEREIGN_APP.py` — التطبيق المحمول
- `LAUNCH_APP.bat` — ملف التشغيل

### للتشغيل:
```
1. اضغط مرتين على LAUNCH_APP.bat
2. سيفتح نافذة مستقلة بالتطبيق
3. للتفعيل على جهاز آخر:
   - انسخ مجلد D:\Work\DOMAINS بالكامل
   - شغّل LAUNCH_APP.bat
```

### لتوزيعه:
```
1. اجمع الملفات في مجلد واحد:
   - SOVEREIGN_APP.py
   - SOVEREIGN_SERVER.py
   - SOVEREIGN.html
   - static/ (مجلد الصور)
   - _GATEWAY_TABLES/ (مجلد قاعدة البيانات)
   - _PMO_OUTPUTS/
   - _PMO_DELIVERABLES/
   - LAUNCH_APP.bat
2. اضغط على المجلد بالزر الأيمن → Send to → Compressed folder
3. وزّع الملف المضغوط
```

---

## الخطوة 3: Gumroad (مجاناً — للبيع المباشر)

### خطوات التنفيذ:
```
1. اذهب إلى: https://gumroad.com
2. سجّل حساب (مجاني)
3. Create a product → Digital product
4. اسم المنتج: "PMO CASCADE Sovereign Engine"
5. السعر: ابدأ بـ 49$ (يمكنك تغييره لاحقاً)
6. ارفع الملف المضغوط
7. اكتب الوصف من PLAY_STORE_LISTING.md
8. اضغط Publish
9. شارك الرابط على وسائل التواصل
```

### للحصول على Free Trial:
```
1. في Gumroad → Pricing → اختر "Pay what you want"
2. اكتب: "Free trial — email required"
3. بعد 7 أيام أرسل لهم عرض الاشتراك
```

---

## الخطوة 4: Product Hunt (مجاني — لإطلاق المنتج)

### خطوات التنفيذ:
```
1. اذهب إلى: https://www.producthunt.com
2. سجّل حساب → Maker
3. اضغط "Submit"
4. اسم المنتج: "PMO CASCADE — UAE Feasibility Engine"
5. Tagline: "5 inputs → 12 domain engineering analysis"
6. رابط: رابط Gumroad
7. صور: صدّر screenshots من التطبيق
8. وصف: من PLAY_STORE_LISTING.md
9. اختر تاريخ الإطلاق (الثلاثاء أو الأربعاء أفضل)
10. شارك على Twitter و LinkedIn قبل وبعد الإطلاق
```

---

## الخطوة 5: صفحة هبوط (مجاناً — Carrd.co)

### خطوات التنفيذ:
```
1. اذهب إلى: https://carrd.co
2. سجّل حساب (مجاني — 3 صفحات)
3. Choose a template → اختر أي قالب
4. حرر المحتوى:
   - العنوان: "PMO CASCADE Sovereign Engine"
   - الوصف: "UAE Real Estate Feasibility Platform"
   - Zapper: "Run feasibility in 5 clicks"
   - زر: "Get Started" → رابط Gumroad
5. اضغط Publish
6. احصل على رابط مجاني like: pmo-cascade.carrd.co
```

---

## 💰 نموذج الدخل المتوقع:

| المنصة | السعر | مبيعات/شهر | الدخل الشهري |
|--------|-------|------------|--------------|
| Gumroad | 49$ | 10 | 490$ |
| Play Store | 9.99$ | 50 | 499$ |
| Carrd (صفحة هبوط) | مجاني | — | تعزيز المبيعات |
| Product Hunt | مجاني | — | حركة مرور مجانية |
| **الإجمالي** | | | **~989$** |

---

## ⚡ ابدأ الآن (الخطة السريعة):

```
اليوم:
1. ✅ اختبر التطبيق في Chrome → http://localhost:9000
2. ✅ شغّل LAUNCH_APP.bat للتطبيق المستقل
3. ✅ رفع على Gumroad (10 دقائق)

غداً:
4. ✅ حمّل Android Studio
5. ✅ اشتر حساب مطور (25$)
6. ✅ ابني APK وارفعه على Play Store

بعد 3 أيام:
7. ✅ أنشئ صفحة هبوط على Carrd
8. ✅ أطلق على Product Hunt
9. ✅ شارك على LinkedIn و Twitter
```
