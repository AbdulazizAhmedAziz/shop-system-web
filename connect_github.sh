#!/bin/bash

# سكريبت لربط المشروع بـ GitHub
# استخدم: bash connect_github.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "❌ خطأ: يجب إدخال اسم المستخدم على GitHub"
    echo "الاستخدام: bash connect_github.sh YOUR_GITHUB_USERNAME"
    echo "مثال: bash connect_github.sh abdulaziz123"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="shop-system-web"

echo "🔗 جاري ربط المشروع بـ GitHub..."
echo "اسم المستخدم: $GITHUB_USERNAME"
echo "اسم المستودع: $REPO_NAME"
echo ""

# التحقق من وجود remote
if git remote get-url origin &>/dev/null; then
    echo "⚠️  يوجد remote مسبقاً. هل تريد استبداله؟ (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        git remote remove origin
    else
        echo "❌ تم الإلغاء"
        exit 1
    fi
fi

# إضافة remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "✅ تم ربط المشروع بـ GitHub"
echo ""
echo "📤 جاري رفع الكود..."
echo "⚠️  سيطلب منك اسم المستخدم وكلمة المرور"
echo "   - اسم المستخدم: $GITHUB_USERNAME"
echo "   - كلمة المرور: استخدم Personal Access Token (ليس كلمة المرور العادية)"
echo ""
echo "📝 إذا لم يكن لديك Token، أنشئه من: https://github.com/settings/tokens"
echo ""

# رفع الكود
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 تم رفع الكود بنجاح!"
    echo "👉 يمكنك الآن رؤية المشروع على: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
else
    echo ""
    echo "❌ حدث خطأ أثناء رفع الكود"
    echo "تأكد من:"
    echo "  1. أنك أنشأت المستودع على GitHub"
    echo "  2. أن اسم المستخدم صحيح"
    echo "  3. أنك استخدمت Personal Access Token ككلمة مرور"
fi

