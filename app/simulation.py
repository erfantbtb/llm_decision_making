import numpy as np
import typing
from pydantic import BaseModel
from models.simulation_parameters import CarSimulationParameters


class MonteCarloSimulation:
    def __init__(self, params: CarSimulationParameters, num_simulations: int = 10000):
        self.params = params
        self.num_simulations = num_simulations

    def run(self) -> typing.Dict[str, float]:
        """
        Runs the Monte Carlo simulation for Buying vs Leasing.
        Returns a dictionary with average costs and probabilities.
        """
        years = self.params.duration_lease_months / 12
        
        # Simulate maintenance for the entire duration (sum of random yearly costs)
        # We assume maintenance costs are independent and identically distributed (i.i.d) per year
        maintenance_costs = np.random.normal(
            loc=self.params.estimated_maintenance_avg, 
            scale=self.params.maintenance_std_dev, 
            size=(self.num_simulations, int(years))
        )
        total_maintenance = np.sum(maintenance_costs, axis=1)

        # Mileage varies (assuming a standard deviation if not provided, or using fixed if 0)
        # Here we add a small variation (e.g., 5% or 1000 miles) to make it a true Monte Carlo simulation
        mileage_std_dev = 1000 
        simulated_annual_mileage = np.random.normal(
            loc=self.params.annual_mileage, 
            scale=mileage_std_dev, 
            size=self.num_simulations
        )

        # 2. Calculate Buy Costs
        # Total Buy = Purchase Price + Total Maintenance
        # (Note: Resale value is ignored here for simplicity, or could be added as a negative cost)
        total_buy_costs = self.params.purchase_price + total_maintenance

        # 3. Calculate Lease Costs
        # Total Lease = (Monthly Payment * Months) + Down Payment + Overage Charges
        base_lease_cost = (self.params.monthly_lease * self.params.duration_lease_months) + self.params.down_payment
        
        # Calculate overage miles (ensure no negative values)
        overage_miles = np.maximum(0, simulated_annual_mileage - self.params.lease_mileage_allowance)
        total_overage_cost = overage_miles * years * self.params.overage_charge_per_mile
        
        total_lease_costs = base_lease_cost + total_overage_cost

        # 4. Aggregate Results
        avg_buy_cost = np.mean(total_buy_costs)
        avg_lease_cost = np.mean(total_lease_costs)
        
        # Probability that Leasing is cheaper than Buying
        prob_lease_cheaper = np.mean(total_lease_costs < total_buy_costs)

        return {
            "avg_buy_cost": avg_buy_cost,
            "avg_lease_cost": avg_lease_cost,
            "prob_lease_cheaper": prob_lease_cheaper,
            "buy_cost_distribution": total_buy_costs.tolist(),
            "lease_cost_distribution": total_lease_costs.tolist()
        }