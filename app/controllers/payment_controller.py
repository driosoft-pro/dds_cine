from typing import Dict, List, Optional
from models.payment import Payment
from core.database import Database

class PaymentController:
    """Controlador para manejar operaciones relacionadas con pagos."""
    
    def __init__(self, db: Database):
        self.db = db
        self.payments_file = "payments.json"
    
    def create_payment(self, user_id: int, amount: float, payment_method: str, 
                        ticket_id: Optional[int] = None, 
                        reservation_id: Optional[int] = None) -> Dict:
        """Crea un nuevo pago."""
        payments = self.db.load_data(self.payments_file)
        payment_id = self.db.get_next_id(self.payments_file)
        
        new_payment = Payment(
            payment_id=payment_id,
            user_id=user_id,
            ticket_id=ticket_id,
            reservation_id=reservation_id,
            amount=amount,
            payment_method=payment_method
        )
        
        payments.append(new_payment.to_dict())
        self.db.save_data(self.payments_file, payments)
        return new_payment.to_dict()
    
    def get_payment_by_id(self, payment_id: int) -> Optional[Dict]:
        """Obtiene un pago por su ID."""
        payments = self.db.load_data(self.payments_file)
        for payment in payments:
            if payment['payment_id'] == payment_id:
                return payment
        return None
    
    def get_payments_by_user(self, user_id: int) -> List[Dict]:
        """Obtiene todos los pagos de un usuario."""
        payments = self.db.load_data(self.payments_file)
        return [p for p in payments if p['user_id'] == user_id and p['status'] == 'activo']
    
    def cancel_payment(self, payment_id: int) -> bool:
        """Cancela un pago (cambia su estado a inactivo)."""
        payments = self.db.load_data(self.payments_file)
        for i, payment in enumerate(payments):
            if payment['payment_id'] == payment_id:
                payments[i]['status'] = 'inactivo'
                self.db.save_data(self.payments_file, payments)
                return True
        return False
    
    def list_payments(self, active_only: bool = True) -> List[Dict]:
        """Lista todos los pagos."""
        payments = self.db.load_data(self.payments_file)
        if active_only:
            return [p for p in payments if p['status'] == 'activo']
        return payments