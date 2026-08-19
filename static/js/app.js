// فعال‌سازی آیکون‌های Lucide
document.addEventListener("DOMContentLoaded", () => {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // تابع هوشمند تبدیل اعداد به فارسی و سه رقم سه رقم جدا کردن
    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    
    document.querySelectorAll('.persian-num').forEach(el => {
        let text = el.innerText.trim().replace(/,/g, ''); // حذف کاماهای قبلی
        if(!isNaN(text) && text !== "") {
            // فرمت سه رقم سه رقم
            let formatted = Number(text).toLocaleString('en-US');
            // تبدیل به فارسی
            el.innerText = formatted.replace(/\d/g, x => persianDigits[x]);
        }
    });
});

// تابع تغییر تب‌ها در صفحه محصول
function switchTab(tab) {
    const descBtn = document.getElementById('tab-desc');
    const comBtn = document.getElementById('tab-comments');
    const descContent = document.getElementById('content-desc');
    const comContent = document.getElementById('content-comments');

    if (!descBtn || !comBtn) return;

    if(tab === 'desc') {
        descContent.classList.remove('hidden');
        comContent.classList.add('hidden');
        descBtn.className = "px-6 py-4 text-sm font-bold text-digikala-red border-b-4 border-digikala-red";
        comBtn.className = "px-6 py-4 text-sm font-bold text-gray-500 border-b-4 border-transparent hover:text-digikala-red transition";
    } else {
        comContent.classList.remove('hidden');
        descContent.classList.add('hidden');
        comBtn.className = "px-6 py-4 text-sm font-bold text-digikala-red border-b-4 border-digikala-red";
        descBtn.className = "px-6 py-4 text-sm font-bold text-gray-500 border-b-4 border-transparent hover:text-digikala-red transition";
    }
}