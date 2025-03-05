import datetime
from typing import Dict, NamedTuple, Optional, Tuple

class CollaborationInputs(NamedTuple):
    team_size: int
    avg_hourly_rate: float
    hours_per_week: int
    current_efficiency: float  # percentage as decimal (e.g., 0.75 for 75%)
    target_efficiency: float   # percentage as decimal (e.g., 0.85 for 85%)

class TechnicalDebtInputs(NamedTuple):
    maintenance_hours: int
    hourly_rate: float
    incident_count: int
    avg_incident_cost: float
    team_velocity: int        # story points per sprint
    potential_velocity: int   # estimated optimal story points per sprint
    sprint_length_weeks: int = 2

class DataQualityInputs(NamedTuple):
    records_processed: int
    error_rate: float        # percentage as decimal
    cost_per_error: float
    processing_time_hours: float
    hourly_operational_cost: float

def calculate_collaboration_roi(inputs: CollaborationInputs) -> Dict[str, float]:
    """
    Calculate ROI for improved team collaboration.
    
    Args:
        inputs: CollaborationInputs containing team metrics
        
    Returns:
        Dictionary containing:
        - annual_savings: Dollar amount saved per year
        - efficiency_gain: Percentage points improved
        - roi: Return on investment as percentage
        - payback_period_months: Months to recover investment
    """
    annual_hours = inputs.hours_per_week * 52
    current_cost = inputs.team_size * inputs.avg_hourly_rate * annual_hours
    
    current_output = current_cost * inputs.current_efficiency
    target_output = current_cost * inputs.target_efficiency
    
    annual_savings = target_output - current_output
    efficiency_gain = (inputs.target_efficiency - inputs.current_efficiency) * 100
    
    # Assuming implementation cost is 3 months of one team member's time
    implementation_cost = inputs.avg_hourly_rate * 480  # 3 months ≈ 480 hours
    roi = ((annual_savings - implementation_cost) / implementation_cost) * 100
    
    # Calculate payback period in months
    if annual_savings > 0:
        payback_period = (implementation_cost / annual_savings) * 12
    else:
        payback_period = float('inf')
    
    return {
        "annual_savings": round(annual_savings, 2),
        "efficiency_gain": round(efficiency_gain, 2),
        "roi": round(roi, 2),
        "payback_period_months": round(payback_period, 1)
    }

def calculate_technical_debt_cost(inputs: TechnicalDebtInputs) -> Dict[str, float]:
    """
    Calculate the cost of technical debt and potential savings.
    
    Args:
        inputs: TechnicalDebtInputs containing maintenance and incident metrics
        
    Returns:
        Dictionary containing:
        - annual_maintenance_cost: Yearly cost of maintenance
        - annual_incident_cost: Yearly cost of incidents
        - opportunity_cost: Cost of lost productivity
        - total_annual_cost: Total cost of technical debt
        - potential_savings: Estimated savings if debt is addressed
    """
    annual_maintenance_cost = inputs.maintenance_hours * inputs.hourly_rate * 52
    annual_incident_cost = inputs.incident_count * inputs.avg_incident_cost
    
    # Calculate opportunity cost based on velocity gap
    sprints_per_year = 52 / inputs.sprint_length_weeks
    velocity_gap = inputs.potential_velocity - inputs.team_velocity
    opportunity_cost = (velocity_gap * inputs.hourly_rate * 8 * inputs.sprint_length_weeks 
                       * sprints_per_year)
    
    total_annual_cost = (annual_maintenance_cost + annual_incident_cost + 
                        opportunity_cost)
    
    # Assume we can recover 70% of costs through debt reduction
    potential_savings = total_annual_cost * 0.7
    
    return {
        "annual_maintenance_cost": round(annual_maintenance_cost, 2),
        "annual_incident_cost": round(annual_incident_cost, 2),
        "opportunity_cost": round(opportunity_cost, 2),
        "total_annual_cost": round(total_annual_cost, 2),
        "potential_savings": round(potential_savings, 2)
    }

def calculate_data_quality_roi(inputs: DataQualityInputs) -> Dict[str, float]:
    """
    Calculate ROI for data quality improvements.
    
    Args:
        inputs: DataQualityInputs containing data quality metrics
        
    Returns:
        Dictionary containing:
        - current_error_cost: Current cost of errors
        - processing_cost: Cost of data processing
        - total_current_cost: Total cost of current operation
        - potential_savings: Potential savings with improved quality
        - roi: Return on investment percentage
    """
    error_count = inputs.records_processed * inputs.error_rate
    current_error_cost = error_count * inputs.cost_per_error
    
    processing_cost = inputs.processing_time_hours * inputs.hourly_operational_cost
    total_current_cost = current_error_cost + processing_cost
    
    # Assume we can reduce errors by 80% with improved quality
    potential_error_reduction = current_error_cost * 0.8
    
    # Assume implementation cost is 3 months of operational costs
    implementation_cost = processing_cost * 0.25  # 3 months = 0.25 years
    
    roi = ((potential_error_reduction - implementation_cost) / 
           implementation_cost) * 100
    
    return {
        "current_error_cost": round(current_error_cost, 2),
        "processing_cost": round(processing_cost, 2),
        "total_current_cost": round(total_current_cost, 2),
        "potential_savings": round(potential_error_reduction, 2),
        "roi": round(roi, 2)
    }

# Example usage
if __name__ == "__main__":
    # Collaboration ROI example
    collab_inputs = CollaborationInputs(
        team_size=5,
        avg_hourly_rate=75.0,
        hours_per_week=40,
        current_efficiency=0.65,
        target_efficiency=0.85
    )
    
    collab_roi = calculate_collaboration_roi(collab_inputs)
    print("Collaboration ROI:", collab_roi)
    
    # Technical Debt example
    debt_inputs = TechnicalDebtInputs(
        maintenance_hours=20,
        hourly_rate=75.0,
        incident_count=12,
        avg_incident_cost=5000.0,
        team_velocity=30,
        potential_velocity=45
    )
    
    debt_cost = calculate_technical_debt_cost(debt_inputs)
    print("Technical Debt Cost:", debt_cost)
    
    # Data Quality ROI example
    quality_inputs = DataQualityInputs(
        records_processed=1000000,
        error_rate=0.02,
        cost_per_error=25.0,
        processing_time_hours=160,
        hourly_operational_cost=100.0
    )
    
    quality_roi = calculate_data_quality_roi(quality_inputs)
    print("Data Quality ROI:", quality_roi)