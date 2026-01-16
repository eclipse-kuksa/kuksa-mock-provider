import time

from lib.DiscreteAnimator import Repeat_Mode
from lib.animator import RepeatMode  
from lib.dsl import (
    create_animation_action,
    create_behavior,
    add_behavior,
    create_set_action,
    mock_datapoint,
    create_discrete_animation_action,
)
from lib.trigger import ClockTrigger


#import pdb; pdb.set_trace()
# Define continuous signals
continuous_signals = [
    #Battery Health Parameters
    ["Vehicle.Powertrain.TractionBattery.StateOfHealth", 0, [0, 10, 20, 30, 40, 50, 60, 70, 90, 100]],
    #Powertrain System Parameters
    ["Vehicle.Powertrain.ElectricMotor.Power", 0, [0, -15, -30, -15, 0, 15, 30, 15, 0]],
    ["Vehicle.Powertrain.ElectricMotor.Speed", 0, [2000, 3000, 4000, 5000, 6000, 7000, -500, -1000, -1500]],
    ["Vehicle.Powertrain.ElectricMotor.Torque", 0, [100, 200, 300, 400, 500, -50, -100, -200, -1250, -300]],
    ["Vehicle.Powertrain.ElectricMotor.Temperature", 0, [50, 60, 70, 80, 90, 100, -10, -20, -30, -40, -50, -70, -60]],
    #Charging System Parameters
    ["Vehicle.Powertrain.TractionBattery.Charging.Temperature", 0, [20, 25, 30, 35, 40]],
    ["Vehicle.Powertrain.TractionBattery.Charging.ChargeRate", 0, [10, 20, 30, 40, 50]],
    #Thermal Management System Parameters
    ["Vehicle.Powertrain.ElectricMotor.CoolantTemperature", 0, [30, 40, 50, 60, 70]],
    ["Vehicle.Cabin.HVAC.Station.Row1.Passenger.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row1.Driver.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row2.Passenger.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row2.Driver.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row3.Passenger.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row3.Driver.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row4.Passenger.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    ["Vehicle.Cabin.HVAC.Station.Row4.Driver.Temperature", 0, [16, 17, 18, 19, 20, 21, 22, 23, 24]],
    #Brake System Parameters
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.PadWear", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.FluidLevel", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.PadWear", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.FluidLevel", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.PadWear", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.FluidLevel", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.PadWear", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.FluidLevel", 0, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Powertrain.AccumulatedBrakingEnergy", 0, [100, 200, 300, 400, 500]],
    #TPMS
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure", 0, [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Temperature", 0, [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.Pressure", 0, [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.Temperature", 0, [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Tire.Pressure", 0, [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Tire.Temperature", 0, [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Tire.Pressure", 0, [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Tire.Temperature", 0, [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]],
]


# Define discrete signals (boolean values)
discrete_signals = [
    ["Vehicle.Powertrain.TractionBattery.Charging.IsCharging", False],
#    ["Vehicle.Powertrain.TractionBattery.Charging.IsChargingCableConnected", False],
    ["Vehicle.Powertrain.TractionBattery.Charging.IsDischarging",False],
    #Brake System Parameters
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.IsBrakesWorn", False],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Brake.IsFluidLevelLow", False],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.IsBrakesWorn", False],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Brake.IsFluidLevelLow", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.IsBrakesWorn", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Brake.IsFluidLevelLow", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.IsBrakesWorn", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Brake.IsFluidLevelLow", False],
    #TPMS
    ["Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.IsPressureLow", False],
    ["Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.IsPressureLow", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Left.Tire.IsPressureLow", False],
    ["Vehicle.Chassis.Axle.Row2.Wheel.Right.Tire.IsPressureLow", False],    
]

#for path, initial_value, values in continuous_signals:
#logger.debug(f"Initializing continuous signal: {path} with values: {values}")
for signal in continuous_signals:
    path, initial_value, values = signal
#    logger.debug(f"Initializing continuous signal: {path} with values: {values}")
    mock_datapoint(
        path,
        initial_value,
        [
            create_behavior(
                ClockTrigger(2),  # Runs every second
                create_animation_action(
                    duration=2.0,
                    repeat_mode=RepeatMode.REPEAT,
                    values=values,
                ),
            )
        ],
    )
    
    
states = [True, False]



for signal in discrete_signals:
    path, initial_value = signal
    mock_datapoint(
        path,
        initial_value,
        [
        	create_behavior(
        		ClockTrigger(1),  # Runs every second
        		create_discrete_animation_action(
 				states,
 				duration=0.1,
 				repeat_mode=Repeat_Mode.REPEAT,
        		),
        	)
        ],
    )

mock_datapoint(
    path="Vehicle.Powertrain.TractionBattery.Temperature.Max",
    initial_value=60,
    behaviors=[
        create_behavior(
            ClockTrigger(1), 
            action=create_set_action(60),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Powertrain.TractionBattery.Temperature.Min",
    initial_value= -20,
    behaviors=[
        create_behavior(
            ClockTrigger(1), 
            action=create_set_action(-20),
        )
    ],
)


mock_datapoint(
    path="Vehicle.Powertrain.TractionBattery.MaxVoltage",
    initial_value=4.2,
    behaviors=[
        create_behavior(
            ClockTrigger(1), 
            action=create_set_action(4.2),
        )
    ],
)

mock_datapoint(
    path="Vehicle.Powertrain.TractionBattery.Charging.TimeToComplete",
    initial_value=10980,
    behaviors=[
        create_behavior(
            ClockTrigger(1), 
            action=create_set_action(10980),
        )
    ],
)

