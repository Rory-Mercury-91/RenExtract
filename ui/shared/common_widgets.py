# shared/common_widgets.py
# Widgets communs pour le générateur de traductions Ren'Py
# Extrait de translation_generator_interface.py

"""
Widgets réutilisables pour l'interface du générateur de traductions
- PlaceholderEntry : Entry avec texte placeholder
- create_themed_summary_entry : Entry lecture seule qui conserve les couleurs du thème
- ToolTip : info-bulle au survol
"""

import tkinter as tk


class ToolTip:
    """Info-bulle simple au survol d'un widget."""

    def __init__(self, widget, text="", delay_ms=400):
        self.widget = widget
        self.text = text or ""
        self.delay_ms = delay_ms
        self._tip_window = None
        self._after_id = None
        self.widget.bind("<Enter>", self._schedule, add="+")
        self.widget.bind("<Leave>", self._hide, add="+")
        self.widget.bind("<ButtonPress>", self._hide, add="+")

    def set_text(self, text: str):
        self.text = text or ""
        if self._tip_window and self.text:
            for child in self._tip_window.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(text=self.text)

    def _schedule(self, _event=None):
        self._cancel()
        if not self.text:
            return
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _cancel(self):
        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        self._after_id = None
        if self._tip_window or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 12
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
            self._tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tw.attributes("-topmost", True)
            label = tk.Label(
                tw,
                text=self.text,
                justify="left",
                background="#2b2b2b",
                foreground="#f0f0f0",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=8,
                pady=4,
            )
            label.pack()
        except Exception:
            self._tip_window = None

    def _hide(self, _event=None):
        self._cancel()
        if self._tip_window is not None:
            try:
                self._tip_window.destroy()
            except Exception:
                pass
            self._tip_window = None


def create_themed_summary_entry(parent, textvariable, theme, **kwargs):
    """
    Crée un Entry d'affichage non éditable qui conserve entry_bg/entry_fg.

    Sous Windows, state='readonly' force souvent un fond blanc illisible :
    on bloque plutôt la saisie tout en gardant le style du thème.
    """
    font = kwargs.pop("font", ("Segoe UI", 10))
    entry = tk.Entry(
        parent,
        textvariable=textvariable,
        font=font,
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        relief="solid",
        borderwidth=1,
        highlightthickness=0,
        **kwargs,
    )

    def _block_edit(_event=None):
        return "break"

    for sequence in (
        "<Key>",
        "<<Paste>>",
        "<Control-v>",
        "<Control-V>",
        "<Button-2>",
        "<Control-x>",
        "<Control-X>",
        "<BackSpace>",
        "<Delete>",
    ):
        entry.bind(sequence, _block_edit)

    return entry


class PlaceholderEntry(tk.Entry):
    """Entry avec placeholder text"""
    def __init__(self, master=None, placeholder="", placeholder_color='grey', **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg_color = self['fg']
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()
    
    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)
    
    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get_real_value(self):
        """Retourne la vraie valeur (vide si c'est le placeholder)"""
        value = self.get()
        return "" if value == self.placeholder else value
