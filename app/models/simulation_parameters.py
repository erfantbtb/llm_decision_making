from pydantic import BaseModel


class CarSimulationParameters(BaseModel):
    purchase_price: float
    monthly_lease: float
    duration_months: int
    estimated_maintenance_avg: float
    maintenance_std_dev: float 
    