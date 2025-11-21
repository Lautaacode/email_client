# main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from models.mail_server import MailServer
from models.message import Message
from models.folder import Folder


# ===================================================================
# APLICACIÓN PRINCIPAL
# ===================================================================
class MailClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Correo")
        self.root.geometry("1440x800")
        self.root.minsize(900, 500)

        self.server = MailServer("Server1")
        self.current_user = None

        self.start_frame = StartFrame(self)
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.main_frame = MainMailFrame(self)
        self.compose_frame = ComposeFrame(self)

        self.show_frame(self.start_frame)

    def show_frame(self, frame):
        for f in [
            self.start_frame,
            self.login_frame,
            self.register_frame,
            self.main_frame,
            self.compose_frame,
        ]:
            f.frame.pack_forget()

        # Mostrar el frame seleccionado
        frame.frame.pack(fill="both", expand=True)

        # Si se muestra el main y hay usuario logueado, refrescar su vista
        if frame is self.main_frame and self.current_user:
            self.main_frame.refresh_on_login()

    def logout(self):
        self.current_user = None
        self.show_frame(self.start_frame)


# ===================================================================
# BASE
# ===================================================================
class BaseFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.root)


# ===================================================================
# START
# ===================================================================
class StartFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app)
        ttk.Label(self.frame, text="Bienvenido", font=("Arial", 28)).pack(pady=40)

        ttk.Button(
            self.frame,
            text="Login",
            width=20,
            command=lambda: app.show_frame(app.login_frame),
        ).pack(pady=10)

        ttk.Button(
            self.frame,
            text="Registrar usuario",
            width=20,
            command=lambda: app.show_frame(app.register_frame),
        ).pack(pady=10)


# ===================================================================
# REGISTRO
# ===================================================================
class RegisterFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app)

        ttk.Label(self.frame, text="Registrar Usuario", font=("Arial", 20)).pack(
            pady=20
        )

        self.username = ttk.Entry(self.frame, width=30)
        self.username.pack(pady=5)
        self.username.insert(0, "Usuario")

        ttk.Button(self.frame, text="Crear", command=self.register).pack(pady=10)
        ttk.Button(
            self.frame,
            text="Volver",
            command=lambda: app.show_frame(app.start_frame),
        ).pack()

    def register(self):
        name = self.username.get().strip()
        if not name:
            messagebox.showerror("Error", "Ingrese un usuario válido.")
            return

        ok = self.app.server.register_user(name)

        if ok:
            messagebox.showinfo("Registro", f"Usuario '{name}' creado.")
            self.app.show_frame(self.app.start_frame)
        else:
            messagebox.showerror("Error", f"El usuario '{name}' ya existe.")


# ===================================================================
# LOGIN
# ===================================================================
class LoginFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app)

        ttk.Label(self.frame, text="Iniciar Sesión", font=("Arial", 20)).pack(
            pady=20
        )

        self.username = ttk.Entry(self.frame, width=30)
        self.username.pack(pady=5)
        self.username.insert(0, "Usuario")

        ttk.Button(self.frame, text="Ingresar", command=self.login).pack(pady=10)
        ttk.Button(
            self.frame,
            text="Volver",
            command=lambda: app.show_frame(app.start_frame),
        ).pack()

    def login(self):
        name = self.username.get().strip()
        user = self.app.server.users.get(name)

        if user:
            self.app.current_user = user
            # cuando hacemos login, reconstruimos árbol y filtros
            self.app.main_frame.refresh_on_login()
            self.app.show_frame(self.app.main_frame)
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")


