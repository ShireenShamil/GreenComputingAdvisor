def R(i, conditions, conclusion, recommendation, explanation, priority="Medium", penalty=5):
    return {
        "id": f"R{i:02d}", "conditions": conditions, "conclusion": conclusion,
        "recommendation": recommendation, "explanation": explanation,
        "priority": priority, "penalty": penalty
    }

RULES = [
R(1, {"daily_usage":"long","power_mode":"high","performance_required":"no"},
  "balanced_power_mode","Use a balanced power mode.",
  "The device is used for long periods in high-performance mode although maximum performance is not required.","High",10),

R(2, {"idle_time":"high","sleep_mode":"disabled"},
  "enable_sleep","Enable automatic sleep mode.",
  "Long idle periods with sleep disabled cause avoidable energy use.","High",10),

R(3, {"device_left_on":"yes","idle_time":"high"},
  "shutdown_when_unused","Shut down the device when it will remain unused.",
  "The system is left powered on during long periods of inactivity.","Medium",5),

R(4, {"device":"laptop","battery_saver":"disabled","workload":"light"},
  "enable_battery_saver","Enable battery saver for light workloads.",
  "A laptop performing light work usually does not need maximum-power operation.","Medium",5),

R(5, {"peripherals_unused":"yes"},
  "disconnect_peripherals","Disconnect or power down unused peripherals.",
  "Unused connected peripherals may continue drawing power.","Low",3),

R(6, {"brightness":"high","environment_brightness":["low","medium"]},
  "reduce_brightness","Reduce display brightness to a comfortable level.",
  "High brightness is unnecessary in a low or moderately lit environment.","Medium",5),

R(7, {"display_timeout":"long"},
  "shorter_timeout","Set a shorter display-off timeout.",
  "A long display timeout keeps the screen powered when it is not needed.","Medium",5),

R(8, {"multiple_monitors":"yes","extra_monitors_required":"no"},
  "disable_extra_monitors","Switch off unused additional monitors.",
  "Multiple active displays consume extra power when they are not required.","Medium",5),

R(9, {"refresh_rate":"high","workload":"office"},
  "lower_refresh_rate","Use a standard refresh rate for office work.",
  "A high refresh rate provides limited benefit for ordinary office workloads while increasing display/GPU activity.","Low",3),

R(10, {"gpu_power":"high","workload":"light"},
  "use_integrated_graphics","Prefer integrated or low-power graphics for light workloads.",
  "A high-power GPU is active for a workload that does not normally require it.","High",10),

R(11, {"cpu_utilization":"low","power_mode":"high"},
  "balanced_cpu","Use balanced CPU/power settings.",
  "CPU utilization is low while the machine remains in high-performance mode.","Medium",5),

R(12, {"gpu_utilization":"low","dedicated_gpu_active":"yes"},
  "power_saving_gpu","Use power-saving graphics when the dedicated GPU is not needed.",
  "The dedicated GPU is active despite low GPU utilization.","Medium",5),

R(13, {"temperature":"high","cooling":"inefficient"},
  "improve_cooling","Inspect airflow, dust, fan control and cooling efficiency.",
  "High operating temperature and inefficient cooling can increase fan power and reduce system efficiency.","High",10),

R(14, {"hardware_old":"yes","energy_consumption":"high"},
  "consider_upgrade","Consider an energy-efficient hardware upgrade when replacement is justified.",
  "Older hardware is reporting high energy consumption.","Medium",5),

R(15, {"overclocking":"enabled","performance_required":"no"},
  "disable_overclocking","Disable unnecessary overclocking.",
  "Overclocking is enabled although maximum performance is not required.","Medium",5),

R(16, {"storage":"hdd","frequent_access":"yes"},
  "consider_ssd","Consider an SSD when replacing frequently accessed storage.",
  "The workload frequently accesses an HDD; an appropriate SSD can improve performance per task and remove mechanical-drive power use.","Low",3),

R(17, {"ram":"insufficient","swapping":"high"},
  "increase_ram","Consider sufficient RAM to reduce excessive swapping.",
  "Insufficient memory is causing frequent storage swapping and additional I/O.","Medium",5),

R(18, {"unused_storage":"yes"},
  "disconnect_storage","Disconnect unused external storage when safe.",
  "Unused storage devices remain connected and may consume power.","Low",3),

R(19, {"duplicate_files":"high"},
  "clean_storage","Remove unnecessary duplicate data after verifying backups.",
  "Large amounts of duplicate data create avoidable storage demand.","Low",3),

R(20, {"workload":"machine_learning","model_size":"large","efficiency_priority":"high"},
  "model_compression","Evaluate model compression or a smaller architecture.",
  "A large ML model is being used where energy efficiency is a stated priority.","High",10),

R(21, {"workload":"deep_learning","mixed_precision":"yes"},
  "mixed_precision","Use supported mixed-precision computation after validating model quality.",
  "The deep-learning workload supports mixed precision, which can reduce computation and memory requirements on compatible hardware.","Medium",5),

R(22, {"inference_frequency":"high","model_size":"large"},
  "quantization","Evaluate post-training or quantization-aware quantization.",
  "A large model is used frequently for inference, so reducing numerical precision may lower resource requirements if quality remains acceptable.","Medium",5),

R(23, {"training_frequency":"high","gpu_power":"high"},
  "efficient_training","Reduce unnecessary retraining and schedule justified training efficiently.",
  "Frequent training is being performed on a high-power GPU.","High",10),

R(24, {"pretrained_model":"yes","dataset_size":"small","workload":["machine_learning","deep_learning"]},
  "transfer_learning","Evaluate transfer learning instead of training a large model from scratch.",
  "A pretrained model is available and the target dataset is small.","Medium",5),

R(25, {"accuracy_difference":"small","smaller_model":"yes","workload":["machine_learning","deep_learning"]},
  "smaller_model","Evaluate the smaller model and verify that its quality meets requirements.",
  "A smaller model is available with only a small stated accuracy difference.","High",10),

R(26, {"server_utilization":"low","server_count":"excess"},
  "server_consolidation","Evaluate safe server/workload consolidation.",
  "Server utilization is low while more servers than required are active.","High",10),

R(27, {"cloud_idle":"yes"},
  "terminate_idle_cloud","Stop or right-size idle cloud resources after checking dependencies.",
  "Idle cloud resources are provisioned and may consume unnecessary compute capacity.","High",10),

R(28, {"workload_variable":"yes","fixed_resources":"yes"},
  "autoscaling","Consider autoscaling or other demand-based resource allocation.",
  "The workload varies while resources remain fixed.","Medium",5),

R(29, {"renewable_region":"yes","latency_requirement":"noncritical"},
  "greener_region","Consider a lower-carbon region if compliance, cost and latency requirements allow.",
  "A potentially lower-carbon region is available and latency is not critical.","Medium",5),

R(30, {"workload_deferrable":"yes","low_carbon_period":"yes"},
  "carbon_aware_schedule","Schedule deferrable work for a lower-carbon period when operationally acceptable.",
  "The workload can be delayed and a lower-carbon execution period is available.","Medium",5),
]
