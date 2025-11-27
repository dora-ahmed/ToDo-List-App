import customtkinter as ctk
from add_task_page import AddTaskPage
from delete_task_page import DeleteTaskPage
from classify_tasks_page import ClassifyTasksPage
from edit_task_page import EditTaskPage
from ViewTasksPage import ViewTasksPage # <--- 1. إضافة استيراد الصفحة الجديدة

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("القائمة الرئيسيه لToDo")
        # قمت بزيادة الطول قليلاً
        self.geometry("400x400")

        ctk.CTkLabel(self, text="القائمة الرئيسية", font=("Arial", 22)).pack(pady=20)

        ctk.CTkButton(self, text="➕ إضافة مهمة", width=200,
                      command=lambda: AddTaskPage(self)).pack(pady=10)

        ctk.CTkButton(self, text="🗑️ حذف مهمة", width=200,
                      command=lambda: DeleteTaskPage(self)).pack(pady=10)

        # أزرار الفريق
        ctk.CTkButton(self, text="✏️ تعديل مهمة (للفريق)", width=200,
                      command=lambda: EditTaskPage(self)).pack(pady=5)

        ctk.CTkButton(self, text="📂 التصنيف (للفريق)", width=200,
                      command=lambda: ClassifyTasksPage(self)).pack(pady=5)

        # 2. تفعيل الزر وربطه بالصفحة الجديدة
        ctk.CTkButton(self, text="✔️ عرض المنتهي والمتأخر (للفريق)", width=200,
                      command=lambda: ViewTasksPage(self)).pack(pady=5) # <--- تم تعديل هذا السطر


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()