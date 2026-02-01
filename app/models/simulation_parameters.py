from pydantic import BaseModel

class CarSimulationParameters(BaseModel):
    data_complete: bool 
    purchase_price: float
    down_payment: float
    
    monthly_lease: float
    lease_mileage_allowance: int  
    
    duration_buy_months: int
    duration_lease_months: int 
    annual_mileage: int  
    
    estimated_maintenance_avg: float = 100.0
    maintenance_std_dev: float = 3.0
    overage_charge_per_mile: float = 1.5 
    
