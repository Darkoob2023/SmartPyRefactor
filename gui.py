import tkinter as tk
from tkinter import scrolledtext, messagebox
from analyzer import analyze_code, get_combined_score, refactor_code

def analyze_code_gui():
    code = code_text.get("1.0", tk.END)
    if not code.strip():
        messagebox.showwarning("Warning", "کد خالی است!")
        return

    analysis = analyze_code(code)

    with open("temp_code.py", "w", encoding="utf-8") as f:
        f.write(code)

    combined_score = get_combined_score("temp_code.py")

    suggested, warnings, diff_text = refactor_code(code)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "📊 AST Analysis:\n")
    for k, v in analysis.items():
        output_text.insert(tk.END, f"{k}: {v}\n")
    output_text.insert(tk.END, f"\n📌 Combined Score: {combined_score}/10\n")
    if warnings:
        output_text.insert(tk.END, "\n⚠️ Refactor Warnings:\n")
        for w in warnings:
            output_text.insert(tk.END, f"{w}\n")
    output_text.config(state=tk.DISABLED)

    suggested_text.config(state=tk.NORMAL)
    suggested_text.delete("1.0", tk.END)
    suggested_text.insert("1.0", "=== BEFORE ===\n", "before")
    suggested_text.insert("2.0", code + "\n", "before_code")
    suggested_text.insert(tk.END, "\n=== AFTER ===\n", "after")
    suggested_text.insert(tk.END, suggested + "\n", "after_code")
    if diff_text:
        suggested_text.insert(tk.END, "\n=== DIFF ===\n", "diff")
        suggested_text.insert(tk.END, diff_text, "diff_text")

    suggested_text.tag_config("before", foreground="red")
    suggested_text.tag_config("after", foreground="green")
    suggested_text.tag_config("diff", foreground="orange")
    suggested_text.tag_config("before_code", foreground="black")
    suggested_text.tag_config("after_code", foreground="blue")
    suggested_text.tag_config("diff_text", foreground="purple")
    suggested_text.config(state=tk.DISABLED)


# ------------------ UI ------------------
root = tk.Tk()
root.title("Python Code Analyzer & Advanced Refactor v2")
root.geometry("1000x800")

tk.Label(root, text="Your Code").pack()
code_text = scrolledtext.ScrolledText(root, width=120, height=15)
code_text.pack(pady=5)

analyze_btn = tk.Button(root, text="Analyze & Refactor", command=analyze_code_gui)
analyze_btn.pack(pady=10)

tk.Label(root, text="Analysis Report").pack()
output_text = scrolledtext.ScrolledText(root, width=120, height=10, state=tk.DISABLED)
output_text.pack(pady=5)

tk.Label(root, text="Suggested Code Before / After / Diff").pack()
suggested_text = scrolledtext.ScrolledText(root, width=120, height=20)
suggested_text.pack(pady=5)

root.mainloop()