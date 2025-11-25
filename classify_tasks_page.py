import customtkinter as ctk
from utils import load_tasks, save_tasks


class ClassifyTasksPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("تصنيف المهام")
        self.geometry("500x500")

        ctk.CTkLabel(self, text="تصنيف وتحديث المهام", font=("Arial", 20, "bold")).pack(pady=10)

        # تحميل المهام
        self.tasks = load_tasks()

        # صندوق عرض المهام (للقراءة فقط)
        self.listbox = ctk.CTkTextbox(self, width=450, height=200)
        self.listbox.pack(pady=10)

        # عرض البيانات فور الفتح
        self.refresh_view()

        # --- منطقة التحكم ---
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=20, padx=20, fill="x")

        # 1. إدخال رقم المهمة
        ctk.CTkLabel(control_frame, text="رقم المهمة:").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.task_num_entry = ctk.CTkEntry(control_frame, width=60, placeholder_text="#")
        self.task_num_entry.grid(row=0, column=1, padx=10, pady=10)

        # 2. اختيار التصنيف
        ctk.CTkLabel(control_frame, text="اختر التصنيف:").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.category_menu = ctk.CTkComboBox(control_frame,
                                             values=["عمل", "دراسة", "شخصي", "تسوق", "أخرى"],
                                             width=150)
        self.category_menu.grid(row=1, column=1, padx=10, pady=10)

        # زر الحفظ
        self.save_btn = ctk.CTkButton(self, text="حفظ التصنيف", command=self.update_category)
        self.save_btn.pack(pady=10)

        # رسالة التنبيه
        self.status_label = ctk.CTkLabel(self, text="", text_color="blue")
        self.status_label.pack()

    def refresh_view(self):
        """تحديث القائمة المعروضة"""
        self.listbox.configure(state="normal")  # تفعيل الكتابة مؤقتاً
        self.listbox.delete("0.0", "end")

        if not self.tasks:
            self.listbox.insert("end", "لا توجد مهام حالياً.")
        else:
            for i, task in enumerate(self.tasks, start=1):
                # نتحقق هل يوجد تصنيف أم لا
                cat = task.get('category')
                display_cat = cat if cat else "غير مصنف"

                # تنسيق النص المعروض
                line = f"{i}. {task['title']}  |  التصنيف: [{display_cat}]\n"
                self.listbox.insert("end", line)

        self.listbox.configure(state="disabled")  # منع المستخدم من الكتابة يدوياً في القائمة

    def update_category(self):
        """حفظ التصنيف الجديد للمهمة المختارة"""
        try:
            # الحصول على رقم المهمة (مع مراعاة أن القائمة تبدأ من 0 والواجهة من 1)
            task_index = int(self.task_num_entry.get()) - 1
            new_category = self.category_menu.get()

            if 0 <= task_index < len(self.tasks):
                # تحديث التصنيف في الذاكرة
                self.tasks[task_index]['category'] = new_category

                # حفظ في ملف JSON
                save_tasks(self.tasks)

                # تحديث الواجهة ورسالة النجاح
                self.refresh_view()
                self.status_label.configure(text=f"✔️ تم تصنيف المهمة رقم {task_index + 1} كـ '{new_category}'",
                                            text_color="green")
                self.task_num_entry.delete(0, "end")
            else:
                self.status_label.configure(text="❌ رقم المهمة غير صحيح", text_color="red")

        except ValueError:
            self.status_label.configure(text="❌ الرجاء إدخال رقم صحيح", text_color="red")