# ===================================================================
# BANDEJA - ESTILO GMAIL (mejorada con árbol y filtros)
# ===================================================================
class MainMailFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app)

        container = ttk.Frame(self.frame)
        container.pack(fill="both", expand=True)

        # --------------------
        # SIDEBAR
        # --------------------
        sidebar = ttk.Frame(container, width=220)
        sidebar.pack(side="left", fill="y", padx=8, pady=8)

        ttk.Label(sidebar, text="📬 MiMail", font=("Arial", 16, "bold")).pack(
            pady=8
        )

        ttk.Button(
            sidebar,
            text="📥 Recibidos",
            width=20,
            command=lambda: self.change_folder("Inbox"),
        ).pack(pady=4)
        ttk.Button(
            sidebar,
            text="📤 Enviados",
            width=20,
            command=lambda: self.change_folder("Sent"),
        ).pack(pady=4)
        ttk.Button(
            sidebar,
            text="✉️ Redactar",
            width=20,
            command=lambda: app.show_frame(app.compose_frame),
        ).pack(pady=10)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=8)

        ttk.Button(sidebar, text="🔄 Refrescar", width=20, command=self.refresh_all).pack(
            pady=4
        )

        # --------------------
        # Árbol de carpetas (requisito)
        # --------------------
        ttk.Label(sidebar, text="Carpetas:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=6, pady=(10, 2)
        )
        self.folder_tree = ttk.Treeview(
            sidebar, show="tree", selectmode="browse", height=8
        )
        self.folder_tree.pack(fill="x", padx=6)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=8)

        # --------------------
        # Panel filtros automáticos (requisito)
        # --------------------
        ttk.Label(sidebar, text="Agregar filtro:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=6, pady=(6, 2)
        )
        filter_frame = ttk.Frame(sidebar)
        filter_frame.pack(fill="x", padx=6)

        ttk.Label(filter_frame, text="Palabra:").grid(row=0, column=0, sticky="w")
        self.filter_keyword_entry = ttk.Entry(filter_frame, width=20)
        self.filter_keyword_entry.grid(row=0, column=1, pady=2, sticky="w")

        ttk.Label(filter_frame, text="Carpeta destino:").grid(
            row=1, column=0, sticky="w"
        )
        self.filter_folder_entry = ttk.Entry(filter_frame, width=20)
        self.filter_folder_entry.grid(row=1, column=1, pady=2, sticky="w")

        ttk.Button(
            filter_frame,
            text="Agregar filtro",
            command=self.add_filter_from_gui,
            width=18,
        ).grid(row=2, column=0, columnspan=2, pady=6)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=8)

        # --------------------
        # Lista de filtros activos (solo visualización)
        # --------------------
        ttk.Label(sidebar, text="Filtros activos:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=6, pady=(4, 2)
        )
        self.filters_box = scrolledtext.ScrolledText(sidebar, height=6, width=28, state="disabled", wrap="word")
        self.filters_box.pack(padx=6, pady=(0, 8))

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=8)
        ttk.Button(sidebar, text="🚪 Cerrar sesión", width=20, command=app.logout).pack(
            side="bottom", pady=6
        )

        # --------------------
        # MAIN AREA
        # --------------------
        main_area = ttk.Frame(container)
        main_area.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # --------------------
        # HEADER + BUSQUEDA
        # --------------------
        header = ttk.Frame(main_area)
        header.pack(fill="x")

        ttk.Label(header, text="Bandeja", font=("Arial", 14, "bold")).pack(
            side="left", padx=10
        )
        ttk.Label(header, text="Buscar:", font=("Arial", 10)).pack(
            side="left", padx=(20, 4)
        )

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=10)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        # --------------------
        # SPLIT LISTA / DETALLE
        # --------------------
        split = ttk.Panedwindow(main_area, orient="horizontal")
        split.pack(fill="both", expand=True, pady=8)

        list_frame = ttk.Frame(split, width=700)
        split.add(list_frame, weight=5)

        columns = ("prio", "from", "subject")
        self.tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=22
        )

        self.tree.heading("prio", text="↑")
        self.tree.heading("from", text="De")
        self.tree.heading("subject", text="Asunto")

        self.tree.column("prio", width=50, anchor="center")
        self.tree.column("from", width=180)
        self.tree.column("subject", width=350)

        self.tree.pack(fill="both", expand=True, side="left")

        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_message)
        self.tree.bind("<Button-3>", self.on_right_click)

        # PANEL DE LECTURA (más chico)
        detail_frame = ttk.Frame(split, width=250)
        split.add(detail_frame, weight=2)

        self.meta_label = ttk.Label(
            detail_frame, text="Seleccione un mensaje", font=("Arial", 12, "bold")
        )
        self.meta_label.pack(anchor="w", padx=8, pady=8)

        self.body_text = scrolledtext.ScrolledText(detail_frame, wrap="word", height=8)
        self.body_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.body_text.configure(state="disabled")

        self.prio_btn = ttk.Button(
            detail_frame, text="Marcar Prioritario ↑", state="disabled", command=self.toggle_priority
        )
        self.prio_btn.pack(pady=6)

        # Estado
        self.current_folder = "Inbox"
        self.messages_cache = []
        self.selected_index = None

    # ---------------------
    # COMPORTAMIENTO
    # ---------------------
    def change_folder(self, folder):
        self.current_folder = folder
        self.refresh_list()
        self.clear_detail()

    def refresh_all(self):
        self.refresh_list()
        self.clear_detail()
        self.rebuild_folder_tree()
        self.rebuild_filters_display()

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        user = self.app.current_user
        if not user:
            return

        folder = user.inbox if self.current_folder == "Inbox" else user.sent
        msgs = folder.messages.copy()

        # Filtrado simple
        q = self.search_var.get().lower().strip()
        if q:
            msgs = [m for m in msgs if q in m.subject.lower() or q in m.sender.lower()]

        # Ordenar urgentes primero
        msgs = sorted(msgs, key=lambda m: not (m.is_urgent()))

        self.messages_cache = msgs

        for i, msg in enumerate(msgs):
            prio_icon = "↗" if msg.is_urgent() else ""
            self.tree.insert("", "end", iid=str(i), values=(prio_icon, msg.sender, msg.subject))

    def on_select_message(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        self.selected_index = idx
        self.show_detail(idx)

    def show_detail(self, idx):
        msg = self.messages_cache[idx]

        header = f"De: {msg.sender}    Para: {msg.receiver}"
        self.meta_label.config(text=header)

        self.body_text.configure(state="normal")
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert(tk.END, f"Asunto: {msg.subject}\n\n")
        self.body_text.insert(tk.END, msg.body)
        self.body_text.configure(state="disabled")

        self.prio_btn.configure(
            state="normal", text="Quitar Prioridad ↘" if msg.is_urgent() else "Marcar Prioritario ↑"
        )

    def clear_detail(self):
        self.selected_index = None
        self.meta_label.config(text="Seleccione un mensaje")
        self.body_text.configure(state="normal")
        self.body_text.delete("1.0", tk.END)
        self.body_text.configure(state="disabled")
        self.prio_btn.configure(state="disabled", text="Marcar Prioritario ↑")

    def toggle_priority(self):
        # Alterna prioridad usando la API pública de Message
        if self.selected_index is None:
            return
        msg = self.messages_cache[self.selected_index]
        msg.toggle_urgent()
        self.refresh_list()
        # re-seleccionar el mensaje (puede haber cambiado el orden)
        try:
            new_idx = self.messages_cache.index(msg)
            self.tree.selection_set(str(new_idx))
            self.show_detail(new_idx)
        except ValueError:
            self.clear_detail()

    # ---------------------
    # FUNCIONALIDAD: menú contextual para MOVER MENSAJE
    # ---------------------
    def on_right_click(self, event):
        # identificar la fila bajo el cursor
        rowid = self.tree.identify_row(event.y)
        if not rowid:
            return
        # seleccionar la fila
        self.tree.selection_set(rowid)
        idx = int(rowid)
        self.selected_index = idx

        menu = tk.Menu(self.tree, tearoff=0)
        menu.add_command(label="Mover a carpeta...", command=self.open_move_dialog)
        menu.add_command(label="Marcar/Quitar prioridad", command=self.toggle_priority)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_move_dialog(self):
        if self.selected_index is None:
            return

        user = self.app.current_user
        if not user:
            return

        # obtener lista de carpetas disponibles (nombres únicos)
        folders = self.get_all_folder_names(user)
        if not folders:
            messagebox.showinfo("Mover mensaje", "No hay carpetas disponibles.")
            return

        # diálogo simple
        dlg = tk.Toplevel(self.app.root)
        dlg.title("Mover mensaje")
        dlg.geometry("320x120")
        dlg.transient(self.app.root)
        dlg.grab_set()

        ttk.Label(dlg, text="Seleccionar carpeta destino:").pack(pady=(8, 6))

        folder_var = tk.StringVar(value=folders[0])
        folder_menu = ttk.OptionMenu(dlg, folder_var, folders[0], *folders)
        folder_menu.pack(pady=(0, 8))

        def do_move():
            target = folder_var.get().strip()
            if not target:
                messagebox.showerror("Error", "Seleccione una carpeta válida.")
                return

            msg = self.messages_cache[self.selected_index]
            subject = msg.subject

            # Si la carpeta destino no existe en el árbol del usuario, la creamos (esto es seguro)
            if user.get_folder(target) is None:
                user.root.add_folder(Folder(target))

            ok = user.move_message(subject, target)
            if ok:
                messagebox.showinfo("Mover", f"Mensaje '{subject}' movido a '{target}'.")
                dlg.destroy()
                # actualizar vista y árbol
                self.refresh_all()
            else:
                messagebox.showerror("Error", "No se pudo mover el mensaje.")
                dlg.destroy()

        ttk.Button(dlg, text="Mover", command=do_move).pack(pady=(4, 8))

    def get_all_folder_names(self, user):
        # recorre el árbol de carpetas y devuelve una lista de nombres
        names = []

        def recurse(folder):
            names.append(folder.name)
            for sub in folder.subfolders:
                recurse(sub)

        recurse(user.root)
        # quitar duplicados y devolver en orden
        seen = set()
        out = []
        for n in names:
            if n.lower() not in seen:
                out.append(n)
                seen.add(n.lower())
        return out

    # ---------------------
    # FUNCIONALIDAD: filtros desde GUI
    # ---------------------
    def add_filter_from_gui(self):
        user = self.app.current_user
        if not user:
            messagebox.showerror("Error", "No hay usuario logueado.")
            return

        keyword = self.filter_keyword_entry.get().strip()
        folder_name = self.filter_folder_entry.get().strip()

        if not keyword or not folder_name:
            messagebox.showerror("Error", "Ingrese palabra clave y carpeta destino.")
            return

        # Si la carpeta no existe, crearla en el árbol del usuario para que quede visible
        if user.get_folder(folder_name) is None:
            user.root.add_folder(Folder(folder_name))

        user.add_filter(keyword, folder_name)
        messagebox.showinfo("Filtro", f"Filtro agregado: '{keyword}' → '{folder_name}'")

        # Limpiar entradas y actualizar árbol y lista de filtros
        self.filter_keyword_entry.delete(0, tk.END)
        self.filter_folder_entry.delete(0, tk.END)
        self.rebuild_folder_tree()
        self.rebuild_filters_display()

    # ---------------------
    # FUNCIONALIDAD: mostrar árbol de carpetas en GUI (orden alfabético)
    # ---------------------
    def rebuild_folder_tree(self):
        # limpia y carga el Treeview de carpetas basado en user.root
        for row in self.folder_tree.get_children():
            self.folder_tree.delete(row)

        user = self.app.current_user
        if not user:
            # mostrar sólo root por defecto
            self.folder_tree.insert("", "end", "root", text="Root")
            return

        def add_node(parent_iid, folder):
            iid = f"{folder.name}_{id(folder)}"
            display = f"{folder.name} ({len(folder.messages)})"
            self.folder_tree.insert(parent_iid, "end", iid, text=display)
            # ordenar subcarpetas alfabéticamente por nombre para presentación limpia
            subs = sorted(folder.subfolders, key=lambda s: s.name.lower())
            for sub in subs:
                add_node(iid, sub)

        add_node("", user.root)
        # expandir el root
        for c in self.folder_tree.get_children(""):
            self.folder_tree.item(c, open=True)

    # ---------------------
    # Mostrar filtros activos
    # ---------------------
    def rebuild_filters_display(self):
        user = self.app.current_user
        self.filters_box.configure(state="normal")
        self.filters_box.delete("1.0", tk.END)
        if not user:
            self.filters_box.insert(tk.END, "(No hay usuario logueado)\n")
            self.filters_box.configure(state="disabled")
            return

        fl = user.list_filters()
        if not fl:
            self.filters_box.insert(tk.END, "(Sin filtros)\n")
        else:
            for k, folder in fl:
                self.filters_box.insert(tk.END, f"'{k}' → {folder}\n")
        self.filters_box.configure(state="disabled")

    # ---------------------
    # REFRESH cuando entramos
    # ---------------------
    def refresh_on_login(self):
        # llamado cuando el usuario hace login
        self.rebuild_folder_tree()
        self.rebuild_filters_display()
        self.refresh_all()


# ===================================================================
# REDACTAR
# ===================================================================
class ComposeFrame(BaseFrame):
    def __init__(self, app):
        super().__init__(app)

        ttk.Label(self.frame, text="Redactar", font=("Arial", 18)).pack(pady=8)

        form = ttk.Frame(self.frame)
        form.pack(padx=12, pady=6, fill="x")

        ttk.Label(form, text="Para:").grid(row=0, column=0, sticky="w")
        self.to_entry = ttk.Entry(form, width=60)
        self.to_entry.grid(row=0, column=1, pady=4)

        ttk.Label(form, text="Asunto:").grid(row=1, column=0, sticky="w")
        self.subject_entry = ttk.Entry(form, width=60)
        self.subject_entry.grid(row=1, column=1, pady=4)

        ttk.Label(form, text="Mensaje:").grid(row=2, column=0, sticky="nw")
        self.body_text = scrolledtext.ScrolledText(form, width=70, height=12)
        self.body_text.grid(row=2, column=1, pady=6)

        self.urgent_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form, text="Marcar como prioritario", variable=self.urgent_var
        ).grid(row=3, column=1, sticky="w", pady=6)

        btns = ttk.Frame(self.frame)
        btns.pack(pady=8)

        ttk.Button(btns, text="Enviar", command=self.send).pack(side="left", padx=6)
        ttk.Button(btns, text="Volver", command=lambda: app.show_frame(app.main_frame)).pack(
            side="left", padx=6
        )

    def reset_fields(self):
        self.to_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        self.urgent_var.set(False)

    def send(self):
        user = self.app.current_user
        if not user:
            messagebox.showerror("Error", "No hay usuario logueado.")
            return

        to = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        urgent = self.urgent_var.get()

        if not to or not subject:
            messagebox.showerror("Error", "Falta destinatario o asunto.")
            return

        # Crear mensaje y enviar
        ok = user.send(self.app.server, to, subject, body, urgent)

        if ok:
            messagebox.showinfo("OK", "Mensaje enviado.")
            # refrescar lista y árbol porque enviar agrega al Sent
            self.app.main_frame.refresh_all()
            self.app.show_frame(self.app.main_frame)
        else:
            # validación explícita si no se entregó
            messagebox.showerror("Error", "No se pudo entregar el mensaje. Verifique el destinatario.")
            # no cerramos la ventana para que el usuario corrija

# ===================================================================
# MAIN
# ===================================================================
def main():
    root = tk.Tk()
    MailClientGUI(root)
    root.iconbitmap("./utils/letter.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
