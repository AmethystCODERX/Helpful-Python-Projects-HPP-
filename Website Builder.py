import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import pyperclip


class WebsiteBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Maker")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")

        self.elements = []

        self.html_align_map = {
            "w": "left",
            "center": "center",
            "e": "right"
        }

        self.setup_ui()

    def setup_ui(self):
        # Левая панель
        left_panel = tk.Frame(self.root, bg="#2b2b2b", width=260)
        left_panel.pack(side="left", fill="y")

        title = tk.Label(
            left_panel,
            text="Designer",
            font=("Arial", 20, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title.pack(pady=20)

        # Кнопки элементов
        self.create_button(left_panel, "Add title", self.add_heading)
        self.create_button(left_panel, "Add text", self.add_text)
        self.create_button(left_panel, "Add button", self.add_button)
        self.create_button(left_panel, "Add image", self.add_image)
        self.create_button(left_panel, "Add container", self.add_container)

        separator = ttk.Separator(left_panel, orient="horizontal")
        separator.pack(fill="x", pady=20)

        self.create_button(left_panel, "Clear all elements", self.clear_site, color="#d9534f")
        self.create_button(left_panel, "Convert and copy as HTML", self.export_html, color="#5cb85c")

        # Правая область
        right_panel = tk.Frame(self.root, bg="#1e1e1e")
        right_panel.pack(side="right", fill="both", expand=True)

        preview_label = tk.Label(
            right_panel,
            text="Website View",
            font=("Arial", 18, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        preview_label.pack(pady=10)

        self.canvas = tk.Canvas(
            right_panel,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

        self.preview_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")

        self.preview_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def create_button(self, parent, text, command, color="#3a7ff6"):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=10
        )
        btn.pack(fill="x", padx=15, pady=8)

    def add_heading(self):
        self.open_element_editor("heading")

    def add_text(self):
        self.open_element_editor("text")

    def add_button(self):
        self.open_element_editor("button")

    def add_image(self):
        self.open_element_editor("image")

    def add_container(self):
        self.open_element_editor("container")

    def open_element_editor(self, element_type):
        alignment_map = {
            "Left": "w",
            "Center": "center",
            "Right": "e"
        }

        html_align_map = {
            "w": "left",
            "center": "center",
            "e": "right"
        }

        fonts = [
            "Arial",
            "Verdana",
            "Helvetica",
            "Times New Roman",
            "Courier New",
            "Georgia",
            "Comic Sans MS",
            "Impact"
        ]
        editor = tk.Toplevel(self.root)
        editor.title(f"Setting: {element_type}")
        editor.geometry("400x600")
        editor.configure(bg="#2b2b2b")

        tk.Label(
            editor,
            text="Text / Content",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        content_entry = tk.Entry(editor, font=("Arial", 12), width=35)
        content_entry.pack(pady=5)

        tk.Label(
            editor,
            text="Font",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        font_var = tk.StringVar(value="Arial")

        font_box = ttk.Combobox(
            editor,
            textvariable=font_var,
            values=fonts,
            state="readonly",
            width=30
        )
        font_box.pack(pady=5)

        tk.Label(
            editor,
            text="Side",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        align_var = tk.StringVar(value="Center")

        align_box = ttk.Combobox(
            editor,
            textvariable=align_var,
            values=list(alignment_map.keys()),
            state="readonly",
            width=30
        )
        align_box.pack(pady=5)

        tk.Label(
            editor,
            text="Size of text",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        size_spin = tk.Spinbox(editor, from_=10, to=72, width=10)
        size_spin.pack(pady=5)
        size_spin.delete(0, "end")
        size_spin.insert(0, "24")

        tk.Label(
            editor,
            text="A link for button (URL)",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        link_entry = tk.Entry(editor, font=("Arial", 12), width=35)
        link_entry.pack(pady=5)

        tk.Label(
            editor,
            text="colour",
            bg="#2b2b2b",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        color_var = tk.StringVar(value="#000000")

        color_frame = tk.Frame(editor, bg="#2b2b2b")
        color_frame.pack(pady=5)

        color_preview = tk.Label(color_frame, bg="#000000", width=4, height=2)
        color_preview.pack(side="left", padx=5)

        def pick_color():
            color = colorchooser.askcolor()[1]
            if color:
                color_var.set(color)
                color_preview.configure(bg=color)

        tk.Button(
            color_frame,
            text="Change colour",
            command=pick_color
        ).pack(side="left", padx=10)

        def save_element():
            content = content_entry.get()
            size = int(size_spin.get())
            color = color_var.get()
            font_name = font_var.get()
            alignment = alignment_map[align_var.get()]

            if not content and element_type != "container":
                messagebox.showwarning("Error", "Write content")
                return

            element = {
                "type": element_type,
                "content": content,
                "size": size,
                "color": color,
                "font": font_name,
                "align": alignment,
                "link": link_entry.get()
            }

            self.elements.append(element)
            self.render_element(element)
            editor.destroy()

        tk.Button(
            editor,
            text="Add",
            command=save_element,
            bg="#3a7ff6",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=20,
            pady=10
        ).pack(pady=30)

    def render_element(self, element):
        etype = element["type"]

        if etype == "heading":
            widget = tk.Label(
                self.preview_frame,
                text=element["content"],
                font=(element["font"], element["size"], "bold"),
                fg=element["color"],
                bg="white"
            )
            if element.get("link"):
                widget.configure(
                    command=lambda url=element['link']: self.open_link(url)
                )

            widget.pack(pady=15, anchor=element["align"])


        elif etype == "text":
            widget = tk.Label(
                self.preview_frame,
                text=element["content"],
                font=(element["font"], element["size"])
,
                fg=element["color"],
                bg="white",
                wraplength=700,
                justify="left"
            )
            widget.pack(pady=10, anchor=element["align"])


        elif etype == "button":
            widget = tk.Button(
                self.preview_frame,
                text=element["content"],
                font=(element["font"], element["size"])
,
                bg=element["color"],
                fg="white",
                relief="flat",
                padx=15,
                pady=10
            )
            widget.pack(pady=15, anchor=element["align"])


        elif etype == "image":
            placeholder = tk.Frame(
                self.preview_frame,
                width=300,
                height=180,
                bg="#d9d9d9"
            )
            placeholder.pack(pady=15, anchor=element["align"])
            placeholder.pack_propagate(False)

            tk.Label(
                placeholder,
                text=f"Image\n{element['content']}",
                bg="#d9d9d9",
                fg="#444",
                font=("Arial", 14)
            ).pack(expand=True)

        elif etype == "container":
            container = tk.Frame(
                self.preview_frame,
                bg="#f3f3f3",
                bd=2,
                relief="solid",
                padx=20,
                pady=20
            )
            container.pack(fill="x", padx=20, pady=15, anchor=element["align"])

            tk.Label(
                container,
                text="Container",
                bg="#f3f3f3",
                fg="#555",
                font=("Arial", 16, "bold")
            ).pack()

    def generate_html(self):
        html = """
<!DOCTYPE html>
<html lang=\"ru\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>Мой сайт</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    margin: 0;
    padding: 40px;
}
button {
    border: none;
    border-radius: 8px;
    cursor: pointer;
}
.section {
    background: #f3f3f3;
    padding: 25px;
    border-radius: 12px;
    margin: 20px 0;
}
</style>
</head>
<body>
<div class=\"container\">\n
"""

        for element in self.elements:
            etype = element["type"]
            content = element["content"]
            size = element["size"]
            font_name = element["font"]
            align = self.html_align_map[element["align"]]
            color = element["color"]

            if etype == "heading":
                html += f'<h1 style="font-size:{size}px;color:{color};font-family:{font_name};text-align:{align};">{content}</h1>\n'

            elif etype == "text":
                html += f'<p style="font-size:{size}px;color:{color};font-family:{font_name};text-align:{align};">{content}</p>\n'

            elif etype == "button":
                link = element.get("link", "")

                html += (
                    f'<div style="text-align:{align};">'
                    f'<a href="{link}" target="_blank">'
                    f'<button style="background:{color};padding:12px 20px;'
                    f'font-size:{size}px;color:white;font-family:{font_name};">{content}</button></a></div><br>\n'
                )

            elif etype == "image":
                html += (
                    f'<img src="{content}" alt="image" '
                    f'style="max-width:100%;border-radius:10px;margin:15px 0;">\n'
                )

            elif etype == "container":
                html += '<div class="section">Контейнерный блок</div>\n'

        html += """
</div>
</body>
</html>
"""

        return html

    def export_html(self):
        html = self.generate_html()

        pyperclip.copy(html)

        messagebox.showinfo(
            "Finished!",
            "HTML code was successfuly copied!"
        )

    def open_link(self, url):
        import webbrowser

        if url:
            webbrowser.open(url)

    def clear_site(self):
        self.elements.clear()

        for widget in self.preview_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteBuilder(root)
    root.mainloop()
