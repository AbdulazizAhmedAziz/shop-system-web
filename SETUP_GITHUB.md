# 📝 خطوات رفع المشروع على GitHub

## الخطوة 1: إنشاء مستودع على GitHub

1. **اذهب إلى:** https://github.com
2. **سجل دخول** (أو أنشئ حساب جديد)
3. **اضغط على زر "+"** في أعلى الصفحة
4. **اختر "New repository"**
5. **املأ البيانات:**
   - **Repository name:** `shop-system-web` (أو أي اسم تريده)
   - **Description:** `Smart Shop System Web Application`
   - **اختر:** Public (أو Private)
   - **⚠️ لا تضع علامة على:** "Initialize this repository with a README"
   - **⚠️ لا تختار:** .gitignore أو license
6. **اضغط "Create repository"**

## الخطوة 2: ربط المشروع المحلي بـ GitHub

بعد إنشاء المستودع، GitHub سيعطيك أوامر. استخدم هذه الأوامر:

```bash
cd /Users/abdulazizahmedabdulaziz/shop-system-web
git remote add origin https://github.com/YOUR_USERNAME/shop-system-web.git
git push -u origin main
```

**⚠️ استبدل `YOUR_USERNAME` باسم المستخدم الخاص بك على GitHub!**

## الخطوة 3: التحقق

اذهب إلى صفحة المستودع على GitHub وتأكد من ظهور جميع الملفات.

---

## 🚀 بعد ذلك: النشر على Render

بعد رفع الكود على GitHub، اتبع الخطوات في `QUICK_DEPLOY.md` للنشر على Render!

