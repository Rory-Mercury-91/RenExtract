import re
from infrastructure.logging.logging import log_message

class SimplePlaceholderGenerator:
    """Générateur corrigé pour patterns avec meilleure détection"""
    
    def __init__(self, pattern):
        # Convertir automatiquement les minuscules en majuscules pour les patterns alphanumériques
        self.original_pattern = self._normalize_pattern(pattern)
        self.counter = 1
        self.pattern_type = None
        self.format_info = {}
        
        self._analyze_pattern_fixed()
    
    def _normalize_pattern(self, pattern):
        """Normalise le pattern en convertissant les minuscules en majuscules pour les lettres"""
        try:
            # Pattern alphanumérique entre parenthèses : (c1) -> (C1)
            paren_match = re.match(r'^\(([a-z])(\d+)\)$', pattern)
            if paren_match:
                letter = paren_match.group(1).upper()  # Convertir en majuscule
                number = paren_match.group(2)
                normalized = f"({letter}{number})"
                log_message("DEBUG", f"Pattern normalisé: '{pattern}' -> '{normalized}'", category="placeholder_generator")
                return normalized
            
            # Pattern avec underscore et lettre : code_c1 -> code_C1
            underscore_match = re.match(r'^(.+)_([a-z])(\d+)$', pattern)
            if underscore_match:
                prefix = underscore_match.group(1)
                letter = underscore_match.group(2).upper()  # Convertir en majuscule
                number = underscore_match.group(3)
                normalized = f"{prefix}_{letter}{number}"
                log_message("DEBUG", f"Pattern normalisé: '{pattern}' -> '{normalized}'", category="placeholder_generator")
                return normalized
            
            # Pattern direct avec lettre : codec1 -> codeC1
            direct_match = re.match(r'^(.+)([a-z])(\d+)$', pattern)
            if direct_match:
                prefix = direct_match.group(1)
                letter = direct_match.group(2).upper()  # Convertir en majuscule
                number = direct_match.group(3)
                normalized = f"{prefix}{letter}{number}"
                log_message("DEBUG", f"Pattern normalisé: '{pattern}' -> '{normalized}'", category="placeholder_generator")
                return normalized
            
            # Aucune conversion nécessaire
            return pattern
            
        except Exception as e:
            log_message("DEBUG", f"Erreur normalisation pattern: {e}", category="placeholder_generator")
            return pattern
    
    def _analyze_pattern_fixed(self):
        """Analyse corrigée des patterns - gère (B01) et (C01) correctement"""
        try:
            # Pattern 1: Numérique avec underscore (RENPY_CODE_001, VAR_123, etc.)
            underscore_match = re.match(r'^(.+)_(\d+)$', self.original_pattern)
            if underscore_match:
                self.pattern_type = 'underscore_numeric'
                self.prefix = underscore_match.group(1)
                self.counter = int(underscore_match.group(2))
                self.format_info = {
                    'digits': len(underscore_match.group(2)),
                    'separator': '_'
                }
                log_message("DEBUG", f"Pattern underscore numérique: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}, digits={self.format_info['digits']}", category="placeholder_generator")
                return
            
            # Pattern 2: Alphanumérique entre parenthèses (B01), (C01), (A123), etc.
            alpha_paren_match = re.match(r'^\(([A-Z])(\d+)\)$', self.original_pattern)
            if alpha_paren_match:
                letter = alpha_paren_match.group(1)
                number_str = alpha_paren_match.group(2)
                self.pattern_type = 'alpha_numeric_paren'
                self.prefix = ""  # Pas de préfixe, tout est dans le pattern
                self.counter = int(number_str)
                self.format_info = {
                    'letter': letter,
                    'digits': len(number_str)
                }
                return
            
            # Pattern 3: Numérique avec tiret (VAR-123, CODE-01, etc.)
            dash_match = re.match(r'^(.+)-(\d+)$', self.original_pattern)
            if dash_match:
                self.pattern_type = 'dash_numeric'
                self.prefix = dash_match.group(1)
                self.counter = int(dash_match.group(2))
                self.format_info = {
                    'digits': len(dash_match.group(2)),
                    'separator': '-'
                }
                log_message("DEBUG", f"Pattern tiret numérique: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 4: Numérique avec parenthèses (CODE(01), VAR(123), etc.)
            paren_match = re.match(r'^(.+)\((\d+)\)$', self.original_pattern)
            if paren_match:
                self.pattern_type = 'paren_numeric'
                self.prefix = paren_match.group(1)
                self.counter = int(paren_match.group(2))
                self.format_info = {
                    'digits': len(paren_match.group(2))
                }
                log_message("DEBUG", f"Pattern parenthèses numérique: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 5: Juste des chiffres entre parenthèses ((01), (123), etc.)
            only_paren_match = re.match(r'^\((\d+)\)$', self.original_pattern)
            if only_paren_match:
                self.pattern_type = 'only_paren_numeric'
                self.prefix = ""
                self.counter = int(only_paren_match.group(1))
                self.format_info = {
                    'digits': len(only_paren_match.group(1))
                }
                return
            
            # Pattern 6: Numérique avec crochets (VAR[01], CODE[123], etc.)
            bracket_match = re.match(r'^(.+)\[(\d+)\]$', self.original_pattern)
            if bracket_match:
                self.pattern_type = 'bracket_numeric'
                self.prefix = bracket_match.group(1)
                self.counter = int(bracket_match.group(2))
                self.format_info = {
                    'digits': len(bracket_match.group(2))
                }
                log_message("DEBUG", f"Pattern crochets numérique: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 7: Numérique avec point (CODE.01, VAR.123, etc.)
            dot_match = re.match(r'^(.+)\.(\d+)$', self.original_pattern)
            if dot_match:
                self.pattern_type = 'dot_numeric'
                self.prefix = dot_match.group(1)
                self.counter = int(dot_match.group(2))
                self.format_info = {
                    'digits': len(dot_match.group(2))
                }
                log_message("DEBUG", f"Pattern point numérique: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 8: Numérique direct (CODE123, VAR01, etc.)
            direct_numeric_match = re.match(r'^([A-Za-z_]+)(\d+)$', self.original_pattern)
            if direct_numeric_match:
                self.pattern_type = 'direct_numeric'
                self.prefix = direct_numeric_match.group(1)
                self.counter = int(direct_numeric_match.group(2))
                self.format_info = {
                    'digits': len(direct_numeric_match.group(2))
                }
                log_message("DEBUG", f"Pattern numérique direct: '{self.original_pattern}' -> préfixe='{self.prefix}', compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 9: Alphabétique avec underscore (VAR_A, CODE_Z, etc.)
            alpha_underscore_match = re.match(r'^(.+)_([A-Z])$', self.original_pattern)
            if alpha_underscore_match:
                self.pattern_type = 'underscore_alpha'
                self.prefix = alpha_underscore_match.group(1)
                letter = alpha_underscore_match.group(2)
                self.counter = ord(letter) - ord('A') + 1
                self.format_info = {
                    'separator': '_'
                }
                log_message("DEBUG", f"Pattern alphabétique underscore: '{self.original_pattern}' -> préfixe='{self.prefix}', lettre={letter}, compteur={self.counter}", category="placeholder_generator")
                return
            
            # Pattern 10: Fallback - pas de pattern reconnu
            self.pattern_type = 'simple_prefix'
            self.prefix = self.original_pattern
            self.counter = 1
            self.format_info = {'digits': 3}
            log_message("DEBUG", f"Pattern simple (fallback): '{self.original_pattern}' -> utilisation comme préfixe", category="placeholder_generator")
            
        except Exception as e:
            log_message("ERREUR", f"Erreur analyse pattern '{self.original_pattern}': {e}", category="placeholder_generator")
            # Fallback sécurisé
            self.pattern_type = 'simple_prefix'
            self.prefix = self.original_pattern
            self.counter = 1
            self.format_info = {'digits': 3}

    def next_placeholder(self):
        """Génère le prochain placeholder selon le pattern détecté"""
        try:
            if self.pattern_type == 'underscore_numeric':
                # RENPY_CODE_001 -> RENPY_CODE_002
                digits = self.format_info['digits']
                result = f"{self.prefix}_{self.counter:0{digits}d}"
                
            elif self.pattern_type == 'alpha_numeric_paren':
                # (B01) -> (B02), (C01) -> (C02)
                letter = self.format_info['letter']
                digits = self.format_info['digits']
                result = f"({letter}{self.counter:0{digits}d})"
                
            elif self.pattern_type == 'dash_numeric':
                # VAR-01 -> VAR-02
                digits = self.format_info['digits']
                result = f"{self.prefix}-{self.counter:0{digits}d}"
                
            elif self.pattern_type == 'paren_numeric':
                # CODE(01) -> CODE(02)
                digits = self.format_info['digits']
                result = f"{self.prefix}({self.counter:0{digits}d})"
                
            elif self.pattern_type == 'only_paren_numeric':
                # (01) -> (02)
                digits = self.format_info['digits']
                result = f"({self.counter:0{digits}d})"
                
            elif self.pattern_type == 'bracket_numeric':
                # VAR[01] -> VAR[02]
                digits = self.format_info['digits']
                result = f"{self.prefix}[{self.counter:0{digits}d}]"
                
            elif self.pattern_type == 'dot_numeric':
                # CODE.01 -> CODE.02
                digits = self.format_info['digits']
                result = f"{self.prefix}.{self.counter:0{digits}d}"
                
            elif self.pattern_type == 'direct_numeric':
                # CODE01 -> CODE02
                digits = self.format_info['digits']
                result = f"{self.prefix}{self.counter:0{digits}d}"
                
            elif self.pattern_type == 'underscore_alpha':
                # VAR_A -> VAR_B
                if self.counter <= 26:
                    letter = chr(ord('A') + self.counter - 1)
                    result = f"{self.prefix}_{letter}"
                else:
                    # Après Z, passer en numérique
                    result = f"{self.prefix}_{self.counter}"
                    
            else:  # simple_prefix
                # CODE -> CODE_001
                digits = self.format_info['digits']
                result = f"{self.prefix}_{self.counter:0{digits}d}"
            
            self.counter += 1
            return result
            
        except Exception as e:
            log_message("ERREUR", f"Erreur génération placeholder: {e}", category="placeholder_generator")
            # Fallback sécurisé
            result = f"{self.prefix}_{self.counter:03d}"
            self.counter += 1
            return result

    def is_placeholder_from_this_generator(self, placeholder):
        """Vérifie si ce placeholder a été généré par ce générateur"""
        try:
            # Extraire le pattern de base et vérifier la correspondance
            pattern_info = self.get_pattern_info()
            if pattern_info['type'] == 'alpha_numeric_paren':
                letter = pattern_info.get('format_info', {}).get('letter', 'B')
                return bool(re.match(rf'^\({letter}\d+\)$', placeholder))
            elif pattern_info['type'] == 'underscore_numeric':
                prefix = pattern_info.get('prefix', '')
                return placeholder.startswith(f"{prefix}_") and re.match(rf'^{prefix}_\d+$', placeholder)
            # Ajouter d'autres types selon besoin
            return False
        except Exception:
            return False
    
    def get_pattern_info(self):
        """Retourne les informations sur le pattern détecté"""
        return {
            'original': self.original_pattern,
            'type': self.pattern_type,
            'prefix': getattr(self, 'prefix', ''),
            'current_counter': self.counter,
            'format_info': self.format_info
        }

# Test pour vérifier la correction
def test_renpy_patterns():
    """Teste spécifiquement les patterns RENPY"""
    test_patterns = [
        "RENPY_CODE_001",
        "RENPY_ASTERISK_001", 
        "RENPY_TILDE_001",
        "(01)",
        "(B1)",
        "CODE",
        "VAR_A"
    ]
    
    for pattern in test_patterns:
        generator = SimplePlaceholderGenerator(pattern)
        print(f"Pattern: {pattern}")
        for i in range(3):
            placeholder = generator.next_placeholder()
            print(f"  {i+1}: {placeholder}")
        print()

if __name__ == "__main__":
    test_renpy_patterns()