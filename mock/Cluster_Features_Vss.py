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
    ["Vehicle.Chassis.SteeringWheel.Angle", 0, [0, -15, -30, -15, 0, 15, 30, 15, 0]],
    ["Vehicle.Speed", 0.0, [0, 30.0, 50.0, 70.0, 100.0, 70.0, 50.0, 30.0, 0.0]],
    ["Vehicle.TripMeterReading", 0.0, [0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]],
    ["Vehicle.TraveledDistanceSinceStart", 0, [100,200, 300, 400, 500]],
    ["Vehicle.AverageSpeed", 0, [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]],
    ["Vehicle.Powertrain.TractionBattery.Range", 10000, [10000, 9000, 8000, 6000,]],
    ["Vehicle.Powertrain.Range", 5000, [5000, 4000, 3000, 2000]],
    ["Vehicle.Powertrain.TractionBattery.Charging.ChargeLimit", 0, [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
    ["Vehicle.Powertrain.Transmission.CurrentGear", 0, [1, 2, 3, 4, 5, 6, -5, -4, -3, -2, -1]],
    ["Vehicle.Powertrain.TractionBattery.AccumulatedConsumedEnergy", 100, [100, 90, 80, 50 ]],
]


# Define discrete signals (boolean values)
discrete_signals = [
    ["Vehicle.ADAS.TCS.IsEngaged", False],
    ["Vehicle.ADAS.ESC.IsEnabled", False],
    ["Vehicle.ADAS.ABS.IsEnabled",False],
    ["Vehicle.Cabin.Seat.Row1.DriverSide.Airbag.IsDeployed",True],
    ["Vehicle.Body.Lights.Fog.Front.IsOn", False],
    ["Vehicle.Cabin.Door.Row1.DriverSide.IsOpen",False],
    ["Vehicle.Body.Lights.DirectionIndicator.Left.IsDefect",True],
    ["Vehicle.Body.Lights.DirectionIndicator.Right.IsDefect",True],
    ["Vehicle.Body.Lights.Parking.IsDefect", True],
    ["Vehicle.Powertrain.Transmission.CurrentGear", True],
    ["Vehicle.Driver.IsEyesOnRoad",True],
    ["Vehicle.ADAS.DMS.IsWarning",False],    
    ["Vehicle.ADAS.DMS.IsError",False],
    ["Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling",False],
    ["Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling",True],  
    
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
                ClockTrigger(100),  # Runs every second
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
        		ClockTrigger(5),  # Runs every second
        		create_discrete_animation_action(
 				states,
 				duration=0.1,
 				repeat_mode=Repeat_Mode.REPEAT,
        		),
        	)
        ],
    )



mock_datapoint(
    path="Vehicle.Cabin.Infotainment.HMI.TirePressureUnit",
    initial_value="PSI",
    behaviors=[
        create_behavior(
            ClockTrigger(1), 
            action=create_set_action("PSI"),
        )
    ],
)
