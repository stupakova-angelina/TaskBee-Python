import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

TASK_FILE = "my_tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

class BeeDoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("🐝 BeeDo — Сделай это!")
        self.tasks = load_tasks()  # Загружаем при старте

       
        self.entry = tk.Entry(window, width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.add_task())  # Enter → добавить

       
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Добавить", command=self.add_task).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="✅ Готово", command=self.mark_done).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🗑️ Удалить", command=self.remove_task).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="📁 Открыть", command=self.open_file).pack(side=tk.LEFT, padx=2)

       
        self.listbox = tk.Listbox(window, width=60, height=15, font=("Arial", 10))
        self.listbox.pack(pady=10, padx=10)

        self.refresh_list()

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка", "Задача не может быть пустой!")
            return
        self.tasks.append({"text": text, "done": False})
        self.refresh_list()
        self.entry.delete(0, tk.END)

    def mark_done(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.refresh_list()

    def remove_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Подсказка", "Выберите задачу для удаления")
            return
        idx = selected[0]
        del self.tasks[idx]
        self.refresh_list()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
                self.refresh_list()
                messagebox.showinfo("Успех", "Задачи загружены!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["done"] else "○"
            prefix = "[Готово] " if task["done"] else "[ ] "
            self.listbox.insert(tk.END, f"{status} {prefix}{task['text']}")

    def on_close(self):
        save_tasks(self.tasks)
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BeeDoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
