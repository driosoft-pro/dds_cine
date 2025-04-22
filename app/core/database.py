import json
import os
from typing import Dict, List, Any
from pathlib import Path

class Database:
    """Clase para manejar la persistencia de datos en archivos JSON."""
    
    def __init__(self, data_dir: str = "data"):
        """Inicializa la base de datos y crea el directorio si no existe."""
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_next_id(self, filename: str, id_field: str = "id") -> int:
        """Obtiene el próximo ID disponible para un archivo, basado en el campo de ID especificado."""
        data = self.load_data(filename)
        if not data:
            return 1
        return max((item.get(id_field, 0) for item in data)) + 1
    
    def load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Carga datos desde un archivo JSON."""
        filepath = Path(self.data_dir) / filename
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_data(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Guarda datos en un archivo JSON."""
        filepath = Path(self.data_dir) / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except (IOError, TypeError):
            return False
    
    def initialize_database(self, initial_data: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Inicializa la base de datos con datos iniciales."""
        try:
            for filename, data in initial_data.items():
                if not self.save_data(filename, data):
                    return False
            return True
        except Exception:
            return False