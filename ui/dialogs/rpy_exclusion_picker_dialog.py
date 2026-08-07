# ui/dialogs/rpy_exclusion_picker_dialog.py
# Modale de sélection des fichiers .rpy à exclure (checkboxes)

"""
Fenêtre modale pour sélectionner les fichiers .rpy à exclure
depuis le dossier langue du projet (cases à cocher).
"""

import tkinter as tk
from typing import List, Optional

from ui.themes import theme_manager
from infrastructure.logging.logging import log_message
from infrastructure.helpers.unified_functions import show_translated_messagebox
from ui.shared.project_utils import (
    list_language_rpy_files,
    parse_exclusions_string,
    exclusions_list_to_string,
)


class RpyExclusionPickerDialog:
    """Modale de sélection d'exclusions .rpy par cases à cocher."""

    def __init__(
        self,
        parent,
        project_path: str,
        language: str,
        current_exclusions: str = "",
        title: str = "Sélection des fichiers à exclure",
    ):
        self.parent = parent
        self.project_path = project_path
        self.language = language
        self.current_exclusions = current_exclusions or ""
        self.title = title
        self.theme = theme_manager.get_theme()
        self.result: Optional[str] = None
        self.window = None
        self.checkbox_vars = []  # List[Tuple[BooleanVar, file_dict]]
        self.select_all_var = tk.BooleanVar(value=False)
        self.filter_var = tk.StringVar(value="")
        self._file_rows = []  # widgets pour filtrage

    def show(self) -> Optional[str]:
        """
        Affiche la modale et retourne la chaîne d'exclusions (CSV)
        ou None si annulé.
        """
        files = list_language_rpy_files(self.project_path, self.language)
        if not files:
            show_translated_messagebox(
                "warning",
                "Aucun fichier .rpy",
                f"Aucun fichier .rpy trouvé dans le dossier langue « {self.language} ».\n\n"
                f"Vérifiez le projet et la langue sélectionnés.",
                parent=self.parent,
            )
            return None

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("640x520")
        self.window.minsize(480, 360)
        self.window.configure(bg=self.theme["bg"])
        self.window.transient(self.parent)
        self.window.grab_set()

        self._center_window()
        self._build_ui(files)
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.window.wait_window()
        return self.result

    def _center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def _build_ui(self, files: List[dict]):
        theme = self.theme
        selected = {name.lower() for name in parse_exclusions_string(self.current_exclusions)}

        header = tk.Frame(self.window, bg=theme["bg"])
        header.pack(fill="x", padx=16, pady=(16, 8))

        tk.Label(
            header,
            text=f"Dossier langue : {self.language}",
            font=("Segoe UI", 11, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            header,
            text="Cochez les fichiers .rpy à exclure, puis validez.\n"
                 "La zone « Rechercher » réduit la liste (ex. tapez common).",
            font=("Segoe UI", 9),
            bg=theme["bg"],
            fg=theme.get("fg", "#333333"),
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Barre outils : recherche + tout sélectionner
        tools = tk.Frame(self.window, bg=theme["bg"])
        tools.pack(fill="x", padx=16, pady=(4, 8))

        tk.Label(
            tools,
            text="Rechercher :",
            font=("Segoe UI", 9),
            bg=theme["bg"],
            fg=theme["fg"],
        ).pack(side="left")

        # Même style que les barres d'input du projet (évite blanc sur blanc)
        filter_entry = tk.Entry(
            tools,
            textvariable=self.filter_var,
            font=("Segoe UI", 9),
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            insertbackground=theme["entry_fg"],
            disabledbackground=theme["entry_bg"],
            disabledforeground=theme["entry_fg"],
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        filter_entry.pack(side="left", fill="x", expand=True, padx=(8, 12), ipady=3)
        filter_entry.bind("<KeyRelease>", lambda _e: self._apply_filter())

        select_all_cb = tk.Checkbutton(
            tools,
            text="Tout sélectionner",
            variable=self.select_all_var,
            command=self._toggle_select_all,
            font=("Segoe UI", 9),
            bg=theme["bg"],
            fg=theme["fg"],
            selectcolor=theme["entry_bg"],
            activebackground=theme["bg"],
            activeforeground=theme["fg"],
        )
        select_all_cb.pack(side="right")

        # Liste scrollable
        list_container = tk.Frame(self.window, bg=theme["bg"])
        list_container.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        canvas = tk.Canvas(list_container, bg=theme["entry_bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas, bg=theme["entry_bg"])

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_window = canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.window.bind("<Destroy>", lambda _e: canvas.unbind_all("<MouseWheel>"))

        self.checkbox_vars = []
        self._file_rows = []
        for file_info in files:
            row = tk.Frame(self.list_frame, bg=theme["entry_bg"])
            row.pack(fill="x", padx=8, pady=2)

            is_checked = (
                file_info["name"].lower() in selected
                or file_info["relative"].lower() in selected
            )
            var = tk.BooleanVar(value=is_checked)
            cb = tk.Checkbutton(
                row,
                text=file_info["relative"],
                variable=var,
                command=self._sync_select_all_state,
                font=("Segoe UI", 9),
                bg=theme["entry_bg"],
                fg=theme["entry_fg"],
                selectcolor=theme["entry_bg"],
                activebackground=theme["entry_bg"],
                activeforeground=theme["entry_fg"],
                anchor="w",
            )
            cb.pack(fill="x", anchor="w")

            self.checkbox_vars.append((var, file_info))
            self._file_rows.append((row, file_info["relative"].lower()))

        self._sync_select_all_state()

        # Compteur + boutons
        footer = tk.Frame(self.window, bg=theme["bg"])
        footer.pack(fill="x", padx=16, pady=(0, 16))

        self.count_label = tk.Label(
            footer,
            text="",
            font=("Segoe UI", 9),
            bg=theme["bg"],
            fg=theme.get("fg", "#CCCCCC"),
            anchor="w",
        )
        self.count_label.pack(side="left", fill="x", expand=True)
        self._update_count()

        # Mettre à jour le compteur à chaque changement
        for var, _info in self.checkbox_vars:
            var.trace_add("write", lambda *_args: self._update_count())

        tk.Button(
            footer,
            text="Annuler",
            command=self._on_cancel,
            bg=theme["button_tertiary_bg"],
            fg="#000000",
            font=("Segoe UI", 9),
            pady=4,
            padx=12,
            relief="flat",
            cursor="hand2",
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            footer,
            text="Valider",
            command=self._on_validate,
            bg=theme["button_primary_bg"],
            fg="#000000",
            font=("Segoe UI", 9, "bold"),
            pady=4,
            padx=16,
            relief="flat",
            cursor="hand2",
        ).pack(side="right")

    def _apply_filter(self):
        query = self.filter_var.get().strip().lower()
        for row, relative_lower in self._file_rows:
            if not query or query in relative_lower:
                row.pack(fill="x", padx=8, pady=2)
            else:
                row.pack_forget()

    def _toggle_select_all(self):
        checked = self.select_all_var.get()
        query = self.filter_var.get().strip().lower()
        for var, file_info in self.checkbox_vars:
            # Si un filtre est actif, n'agir que sur les lignes visibles
            if query and query not in file_info["relative"].lower():
                continue
            var.set(checked)
        self._update_count()

    def _sync_select_all_state(self):
        if not self.checkbox_vars:
            return
        all_checked = all(var.get() for var, _info in self.checkbox_vars)
        self.select_all_var.set(all_checked)
        self._update_count()

    def _update_count(self):
        if not hasattr(self, "count_label"):
            return
        selected_count = sum(1 for var, _info in self.checkbox_vars if var.get())
        total = len(self.checkbox_vars)
        self.count_label.config(text=f"{selected_count} / {total} fichier(s) exclus")

    def _on_validate(self):
        selected_names = [
            file_info["name"]
            for var, file_info in self.checkbox_vars
            if var.get()
        ]
        self.result = exclusions_list_to_string(selected_names)
        log_message(
            "INFO",
            f"Exclusions .rpy validées ({self.language}): {self.result or 'aucune'}",
            category="rpy_exclusion_picker",
        )
        self.window.destroy()

    def _on_cancel(self):
        self.result = None
        self.window.destroy()


def show_rpy_exclusion_picker(
    parent,
    project_path: str,
    language: str,
    current_exclusions: str = "",
    title: str = "Sélection des fichiers à exclure",
) -> Optional[str]:
    """
    Ouvre la modale de sélection d'exclusions .rpy.

    Returns:
        Chaîne CSV des fichiers exclus, ou None si annulé.
    """
    dialog = RpyExclusionPickerDialog(
        parent=parent,
        project_path=project_path,
        language=language,
        current_exclusions=current_exclusions,
        title=title,
    )
    return dialog.show()
