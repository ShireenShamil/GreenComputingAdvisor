from engine.inference_engine import infer


def ids(facts):
    return {x["id"] for x in infer(facts)}


def test_laptop_rules():
    facts = {
        "device": "laptop",
        "battery_saver": "disabled",
        "workload": "light",
        "idle_time": "high",
        "sleep_mode": "disabled",
        "brightness": "high",
        "environment_brightness": "medium",
    }
    result = ids(facts)
    assert {"R02", "R04", "R06"}.issubset(result)


def test_ml_rules():
    facts = {
        "workload": "deep_learning",
        "mixed_precision": "yes",
        "pretrained_model": "yes",
        "dataset_size": "small",
        "model_size": "large",
        "inference_frequency": "high",
        "accuracy_difference": "small",
        "smaller_model": "yes",
    }
    result = ids(facts)
    assert {"R21", "R22", "R24", "R25"}.issubset(result)


def test_high_power_desktop_saves_energy():
    facts = {
        "device": "desktop",
        "power_mode": "high",
        "performance_required": "no",
        "daily_usage": "long",
        "gpu_power": "high",
        "workload": "light",
        "gpu_utilization": "low",
        "dedicated_gpu_active": "yes",
        "brightness": "high",
        "environment_brightness": "low",
    }
    result = ids(facts)
    assert {"R01", "R10", "R12", "R06"}.issubset(result)


def test_cloud_idle_and_scheduling_rules():
    facts = {
        "server_utilization": "low",
        "server_count": "excess",
        "cloud_idle": "yes",
        "workload_variable": "yes",
        "fixed_resources": "yes",
        "workload_deferrable": "yes",
        "low_carbon_period": "yes",
        "renewable_region": "yes",
        "latency_requirement": "noncritical",
    }
    result = ids(facts)
    assert {"R26", "R27", "R28", "R30", "R29"}.issubset(result)


def test_storage_and_memory_inefficiency():
    facts = {
        "storage": "hdd",
        "frequent_access": "yes",
        "ram": "insufficient",
        "swapping": "high",
        "unused_storage": "yes",
        "duplicate_files": "high",
    }
    result = ids(facts)
    assert {"R16", "R17", "R18", "R19"}.issubset(result)


def test_oversized_model_and_transfer_learning():
    facts = {
        "workload": "machine_learning",
        "model_size": "large",
        "efficiency_priority": "high",
        "mixed_precision": "yes",
        "pretrained_model": "yes",
        "dataset_size": "small",
        "accuracy_difference": "small",
        "smaller_model": "yes",
    }
    result = ids(facts)
    assert {"R20", "R24", "R25"}.issubset(result)
