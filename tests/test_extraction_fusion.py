import os
from pathlib import Path
from core.services.translation.text_extraction_results_business import TextExtractionResultsBusiness
from core.models.backup.unified_backup_manager import BackupType


def test_generate_extraction_append_to_textes_manquants(tmp_path, monkeypatch):
    tl_dir = tmp_path / 'tl'
    tl_dir.mkdir()
    existing = tl_dir / 'textes_manquants.rpy'
    existing.write_text('# existing content\n', encoding='utf-8')

    biz = TextExtractionResultsBusiness()

    # Préparer selected_texts
    selected_texts = {"Bonjour", "Au revoir"}

    output_path = str(tl_dir / 'textes_manquants.rpy')

    # Monkeypatch UI to auto-confirm
    monkeypatch.setattr('core.services.translation.text_extraction_results_business.show_translated_messagebox', lambda *a, **k: True)

    # Dummy backup manager
    calls = {}
    class DummyUBM:
        def create_backup(self, source_path, backup_type, description=None, **kwargs):
            calls['called'] = True
            calls['source_path'] = source_path
            calls['backup_type'] = backup_type
            return {'success': True, 'backup_path': '/tmp/fake_backup'}

    monkeypatch.setattr('core.services.translation.text_extraction_results_business.UnifiedBackupManager', lambda: DummyUBM())

    result = biz.generate_extraction_file(selected_texts, output_path, metadata={'Projet': 'Test'})
    assert result['success'] is True
    assert result['texts_count'] == 2
    content = existing.read_text(encoding='utf-8')
    assert '# === Fusion depuis' in content
    assert 'Bonjour' in content
    assert calls.get('called', False) is True
    assert calls.get('backup_type') == BackupType.BEFORE_FUSION


def test_generate_extraction_overwrite_other_file(tmp_path, monkeypatch):
    tl_dir = tmp_path / 'tl'
    tl_dir.mkdir()
    existing = tl_dir / 'user_modified.rpy'
    existing.write_text('# user content\n', encoding='utf-8')

    biz = TextExtractionResultsBusiness()
    selected_texts = {"Test1"}
    output_path = str(tl_dir / 'generated_file.rpy')

    # Monkeypatch UI to raise if called
    called = {'asked': False}
    def ask(*a, **kw):
        called['asked'] = True
        return True
    monkeypatch.setattr('core.services.translation.text_extraction_results_business.show_translated_messagebox', ask)

    result = biz.generate_extraction_file(selected_texts, output_path, metadata={'Projet': 'Test'})
    assert result['success'] is True
    assert Path(output_path).read_text(encoding='utf-8')
    assert called['asked'] is False
