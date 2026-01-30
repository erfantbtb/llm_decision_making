from pydantic import BaseModel

class CarSimulationParameters(BaseModel):
    data_complete: bool 
    # Purchase Parameters
    purchase_price: float
    down_payment: float
    
    # Lease Parameters
    monthly_lease: float
    lease_mileage_allowance: int  # e.g., 12000 miles/year
    
    # Time and Usage
    duration_months: int
    annual_mileage: int  # e.g., 15000 miles/year
    
    # Costs and Variability
    estimated_maintenance_avg: float
    maintenance_std_dev: float
    overage_charge_per_mile: float  # e.g., 0.15 dollars/mile