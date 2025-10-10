# ui/widgets/spinner.py
"""
Widget Spinner animé pour indiquer les opérations en cours
"""

import tkinter as tk
from ui.themes import theme_manager

class Spinner(tk.Canvas):
    """Widget spinner avec animation de rotation"""
    
    def __init__(self, parent, size=20, **kwargs):
        """
        Initialise le spinner
        
        Args:
            parent: Widget parent
            size: Taille du spinner en pixels (défaut: 20)
        """
        theme = theme_manager.get_theme()
        bg = kwargs.pop('bg', theme["bg"])
        
        super().__init__(parent, width=size, height=size, bg=bg, 
                        highlightthickness=0, **kwargs)
        
        self.size = size
        self.angle = 0
        self.is_spinning = False
        self.animation_id = None
        
        # Couleurs du thème
        self.color = theme.get("accent", "#3498db")
        self.bg_color = bg
        
        # Créer les éléments graphiques
        self._draw_spinner()
    
    def _draw_spinner(self):
        """Dessine le spinner (cercle avec un arc)"""
        # Effacer le canvas
        self.delete("all")
        
        # Définir les marges
        margin = 2
        
        # Dessiner un arc qui tourne
        self.create_arc(
            margin, margin,
            self.size - margin, self.size - margin,
            start=self.angle,
            extent=300,  # Arc de 300 degrés
            outline=self.color,
            width=2,
            style='arc'
        )
    
    def _animate(self):
        """Animation du spinner"""
        if self.is_spinning:
            # Incrémenter l'angle de rotation
            self.angle = (self.angle + 15) % 360
            
            # Redessiner
            self._draw_spinner()
            
            # Planifier la prochaine frame (60 FPS = ~16ms)
            self.animation_id = self.after(16, self._animate)
    
    def start(self):
        """Démarre l'animation du spinner"""
        if not self.is_spinning:
            self.is_spinning = True
            self._animate()
    
    def stop(self):
        """Arrête l'animation du spinner"""
        self.is_spinning = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        
        # Effacer le spinner
        self.delete("all")
    
    def update_theme(self):
        """Met à jour les couleurs selon le thème actuel"""
        theme = theme_manager.get_theme()
        self.color = theme.get("accent", "#3498db")
        self.bg_color = theme["bg"]
        self.configure(bg=self.bg_color)
        if self.is_spinning:
            self._draw_spinner()

