from datetime import datetime
from typing import List, Dict, Optional
from core.database import Database
from controllers.movie_controller import MovieController
from controllers.user_controller import UserController

class ReportController:
    """Genera datos para los distintos reportes."""

    def __init__(self, db: Database):
        self.db = db
        self.movie_ctrl = MovieController(db)
        self.user_ctrl = UserController(db)

    def total_sales(
        self,
        start: Optional[datetime.date] = None,
        end:   Optional[datetime.date] = None
    ) -> float:
        """Suma todos los pagos entre start y end (inclusive)."""
        payments = self.db.load_data("payments.json")
        total = 0.0
        for p in payments:
            # suponemos p['date'] es algo como "2025-04-23T20:15:00"
            dt = datetime.fromisoformat(p["date"]).date()
            if (not start or dt >= start) and (not end or dt <= end):
                total += p.get("amount", 0)
        return total

    def sales_by_movie(
        self,
        start: Optional[datetime.date] = None,
        end:   Optional[datetime.date] = None
    ) -> List[Dict]:
        """
        Devuelve lista de dicts:
        [{'movie_id': X, 'title': '...', 'sales': 123.0}, ...]
        Incluye todas las películas (ventas=0 si no hay pagos).
        """
        payments = self.db.load_data("payments.json")
        tickets  = self.db.load_data("tickets.json")
        # ticket_id -> movie_id
        tid2mid = {t["ticket_id"]: t["movie_id"] for t in tickets}

        # Agregamos solo los que tengan pagos, pero luego
        # rellenaremos todos con zero
        agg: Dict[int,float] = {}
        for p in payments:
            try:
                dt = datetime.fromisoformat(p["date"]).date()
            except Exception:
                continue
            if (not start or dt >= start) and (not end or dt <= end):
                mid = tid2mid.get(p.get("ticket_id"))
                if mid:
                    agg[mid] = agg.get(mid, 0) + p.get("amount", 0)

        # Ahora recorremos todas las películas y asignamos 0 si no están en agg
        all_movies = self.movie_ctrl.list_movies(active_only=False)
        result: List[Dict] = []
        for m in all_movies:
            result.append({
                "movie_id": m["movie_id"],
                "title":    m.get("title", "N/D"),
                "sales":    agg.get(m["movie_id"], 0.0)
            })
        return result

    def sales_by_user(
        self,
        start: Optional[datetime.date] = None,
        end:   Optional[datetime.date] = None
    ) -> List[Dict]:
        """
        Devuelve lista de dicts:
        [{'user_id': U, 'username':'...', 'sales':123.0}, ...]
        Incluye todos los usuarios (ventas=0 si no hay pagos).
        """
        payments = self.db.load_data("payments.json")
        tickets  = self.db.load_data("tickets.json")
        # ticket_id -> user_id
        tid2uid = {t["ticket_id"]: t["user_id"] for t in tickets}

        agg: Dict[int,float] = {}
        for p in payments:
            try:
                dt = datetime.fromisoformat(p["date"]).date()
            except Exception:
                continue
            if (not start or dt >= start) and (not end or dt <= end):
                uid = tid2uid.get(p.get("ticket_id"))
                if uid:
                    agg[uid] = agg.get(uid, 0) + p.get("amount", 0)

        # Ahora listamos todos los usuarios y rellenamos con zero
        all_users = self.user_ctrl.list_users(active_only=False)
        result: List[Dict] = []
        for u in all_users:
            result.append({
                "user_id":  u["user_id"],
                "username": u.get("username", "N/D"),
                "sales":    agg.get(u["user_id"], 0.0)
            })
        return result

    def sales_by_user(
        self,
        start: Optional[datetime.date] = None,
        end:   Optional[datetime.date] = None
    ) -> List[Dict]:
        """
        Devuelve lista de dicts:
        [{'user_id': U, 'username':'...', 'sales':123.0}, ...]
        Incluye todos los usuarios (ventas=0 si no hay pagos en el rango).
        """
        payments = self.db.load_data("payments.json")
        tickets  = self.db.load_data("tickets.json")
        # Construye mapa ticket_id → user_id
        tid2uid = {t["ticket_id"]: t["user_id"] for t in tickets}

        # Agrega sólo los pagos en el rango
        agg: Dict[int,float] = {}
        for p in payments:
            try:
                dt = datetime.fromisoformat(p["date"]).date()
            except Exception:
                continue
            if (not start or dt >= start) and (not end or dt <= end):
                uid = tid2uid.get(p.get("ticket_id"))
                if uid:
                    agg[uid] = agg.get(uid, 0.0) + p.get("amount", 0.0)

        # Ahora recorre **todos** los usuarios, asignando 0 si no existe
        all_users = self.user_ctrl.list_users(active_only=False)
        result: List[Dict] = []
        for u in all_users:
            result.append({
                "user_id":  u["user_id"],
                "username": u.get("username", "N/D"),
                "sales":    agg.get(u["user_id"], 0.0)
            })
        return result
