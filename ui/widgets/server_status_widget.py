# ui/widgets/server_status_widget.py
"""
Widget pour afficher l'état du serveur éditeur persistant
"""

import tkinter as tk
from tkinter import ttk
from infrastructure.helpers.server_utils import get_server_info, stop_server
from infrastructure.logging.logging import log_message


class ServerStatusWidget(ttk.LabelFrame):
    """Widget affichant l'état du serveur HTTP persistant"""
    
    def __init__(self, parent, port: int = 8765):
        super().__init__(parent, text="🚀 Serveur Éditeur Persistant", padding=10)
        self.port = port
        self._create_widgets()
        self.update_status()
    
    def _create_widgets(self):
        """Crée les widgets"""
        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Statut
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(status_frame, text="Statut:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = ttk.Label(
            status_frame, 
            text="Vérification...",
            font=('TkDefaultFont', 9, 'bold')
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Informations
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(
            info_frame,
            text="",
            font=('TkDefaultFont', 8),
            foreground='gray'
        )
        self.info_label.pack(side=tk.LEFT)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.refresh_btn = ttk.Button(
            button_frame,
            text="🔄 Actualiser",
            command=self.update_status,
            width=15
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️ Arrêter",
            command=self.stop_server,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Description
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill=tk.X, pady=(10, 0))
        
        desc_text = (
            "Le serveur permet aux boutons 'Ouvrir dans l'éditeur' des rapports HTML\n"
            "de fonctionner même après la fermeture de RenExtract. Il reste actif\n"
            "en arrière-plan et démarre automatiquement. 🔒 Localhost uniquement."
        )
        
        desc_label = ttk.Label(
            desc_frame,
            text=desc_text,
            font=('TkDefaultFont', 8),
            foreground='gray',
            justify=tk.LEFT
        )
        desc_label.pack(side=tk.LEFT)
    
    def update_status(self):
        """Met à jour l'affichage du statut"""
        try:
            info = get_server_info(self.port)
            
            if info['running']:
                self.status_label.config(
                    text="✅ Actif",
                    foreground='green'
                )
                
                info_text = f"Port: {info['port']}"
                if info['pid']:
                    info_text += f" • PID: {info['pid']}"
                if info['url']:
                    info_text += f" • {info['url']}"
                
                self.info_label.config(text=info_text)
                self.stop_btn.config(state=tk.NORMAL)
            else:
                self.status_label.config(
                    text="⏸️ Inactif",
                    foreground='orange'
                )
                self.info_label.config(
                    text="Le serveur démarrera automatiquement au prochain lancement"
                )
                self.stop_btn.config(state=tk.DISABLED)
        
        except Exception as e:
            log_message("ERREUR", f"Erreur mise à jour statut serveur: {e}", category="server_widget")
            self.status_label.config(
                text="❌ Erreur",
                foreground='red'
            )
            self.info_label.config(text=str(e))
            self.stop_btn.config(state=tk.DISABLED)
    
    def stop_server(self):
        """Arrête le serveur"""
        try:
            if stop_server(self.port):
                log_message("INFO", "Serveur arrêté par l'utilisateur", category="server_widget")
                # Rafraîchir après un court délai
                self.after(500, self.update_status)
            else:
                log_message("ATTENTION", "Impossible d'arrêter le serveur", category="server_widget")
        except Exception as e:
            log_message("ERREUR", f"Erreur arrêt serveur: {e}", category="server_widget")
        
        # Toujours rafraîchir l'affichage
        self.after(500, self.update_status)

