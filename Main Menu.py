import customtkinter as ctk
from add_task_page import AddTaskPage
from delete_task_page import DeleteTaskPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("القائمة الرئيسية لـ ToDo")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="القائمة الرئيسية", font=("Arial", 22)).pack(pady=20)

        ctk.CTkButton(self, text="➕ إضافة مهمة", width=200,
                      command=lambda: AddTaskPage(self)).pack(pady=10)

        ctk.CTkButton(self, text="🗑️ حذف مهمة", width=200,
                      command=lambda: DeleteTaskPage(self)).pack(pady=10)

        # أزرار الفريق (فارغة حالياً)
        ctk.CTkButton(self, text="✏️ تعديل مهمة (للفريق)", width=200, state="disabled").pack(pady=5)
        ctk.CTkButton(self, text="📂 التصنيف (للفريق)", width=200, state="disabled").pack(pady=5)
        ctk.CTkButton(self, text="✔️ عرض المنتهي (للفريق)", width=200, state="disabled").pack(pady=5)


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
