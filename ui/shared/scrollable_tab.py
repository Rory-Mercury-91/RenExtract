# ui/shared/scrollable_tab.py
# Conteneur scrollable réutilisable pour onglets (barre visible seulement si contenu dépasse)

"""
Fournit un conteneur scrollable pour le contenu d'un onglet de notebook.
- Barre de défilement affichée uniquement si le contenu dépasse la zone visible
- Molette (Windows + Linux) sur toute la zone
- Utilisé par maintenance_tools, translation_generator et settings
"""

import tkinter as tk
from tkinter import ttk

from ui.themes import theme_manager


def make_scrollable_tab_container(parent):
    """
    Crée un conteneur scrollable pour le contenu d'un onglet.
    Retourne (wrapper_frame, inner_frame, bind_mousewheel_func).
    - wrapper_frame : à ajouter au notebook
    - inner_frame : frame intérieur où le contenu de l'onglet est construit (scrollable)
    - bind_mousewheel_func : à appeler après création du contenu pour que toute la zone réponde à la molette
    """
    theme = theme_manager.get_theme()
    wrapper = tk.Frame(parent, bg=theme["bg"])
    canvas = tk.Canvas(wrapper, bg=theme["bg"], highlightthickness=0)
    scrollbar_frame = tk.Frame(wrapper, bg='#666666', width=14)
    scrollbar_frame.pack_propagate(False)
    scrollbar = ttk.Scrollbar(scrollbar_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(fill='both', expand=True, padx=1, pady=1)
    canvas.pack(side='left', fill='both', expand=True)
    inner = tk.Frame(canvas, bg=theme["bg"])
    inner_id = canvas.create_window((0, 0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    def _update_scrollbar_visibility():
        canvas.update_idletasks()
        bbox = canvas.bbox('all')
        content_height = (bbox[3] - bbox[1]) if bbox else 0
        canvas_height = canvas.winfo_height()
        if content_height > canvas_height and canvas_height > 0:
            if not scrollbar_frame.winfo_ismapped():
                scrollbar_frame.pack(side='right', fill='y')
        else:
            if scrollbar_frame.winfo_ismapped():
                scrollbar_frame.pack_forget()
            canvas.yview_moveto(0)

    def _on_inner_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
        wrapper.after_idle(_update_scrollbar_visibility)

    inner.bind('<Configure>', _on_inner_configure)

    def _on_mousewheel(event):
        delta = getattr(event, 'delta', 0)
        if not delta:
            num = getattr(event, 'num', None)
            delta = 120 if num == 4 else -120 if num == 5 else 0
        if delta:
            canvas.yview_scroll(int(-1 * (delta / 120)), 'units')

    def _bind_mousewheel_recursive(widget):
        widget.bind('<MouseWheel>', _on_mousewheel, add='+')
        widget.bind('<Button-4>', _on_mousewheel, add='+')
        widget.bind('<Button-5>', _on_mousewheel, add='+')
        for child in widget.winfo_children():
            _bind_mousewheel_recursive(child)

    def _bind_mousewheel_now():
        canvas.bind('<MouseWheel>', _on_mousewheel, add='+')
        canvas.bind('<Button-4>', _on_mousewheel, add='+')
        canvas.bind('<Button-5>', _on_mousewheel, add='+')
        _bind_mousewheel_recursive(inner)

    def _on_canvas_configure(evt):
        if evt.width > 0:
            canvas.itemconfig(inner_id, width=evt.width)
        wrapper.after_idle(_update_scrollbar_visibility)

    canvas.bind('<Configure>', _on_canvas_configure)
    return wrapper, inner, _bind_mousewheel_now
