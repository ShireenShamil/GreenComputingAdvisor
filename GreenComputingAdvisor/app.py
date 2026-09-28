from flask import Flask, render_template, request
from engine.inference_engine import infer, backward_chain
from engine.calculator import energy_metrics

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

@app.route("/backward-form")
def backward_form():
    return render_template("backward.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    form = request.form
    facts = {
        "device": form.get("device"),
        "daily_usage": form.get("daily_usage"),
        "power_mode": form.get("power_mode"),
        "performance_required": form.get("performance_required"),
        "idle_time": form.get("idle_time"),
        "sleep_mode": form.get("sleep_mode"),
        "device_left_on": form.get("device_left_on"),
        "battery_saver": form.get("battery_saver"),
        "workload": form.get("workload"),
        "peripherals_unused": form.get("peripherals_unused"),
        "brightness": form.get("brightness"),
        "environment_brightness": form.get("environment_brightness"),
        "display_timeout": form.get("display_timeout"),
        "multiple_monitors": form.get("multiple_monitors"),
        "extra_monitors_required": form.get("extra_monitors_required"),
        "refresh_rate": form.get("refresh_rate"),
        "gpu_power": form.get("gpu_power"),
        "cpu_utilization": form.get("cpu_utilization"),
        "gpu_utilization": form.get("gpu_utilization"),
        "dedicated_gpu_active": form.get("dedicated_gpu_active"),
        "temperature": form.get("temperature"),
        "cooling": form.get("cooling"),
        "hardware_old": form.get("hardware_old"),
        "energy_consumption": form.get("energy_consumption"),
        "overclocking": form.get("overclocking"),
        "storage": form.get("storage"),
        "frequent_access": form.get("frequent_access"),
        "ram": form.get("ram"),
        "swapping": form.get("swapping"),
        "unused_storage": form.get("unused_storage"),
        "duplicate_files": form.get("duplicate_files"),
        "model_size": form.get("model_size"),
        "efficiency_priority": form.get("efficiency_priority"),
        "mixed_precision": form.get("mixed_precision"),
        "inference_frequency": form.get("inference_frequency"),
        "training_frequency": form.get("training_frequency"),
        "pretrained_model": form.get("pretrained_model"),
        "dataset_size": form.get("dataset_size"),
        "accuracy_difference": form.get("accuracy_difference"),
        "smaller_model": form.get("smaller_model"),
        "server_utilization": form.get("server_utilization"),
        "server_count": form.get("server_count"),
        "cloud_idle": form.get("cloud_idle"),
        "workload_variable": form.get("workload_variable"),
        "fixed_resources": form.get("fixed_resources"),
        "renewable_region": form.get("renewable_region"),
        "latency_requirement": form.get("latency_requirement"),
        "workload_deferrable": form.get("workload_deferrable"),
        "low_carbon_period": form.get("low_carbon_period"),
    }

    results = infer(facts)
    try:
        power = float(form.get("power_watts", 0) or 0)
        hours = float(form.get("hours_numeric", 0) or 0)
        ci = float(form.get("carbon_intensity", 0) or 0)
    except ValueError:
        power = hours = ci = 0
    metrics = energy_metrics(power, hours, ci)

    penalty = sum(r["penalty"] for r in results)
    score = max(0, 100 - penalty)
    if score >= 80: label = "Excellent"
    elif score >= 60: label = "Good"
    elif score >= 40: label = "Moderate"
    else: label = "Poor"

    return render_template("results.html", results=results, metrics=metrics,
                           score=score, label=label, facts=facts)


@app.route("/backward", methods=["POST"])
def backward():
    form = request.form

    # Collect the same observations used by the
    # forward-chaining assessment.
    facts = {
        "idle_time": form.get("idle_time"),
        "sleep_mode": form.get("sleep_mode"),
        "power_mode": form.get("power_mode"),
        "daily_usage": form.get("daily_usage"),
        "performance_required": form.get("performance_required"),
        "workload": form.get("workload"),
        "battery_saver": form.get("battery_saver"),
        "brightness": form.get("brightness"),
        "environment_brightness": form.get(
            "environment_brightness"
        ),
    }

    # Remove fields that the user did not supply.
    facts = {
        key: value
        for key, value in facts.items()
        if value is not None and value != ""
    }

    goal = form.get("goal", "").strip()

    if not goal:
        return "Please select a goal.", 400

    result = backward_chain(goal, facts)

    return render_template(
        "backward_results.html",
        result=result,
        facts=facts
    )


if __name__ == "__main__":
    app.run(debug=True)
