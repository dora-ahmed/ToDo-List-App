#delete_task_page.py
import customtkinter as ctk
from utils import load_tasks, save_tasks

class DeleteTaskPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("حذف مهمة")
        self.geometry("450x400")

        ctk.CTkLabel(self, text="اختر مهمة لحذفها", font=("Arial", 20)).pack(pady=10)

        self.tasks = load_tasks()

        self.listbox = ctk.CTkTextbox(self, width=380, height=250)
        self.listbox.pack(pady=10)
        self.refresh_view()

        ctk.CTkButton(self, text="حذف", command=self.delete_task).pack(pady=10)

    def refresh_view(self):
        self.listbox.delete("0.0", "end")
        for i, task in enumerate(self.tasks, start=1):
            self.listbox.insert("end", f"{i}. {task['title']} ({task['status']})\n")

    def delete_task(self):
        try:
            index = int(self.listbox.index("insert").split(".")[0]) - 1
            self.tasks.pop(index)
            save_tasks(self.tasks)
            self.refresh_view()
        except:
            pass
