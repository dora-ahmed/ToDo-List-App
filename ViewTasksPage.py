import customtkinter as ctk
from utils import load_tasks
from datetime import date, datetime


class ViewTasksPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("✔️ عرض المهام المنتهية والمتأخرة")
        self.geometry("500x500")

        ctk.CTkLabel(self, text="قائمة المهام المنتهية أو المتأخرة", font=("Arial", 20)).pack(pady=15)

        # إطار لعرض النتائج
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="المهام")
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.filter_and_display_tasks()

    def filter_tasks(self):
        """تقوم بتحميل وترشيح المهام المنتهية أو المتأخرة."""

        tasks = load_tasks()
        today = date.today()
        filtered_tasks = []

        for i, task in enumerate(tasks, start=1):

            task_status = task.get("status", "unfinished")  # الوضع الافتراضي 'unfinished'
            task_date_str = task.get("date")  # التاريخ بصيغة 'YYYY-MM-DD'
            task_title = task.get("title", "بدون عنوان")
            task_category = task.get("category", "غير مصنف")

            # 1. المهام المنتهية (Completed)
            if task_status == "finished":  # يجب أن تفترض أن حالتك ستستخدم 'finished'
                filtered_tasks.append({
                    "index": i,
                    "title": task_title,
                    "category": task_category,
                    "date": task_date_str,
                    "type": "منتهية ✔️"
                })
                continue

            # 2. المهام المتأخرة (Overdue)
            if task_date_str:
                try:
                    # تحويل التاريخ من نص إلى كائن تاريخ للمقارنة
                    task_date = datetime.strptime(task_date_str, "%Y-%m-%d").date()

                    # إذا كان تاريخ المهمة أقل من التاريخ الحالي (في الماضي) والحالة ليست منتهية
                    if task_date < today and task_status != "finished":
                        filtered_tasks.append({
                            "index": i,
                            "title": task_title,
                            "category": task_category,
                            "date": task_date_str,
                            "type": "متأخرة ⚠️"
                        })
                except ValueError:
                    # تجاهل المهام ذات التنسيق الخاطئ للتاريخ
                    pass

        return filtered_tasks

    def filter_and_display_tasks(self):
        """عرض المهام المفلترة في الإطار."""

        filtered_tasks = self.filter_tasks()

        # مسح أي عناصر سابقة في الإطار
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not filtered_tasks:
            ctk.CTkLabel(self.results_frame, text="لا توجد مهام منتهية أو متأخرة حالياً.", font=("Arial", 16)).pack(
                pady=20)
            return

        for task in filtered_tasks:
            # تنسيق العرض للمهمة
            display_text = (
                f'#{task["index"]} - {task["title"]}\n'
                f'[{task["type"]}] | التصنيف: {task["category"]} | التاريخ: {task["date"]}'
            )

            # تحديد الألوان
            if task["type"] == "منتهية ✔️":
                bg_color = ("green", "darkgreen")
            else:  # متأخرة ⚠️
                bg_color = ("red", "darkred")

            task_label = ctk.CTkLabel(
                self.results_frame,
                text=display_text,
                anchor="e",
                justify="right",
                padx=10,
                pady=5,
                fg_color=bg_color,
                text_color="white",
                corner_radius=8
            )
            task_label.pack(fill="x", pady=5)