import json
import os
from datetime import datetime

class ProjectContext:
    def __init__(self, project_name="default"):
        self.project_name = project_name
        self.context_file = f"data/context_{project_name}.json"
        self._ensure_data_dir()
        self.context = self._load_context()
    
    def _ensure_data_dir(self):
        """Создание директории для данных"""
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_context(self):
        """Загрузка контекста"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._empty_context()
        return self._empty_context()
    
    def _empty_context(self):
        return {
            "project_name": self.project_name,
            "analyses": [],
            "notes": [],
            "music_analyses": [],
            "created": datetime.now().isoformat()
        }
    
    def _save_context(self):
        """Сохранение контекста"""
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, ensure_ascii=False, indent=2)
    
    def save_analysis(self, analysis):
        """Сохранение анализа кода"""
        self.context["analyses"].append(analysis)
        self._save_context()
    
    def save_music_analysis(self, analysis):
        """Сохранение музыкального анализа"""
        self.context["music_analyses"].append(analysis)
        self._save_context()
    
    def save_note(self, note_text):
        """Сохранение заметки"""
        note = {
            "timestamp": datetime.now().isoformat(),
            "content": note_text
        }
        self.context["notes"].append(note)
        self._save_context()
    
    def get_context(self):
        """Получение контекста"""
        return self.context
    
    def get_recent_analyses(self, limit=5):
        """Последние анализы"""
        return self.context["analyses"][-limit:] if self.context["analyses"] else []
    
    def get_recent_music_analyses(self, limit=5):
        """Последние музыкальные анализы"""
        return self.context["music_analyses"][-limit:] if self.context["music_analyses"] else []
