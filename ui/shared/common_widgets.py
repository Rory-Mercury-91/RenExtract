# shared/common_widgets.py
# Widgets communs pour le générateur de traductions Ren'Py
# Extrait de translation_generator_interface.py

"""
Widgets réutilisables pour l'interface du générateur de traductions
- PlaceholderEntry : Entry avec texte placeholder
- Autres widgets communs
"""

import tkinter as tk

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