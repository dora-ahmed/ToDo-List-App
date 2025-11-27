#add_task_page.py
import customtkinter as ctk
from utils import load_tasks, save_tasks
from datetime import datetime

class AddTaskPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("إضافة ممهمة")
        self.geometry("400x350")

        ctk.CTkLabel(self, text="إضافة مهمة جديدة", font=("Arial", 20)).pack(pady=10)

        # عنوان المهمة فقط (أنتِ مسؤولة عنه فقط الآن)
        self.task_entry = ctk.CTkEntry(self, placeholder_text="عنوان المهمة", width=300)
        self.task_entry.pack(pady=10)

        # زر إضافة
        ctk.CTkButton(self, text="إضافة", command=self.add_task).pack(pady=10)

        # رسالة نجاح
        self.msg_label = ctk.CTkLabel(self, text="", text_color="green")
        self.msg_label.pack()

    def add_task(self):
        title = self.task_entry.get().strip()

        if title:
            tasks = load_tasks()
            tasks.append({
                "title": title,
                "category": "",       # الفريق سيستخدمها لاحقًا
                "date": str(datetime.today().date()),
                "status": "unfinished"
            })

            save_tasks(tasks)
            self.msg_label.configure(text="✔️ تمت إضافة المهمة")
            self.task_entry.delete(0, "end")
