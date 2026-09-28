def energy_metrics(power_watts, hours_per_day, carbon_intensity=0):
    daily_kwh = (power_watts * hours_per_day) / 1000
    monthly_kwh = daily_kwh * 30
    annual_kwh = daily_kwh * 365
    # carbon_intensity is entered as kg CO2e per kWh
    daily_co2 = daily_kwh * carbon_intensity
    monthly_co2 = monthly_kwh * carbon_intensity
    return {
        "daily_kwh": round(daily_kwh, 2),
        "monthly_kwh": round(monthly_kwh, 2),
        "annual_kwh": round(annual_kwh, 2),
        "daily_co2": round(daily_co2, 2),
        "monthly_co2": round(monthly_co2, 2)
    }
