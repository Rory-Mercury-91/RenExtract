import os
from pathlib import Path
from core.services.translation import translation_generation_business as tmod
from core.services.translation.translation_generation_business import TranslationGenerationBusiness
from core.models.backup.unified_backup_manager import BackupType


def test_safe_write_fusion_only_for_textes_manquants(tmp_path, monkeypatch):
    # Préparer le dossier temporaire et le fichier 'textes_manquants.rpy'
    tmpdir = tmp_path / "tl"
    tmpdir.mkdir()
    existing = tmpdir / 'textes_manquants.rpy'
    existing.write_text('# existing content\n', encoding='utf-8')

    # Cible générée qui n'existe pas encore
    target = tmpdir / '99_new_generated.rpy'

    # On ne doit PAS proposer de fusion via ce helper : il doit écrire normalement.
    biz = TranslationGenerationBusiness()
    # Rendre explicite qu'aucun backup ne doit être appelé en mode par défaut
    calls = {}
    class DummyBackupManager:
        def create_backup(self, source_path, backup_type, description=None, **kwargs):
            calls['called'] = True
            return {'success': True}

    biz.backup_manager = DummyBackupManager()

    # Appel à la méthode _safe_write_file (comportement par défaut : écriture simple)
    content = '# new lines\nline2\n'
    actual_path, msg = biz._safe_write_file(target, content)

    # Vérifications : écriture normale dans le fichier cible (pas de fusion)
    assert actual_path == target
    assert 'Écrit' in msg

    text = target.read_text(encoding='utf-8')
    assert 'line2' in text

    # Aucune backup n'a été demandée
    assert calls.get('called', False) is False


def test_safe_write_no_prompt_for_other_files(tmp_path, monkeypatch):
    # Si un autre fichier existe (ex: user_modified.rpy), on n'offre pas la fusion
    tmpdir = tmp_path / 'tl'
    tmpdir.mkdir()
    existing = tmpdir / 'user_modified.rpy'
    existing.write_text('# user changed\n', encoding='utf-8')

    target = tmpdir / '99_generated.rpy'

    # Monkeypatch pour détecter si messagebox est appelé (ne devrait pas l'être)
    called = {'asked': False}
    def ask(box_type, title, message, **kwargs):
        called['asked'] = True
        return True

    monkeypatch.setattr(tmod, 'show_translated_messagebox', ask)

    biz = TranslationGenerationBusiness()
    biz.backup_manager = None  # pas nécessaire pour ce test

    content = 'new content'
    actual_path, status = biz._safe_write_file(target, content)

    # Comme aucun 'textes_manquants.rpy' présent, on écrit normalement dans target
    assert actual_path == target
    assert target.read_text(encoding='utf-8') == content
    assert called['asked'] is False
