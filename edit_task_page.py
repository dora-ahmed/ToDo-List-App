import customtkinter as ctk
from utils import load_tasks, save_tasks


class EditTaskPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("تعديل مهمة")
        self.geometry("500x500")

        ctk.CTkLabel(self, text="تعديل عنوان المهمة", font=("Arial", 20, "bold")).pack(pady=10)

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

        # 2. إدخال العنوان الجديد
        ctk.CTkLabel(control_frame, text="العنوان الجديد:").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.new_title_entry = ctk.CTkEntry(control_frame, width=200, placeholder_text="اكتب التعديل هنا")
        self.new_title_entry.grid(row=1, column=1, padx=10, pady=10)

        # زر الحفظ
        self.save_btn = ctk.CTkButton(self, text="حفظ التعديل", command=self.update_task)
        self.save_btn.pack(pady=10)

        # رسالة التنبيه
        self.status_label = ctk.CTkLabel(self, text="", text_color="blue")
        self.status_label.pack()

    def refresh_view(self):
        """تحديث القائمة المعروضة"""
        self.listbox.configure(state="normal")
        self.listbox.delete("0.0", "end")

        if not self.tasks:
            self.listbox.insert("end", "لا توجد مهام حالياً.")
        else:
            for i, task in enumerate(self.tasks, start=1):
                # عرض العنوان الحالي
                line = f"{i}. {task['title']}\n"
                self.listbox.insert("end", line)

        self.listbox.configure(state="disabled")

    def update_task(self):
        """حفظ العنوان الجديد للمهمة المختارة"""
        try:
            # الحصول على رقم المهمة (مع مراعاة أن القائمة تبدأ من 0 والواجهة من 1)
            task_index = int(self.task_num_entry.get()) - 1
            new_title = self.new_title_entry.get().strip()

            if not new_title:
                self.status_label.configure(text="⚠️ يرجى كتابة عنوان جديد", text_color="orange")
                return

            if 0 <= task_index < len(self.tasks):
                # حفظ العنوان القديم للعرض في الرسالة
                old_title = self.tasks[task_index]['title']

                # تحديث العنوان في الذاكرة
                self.tasks[task_index]['title'] = new_title

                # حفظ في ملف JSON
                save_tasks(self.tasks)

                # تحديث الواجهة ورسالة النجاح
                self.refresh_view()
                self.status_label.configure(text=f"✔️ تم تغيير '{old_title}' إلى '{new_title}'",
                                            text_color="green")

                # تنظيف الحقول
                self.task_num_entry.delete(0, "end")
                self.new_title_entry.delete(0, "end")
            else:
                self.status_label.configure(text="❌ رقم المهمة غير صحيح", text_color="red")

        except ValueError:
            self.status_label.configure(text="❌ الرجاء إدخال رقم صحيح", text_color="red")