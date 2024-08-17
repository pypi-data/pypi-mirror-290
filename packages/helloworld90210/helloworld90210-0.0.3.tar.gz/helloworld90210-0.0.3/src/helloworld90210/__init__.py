#make sure pythonet is installed, if not you can install in CMD with:
#pip install pythonnet
"""
SMD PYTHON API BY ARUN MICROELECTRONICS
--------------------------------------

DESCRIPTION OF SMD3 FUNCTIONS
-----------------------------
"""


class SMD3:
    def Mode(self):
        """Set or query the operating mode."""
        pass

    def JoystickMode(self):
        """Set or query the joystick operation mode. Choose between single step or continuous rotation."""
        pass

    def UseExternalEnable(self):
        """Set or query whether the external enable signal should be used."""
        pass

    def SensorSelect(self):
        """Select termperature sensor. Choose between a K-Type thermocouple or a PT100 RTD."""
        pass

    def MotorTemperature(self):
        """Query the motor temperature."""
        pass

    def RunCurrent(self):
        """Set or query the motor run current, in Amps."""
        pass

    def HoldCurrent(self):
        """Set or query the motor hold current, in Amps."""
        pass

    def PowerdownDelay(self):
        """Set or query the delay time between standstill occurring and the motor current being reduced from the acceleration current to the hold current, in milliseconds."""
        pass

    def CurrentReductionDelay(self):
        """Set or query the delay per current reduction step that occurs when run current is reduced to hold current, in milliseconds"""
        pass

    def Freewheel(self):
        """Set or query the freewheel mode. Set the option to use passive braking or freewheeling when the motor is in standby."""
        pass

    def Resolution(self):
        """Set or query the microstep resolution"""
        pass

    def BakeTemperature(self):
        """Set or query the bake temperature setpoint."""
        pass

    def LimitsEnable(self):
        """Set or query global enable of limits inputs."""
        pass

    def LimitPositiveEnable(self):
        """Set or query enable of the positive limit."""
        pass

    def LimitNegativeEnable(self):
        """Set or query enable of the negative limit."""
        pass

    def LimitPositivePolarity(self):
        """Set or query polarity of the positive limit."""
        pass

    def LimitNegativePolarity(self):
        """Set or query polarity of the negative limit."""
        pass

    def LimitsStopMode(self):
        """Set or query the stop mode, determines behaviour when a limit is triggered."""
        pass

    def Acceleration(self):
        """Set or query the motor acceleration, in Hz/s."""
        pass

    def Deceleration(self):
        """Set or query the motor deceleration, in Hz/s."""
        pass

    def StartFrequency(self):
        """Set or query the start frequency, in Hz."""
        pass

    def StopFrequency(self):
        """Set or query the stop frequency, in Hz."""
        pass

    def StepFrequency(self):
        """Set or query the target step frequency, in Hz."""
        pass

    def ActualStepFrequency(self):
        """query the actual step frequency, in Hz."""
        pass

    def ActualPosition(self):
        """Set or query the actual position, in steps. Argument range between [-8388608, +8388607] steps."""
        pass

    def StepEdge(self):
        """Set or query a value indicating whether a step occurs on both the rising and falling edges of the step input, or just the rising edge."""
        pass

    def StepInterpolation(self):
        """Set or query a value indicating whether the step input should be interpolated to 256 microsteps."""
        pass

    def Load(self):
        """Load saved configuration."""
        pass

    def Store(self):
        """Store configuration."""
        pass

    def Stop(self):
        """Command motor to stop moving according to the current profile."""
        pass

    def MicrostepTransition(self):
        """Set or query the full step / microstepping transition, in Hz."""
        pass

    def Clear(self):
        """Clear faults."""
        pass

    def Serial(self):
        """Query the serial number."""
        pass

    def ZerowaitTime(self):
        """Set or query the waiting time after ramping down to a stop before the next movement can start, in milliseconds."""
        pass

    def JoystickAutoSelect(self):
        """Set or query auto switching to joystick mode."""
        pass

    def Identify(self):
        """Set or query enable blinking of that status indicator to aid in identifying the SMD3 among others."""
        pass

    def MoveAbsolute(self):
        """Command to move the motor to an absolute position using the positioning mode.  Argument range between [-8388607, +8388607] steps."""
        pass

    def MoveRelative(self):
        """Command to move the motor to a relative position using the positioning mode. Argument range between [-8388607, +8388607] steps."""
        pass

    def MoveVelocity(self):
        """Command to move the motor using velocity mode.  Set "+" for positive direction or "-" for negative direction."""
        pass

    def EmergencyStop(self):
        """Command stops immediately and disables the motor."""
        pass

    def AccelerationCurrent(self):
        """Set or query the motor acceleration/deceleration current."""
        pass

    def RelativePosition(self):
        """Set or query the relative position, in steps. Argument range between [-8388608, +8388607] steps."""
        pass

    def StartBake(self):
        """Command to start the bake mode."""
        pass

    def StartHome(self):
        """Command to start the home procedure. Set "+" for positive direction or "-" for negative direction."""
        pass

    def QuickStop(self):
        """Command motor to stop the motion in 1 second."""
        pass

    def LimitsPolarity(self):
        """Set the polarity for both positve and negative limits."""
        pass

    def FactoryReset(self):
        """Load factory defaults."""
        pass

    def FirmwareVersion(self):
        """Query the firmware version number."""
        pass

    def Flag(self):
        """Get the error or status flags."""
        pass

    def EmulatedValueDefault(self):
        """Emulated value."""
        pass

    def TemperatureSensorShorted(self):
        """Selected temperature sensor is short-circuited."""
        pass

    def TemperatureSensorOpen(self):
        """Selected temperature sensor is open circuit."""
        pass

    def MotorOverTemperature(self):
        """Selected temperature sensor is reporting temperature > 190 �C."""
        pass

    def MotorShort(self):
        """Motor phase to phase or phase to ground short has been detected."""
        pass

    def ExternalInhibit(self):
        """Motor disabled via external input."""
        pass

    def ConfigurationError(self):
        """Motor configuration is corrupted."""
        pass

    def JoystickConnected(self):
        """Joystick is connected."""
        pass

    def LimitNegative(self):
        """Limit negative input is active."""
        pass

    def LimitPositive(self):
        """Limit positive input is active"""
        pass

    def ExternalEnable(self):
        """External enable input state."""
        pass

    def IdentModeActive(self):
        """Ident mode is active."""
        pass

    def MotorStandby(self):
        """Motor stationary."""
        pass

    def BakeActive(self):
        """Bake mode running"""
        pass

    def TargetVelocityReached(self):
        """Set when the motor is at target velocity"""
        pass

    def Error(self):
        """Error flags"""
        pass

    def Status(self):
        """status flags"""
        pass

    def OperationParameters(self):
        """Device configuration options."""
        pass

    def ResponseFlag(self):
        """Error and status flags"""
        pass

    def PortIsOpen(self):
        """Get the value indicating the open or closed status of the serial port"""
        pass

    def PortName(self):
        """Get the name port used for the serial communication"""
        pass

    def PortBaud(self):
        """Get the serial baud rate"""
        pass

    def Connect(self):
        """Connect in emulation mode"""
        pass

    def Disconnect(self):
        """Close serial port"""
        pass

    def StepDir(self):
        """Step and direction."""
        pass

    def StepDirTrigg(self):
        """Step and direction triggered velocity."""
        pass

    def Remote(self):
        """USB remote control."""
        pass

    def Joystick(self):
        """Joystick."""
        pass

    def Bake(self):
        """Bake."""
        pass

    def Home(self):
        """Home."""
        pass

    def Jsmode(self):
        """Joystick operation mode."""
        pass

    def SingleStep(self):
        """Single step mode."""
        pass

    def Continuous(self):
        """Continuous mode."""
        pass

    def Tsel(self):
        """Temperature sensor."""
        pass

    def Thermocouple(self):
        """Thermocouple K type sensor."""
        pass

    def RTD(self):
        """RTD sensor."""
        pass

    def NormalOperation(self):
        """Normal operation."""
        pass

    def CoilShortedLS(self):
        """Phase shorted to ground."""
        pass

    def Res(self):
        """Motor microstep resolutions."""
        pass

    def MicroStep8(self):
        """Microstep resolution 8."""
        pass

    def MicroStep16(self):
        """Microstep resolution 16."""
        pass

    def MicroStep32(self):
        """Microstep resolution 32."""
        pass

    def MicroStep64(self):
        """Microstep resolution 64."""
        pass

    def MicroStep128(self):
        """Microstep resolution 128."""
        pass

    def MicroStep256(self):
        """Microstep resolution 256."""
        pass

    def Polarity(self):
        """Limits activation logic level"""
        pass

    def ActiveHigh(self):
        """Limit is active when logic level is high."""
        pass

    def ActiveLow(self):
        """Limit is active when logic level is low."""
        pass

    def StopMode(self):
        """Behaviour when a limit is triggered."""
        pass

    def HardStop(self):
        """The motor will stop immediately on a limit being triggered."""
        pass

    def SoftStop(self):
        """The motor decelerates according to the profile."""
        pass

    def Edge(self):
        """Edge of the step impulse"""
        pass

    def Rising(self):
        """A step occurs only on the rising edge."""
        pass

    def Both(self):
        """a step occurs on both rising and falling edges."""
        pass

    def Interp(self):
        """Step interpolation."""
        pass

    def Normal(self):
        """Each step input will cause one step at the current resolution."""
        pass

    def Interp256Microstep(self):
        """Each step input will be interpolated to 256 microsteps."""
        pass
"""
---------------------------------------------------------------------------------
DESCRIPTION OF SMD4 FUNCTIONS
---------------------------------------------------------------------------------
"""
class SMD4:
    def Batch(self):
        """Batch number"""
        pass

    def Serial(self):
        """Board serial number within batch"""
        pass


    def IsDefault(self):
        """Return true if the serial number matches the default pattern"""
        pass

    def Descriptor(self):
        """Gets an object representing a path to connecting the device"""
        pass

    def Connect(self):
        """Connect on the default connection which is USB"""
        pass

    def Text(self):
        """Specify text protocol"""
        pass

    def AutoProtocol(self):
        """Auto-detect the protocol. This will slow down the connection process as each protocol must be tested in turn"""
        pass

    def IpAddress(self):
        """Target IP address"""
        pass

    def TcpPortNumber(self):
        """Port number to use for TCP/IP. Leave null to auto-select based on protocol selection"""
        pass

    def Interface(self):
        """Interface type, for example USB or Ethernet"""
        pass

    def Protocol(self):
        """Protocol type, for example Text or Modbus"""
        pass

    def SerialNumber(self):
        """Target serial number"""
        pass

    def BaudRate(self):
        """Baud rate, applicable to serial interface only"""
        pass

    def PortName(self):
        """Com port name, for example "COM1" """
        pass

    def SlaveAddress(self):
        """Slave address. Only applicable to modbus over USB or Serial."""
        pass

    def TemperatureSensorShorted(self):
        """Selected temperature sensor is short-circuited"""
        pass

    def TemperatureSensorOpen(self):
        """Selected temperature sensor is open circuit"""
        pass

    def MotorOverTemperature(self):
        """Selected temperature sensor is reporting temperature > 190 �C."""
        pass

    def MotorShort(self):
        """Motor phase to phase or phase to ground short has been detected"""
        pass

    def ExternalInhibit(self):
        """Motor disabled via external input"""
        pass

    def EmergencyStop(self):
        """Motor disabled via software"""
        pass

    def ConfigurationError(self):
        """Motor configuration is corrupted"""
        pass

    def EncoderError(self):
        """Encoder Error"""
        pass

    def BoostUVLO(self):
        """Boost Error"""
        pass

    def JoystickConnected(self):
        """Joystick is connected"""
        pass

    def LimitNegative(self):
        """Limit negative input is active"""
        pass

    def LimitPositive(self):
        """Limit positive input is active"""
        pass

    def ExternalEnable(self):
        """External enable input state"""
        pass

    def IdentModeActive(self):
        """Ident mode is active"""
        pass

    def MotorStationary(self):
        """Motor stationary"""
        pass

    def BakeActive(self):
        """Bake mode running"""
        pass

    def TargetVelocityReached(self):
        """Set when the motor is at target velocity"""
        pass

    def EncoderPresent(self):
        """Encoder Present"""
        pass

    def BoostOperational(self):
        """Boost Operational"""
        pass

    def BoostDisableJumperFitted(self):
        """Boost disable jumper is fitted"""
        pass

    def JoystickPins(self):
        """Gets a value representing the state of the joystick pins at the microcontroller pins"""
        pass

    def SdelfioPins(self):
        """Gets a value representing the state of the step, direction, enable, limits and fault signals at the microcontroller pins"""
        pass

    def SdramTest(self):
        """Test the SDRAM, locks up the SMD4 for a few seconds while running."""
        pass

    def BoardSerialNumber(self):
        """Get or set the board serial number. This is the serial of the PCB assigned during production, and not normally visible to the customer. The customer sees the"""
        pass

    def ProductSerialNumber(self):
        """Get or set the product serial number. This is the serial the customer sees, as distinct from the"""
        pass

    def TemperatureFast(self):
        """Set a value indicating whether the normal temperature sensor averaging period should be overidden.
                Normally averaging period is about 10 seconds, this cuts that to nothing so that faults and temperature changes register immediately."""
        pass

    def Uuid(self):
        """Get or set the UUID."""
        pass

    def QspiFlashErase(self):
        """Erase QSPI flash."""
        pass

    def BoardTestPassFlag(self):
        """Gets or sets a flag recording board test pass fail status of the board"""
        pass

    def PostSoakTestPassFlag(self):
        """Gets or sets a flag recording post soak test pass fail status of the board"""
        pass

    def IntegrationTestPassFlag(self):
        """Gets or sets a flag recording integration test pass fail status of the board"""
        pass

    def ThermocoupleSampleInterval(self):
        """Gets or sets a value representing the thermocouple sample interval in ms. 
                The firmware always restores the default value on restart so the effect of this is temporary."""
        pass

    def StorePrivate(self):
        """Store private data that is either inaccessible or read only to the user, such as the serial number"""
        pass

    def Args(self):
        """Data returned, less the flags"""
        pass

    def ComsInterface(self):
        """Coms connection interface type"""
        pass

    def USB(self):
        """Connected via USB Port"""
        pass

    def COM(self):
        """Connected via COM Port"""
        pass

    def Ethernet(self):
        """Connected via Ethernet Port"""
        pass

    def JoystickMode(self):
        """Joystick operation mode"""
        pass

    def Single_Step(self):
        """Single step"""
        pass

    def Continuous(self):
        """Continuous"""
        pass

    def TemperatureSensorType(self):
        """Temperature sensor"""
        pass

    def Thermocouple(self):
        """K-Type Thermocouple"""
        pass

    def RTD(self):
        """PT100 RTD"""
        pass

    def Freewheel(self):
        """Freewheel mode"""
        pass

    def Normal_Operation(self):
        """Normal"""
        pass

    def CoilShortedLS(self):
        """Phase shorted to ground"""
        pass

    def MicrostepResolution(self):
        """Microstep resolution"""
        pass

    def MicroStep_8(self):
        """Microstep resolution 8"""
        pass

    def MicroStep_16(self):
        """Microstep resolution 16"""
        pass

    def MicroStep_32(self):
        """Microstep resolution 32"""
        pass

    def MicroStep_64(self):
        """Microstep resolution 64"""
        pass

    def MicroStep_128(self):
        """Microstep resolution 128"""
        pass

    def MicroStep_256(self):
        """Microstep resolution 256"""
        pass

    def SignalPolarity(self):
        """Limit input polarity"""
        pass

    def Active_High(self):
        """Limit is active when logic level is high"""
        pass

    def Active_Low(self):
        """Limit is active when logic level is low"""
        pass

    def LimitStopMode(self):
        """Behaviour when a limit is triggered"""
        pass

    def Hard_Stop(self):
        """The motor will stop immediately on a limit being triggered"""
        pass

    def Soft_Stop(self):
        """The motor decelerates according to the profile"""
        pass

    def StepDirectionEdge(self):
        """Edge on which a step occurs"""
        pass

    def Rising(self):
        """A step occurs only on the rising edge"""
        pass

    def Both(self):
        """a step occurs on both rising and falling edges"""
        pass

    def StepDirectionMode(self):
        """Step direction modes"""
        pass

    def Normal(self):
        """Text Protocol"""
        pass

    def Triggered(self):
        """Modbus RTU for serial or TCP for ethernet"""
        pass

    def SerialMode(self):
        """"""
        pass

    def RS232(self):
        """RS232 mode"""
        pass

    def RS485(self):
        """RS485 mode"""
        pass

    def StepInputInterpolationMode(self):
        """Step interpolation"""
        pass

    def Interp256Microstep(self):
        """Each step input is one full step, which is executed as 256 microsteps"""
        pass

    def Mode(self):
        """Operation mode"""
        pass

    def StepDir(self):
        """Step and direction."""
        pass

    def Remote(self):
        """USB remote control."""
        pass

    def Joystick(self):
        """Joystick."""
        pass

    def Bake(self):
        """Bake."""
        pass

    def Local(self):
        """Local."""
        pass

    def Soak(self):
        """Soak. Run a pre-configured test program used to exercise the product as part of production test"""
        pass

    def B4800(self):
        """A step occurs only on the rising edge."""
        pass

    def B9600(self):
        """A step occurs only on the rising edge."""
        pass

    def B14400(self):
        """A step occurs only on the rising edge."""
        pass

    def B19200(self):
        """A step occurs only on the rising edge."""
        pass

    def B38400(self):
        """A step occurs only on the rising edge."""
        pass

    def B57600(self):
        """A step occurs only on the rising edge."""
        pass

    def B115200(self):
        """A step occurs only on the rising edge."""
        pass

    def B230400(self):
        """A step occurs only on the rising edge."""
        pass

    def B460800(self):
        """A step occurs only on the rising edge."""
        pass

    def B921600(self):
        """A step occurs only on the rising edge."""
        pass

    def Direction(self):
        """Motor direction"""
        pass

    def ModbusFunctionCode(self):
        """Modbus function code"""
        pass

    def FC01(self):
        """Read Coil Status"""
        pass

    def FC02(self):
        """Read Input Status"""
        pass

    def FC03(self):
        """Read Holding Registers"""
        pass

    def FC04(self):
        """Read Input Registers"""
        pass

    def FC05(self):
        """Force Single Coil"""
        pass

    def FC06(self):
        """Preset Single Register"""
        pass

    def FC15(self):
        """Force Multiple Coils"""
        pass

    def FC16(self):
        """Preset Multiple Registers"""
        pass

    def ComsProtocol(self):
        """Device comunication Protocols"""
        pass

    def Modbus(self):
        """Modbus RTU for serial or TCP for ethernet"""
        pass

    def AutoDetect(self):
        """Unspecified, protocol will be auto-detected"""
        pass

    def ProfileItem(self):
        """Object defining a pair of values returned by the device when a profile parameter is requested.
                The user value is the value that the user set. The rear value is the same value after conversion by the device
                to the closest actual value that can be set."""
        pass

    def Disconnect(self):
        """Disconnect the device"""
        pass

    def Acceleration(self):
        """Gets or sets the acceleration, in Hz/s (steps per second per second)"""
        pass

    def AccelerationDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def AccelerationCurrent(self):
        """Gets or sets the motor current applied during acceleration or deceleration"""
        pass

    def ActualPosition(self):
        """Gets or sets the actual position in steps"""
        pass

    def ActualStepFrequency(self):
        """Get the live step frequency of the motor in Hz (steps per second)"""
        pass

    def BakeElapsed(self):
        """Gets the elapsed bake time."""
        pass

    def BakeTemperature(self):
        """Gets or sets the bake temperature setpoint"""
        pass

    def DelayPerCurrentReductionStep(self):
        """Gets or sets the delay in seconds per current reduction step that occurs when run current is reduced to hold current. 
                Non-zero values result in a smooth reduction in current which reduces the chance of a jerk upon power down.       
                The range is 0 to 0.328 seconds, with a resolution of 4 bits or approx. 20 ms. 
                Current setting has a resolution of 5 bits, or 32 steps, and consequently the current reduction process will only have
                as many steps as exist between the configured run and hold current.
                See also"""
        pass

    def Deceleration(self):
        """Gets or sets the deceleration, in Hz/s (steps per second per second)"""
        pass

    def DecelerationDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def FirmwareVersion(self):
        """Get the firmware version string"""
        pass

    def Flags(self):
        """Gets the device flags, indicating useful status and error conditions"""
        pass

    def HoldCurrent(self):
        """Gets or sets the motor hold current.
                Set this as low as possible while still obtaining the required holding torque to minimise temperature rise.
                See also"""
        pass

    def Identify(self):
        """Gets or sets a value indicating whether the identify function is enabled.F
                When set to true, the green status light on the front of the product flashes.
                This can be used to help identify one device amongst several."""
        pass

    def JoystickAutoSelect(self):
        """Gets or sets the joystick auto select function. When set to true, the product switches to joystick mode automatically when connecting a joystick."""
        pass

    def LimitNegativeEnable(self):
        """Gets or sets the negative limit (corresponding to decrementing step counter) enable."""
        pass

    def LimitNegativePolarity(self):
        """Gets or sets the negative limit polarity"""
        pass

    def LimitPositiveEnable(self):
        """Gets or sets the positive limit (corresponding to incrementing step counter) enable."""
        pass

    def LimitPositivePolarity(self):
        """Gets or sets the negative limit polarity"""
        pass

    def LimitsEnable(self):
        """Gets or sets global limit enable state.
                If this setting is false, limits are disabled regardless of the state of any other limits configuration item.
                This does not affect other limits configuration settings, allowing limits to be configured as desired, then globally enabled or disabled if required."""
        pass

    def LimitsStopMode(self):
        """Gets or sets the limits stop mode, which determines behaviour on limit being triggered."""
        pass

    def TransitionToMicrostep(self):
        """Gets or sets the full step / microstepping transition. When frequency falls below this threshold (approximately), the motor
                switches from full step to the selected microstep resolution. The product determines the upper threshold automatically and
                applies hysteresis to avoid possible jitter between the two stepping modes. The upper threshold cannot be adjusted."""
        pass

    def TransitionToMicrostepDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def MotorTemperature(self):
        """Get the motor temperature in �C"""
        pass

    def PowerdownDelay(self):
        """Gets or sets the delay time in seconds between stand still occurring and the motor current being reduced from the acceleration current to the hold current.
                The range is 0 to 5.5 seconds, with approximately 8 bit / 20 ms resolution
                See also"""
        pass

    def RelativePosition(self):
        """Gets or sets the relative position counter in steps"""
        pass

    def Resolution(self):
        """Gets or sets the micro step resolution.Micro stepping is used to smooth motor movement 
                and reduce resonances. Full stepping is always used above a specified threshold step rate, see also"""
        pass

    def RunCurrent(self):
        """Gets or sets the motor run current. See also"""
        pass

    def MotorTemperatureSensorType(self):
        """Gets or sets the motor temperature sensor type"""
        pass

    def StartFrequency(self):
        """Get the start frequency in Hz. Must be set less than or equal to"""
        pass

    def StartFrequencyDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def StepEdge(self):
        """Gets or sets which edge(s) a step occurs on when in step direction mode"""
        pass

    def Uptime(self):
        """Gets the total operating time since last reset."""
        pass

    def SerialTermination(self):
        """Gets or sets a value indicating whether RS485 line termination should be used.If enabled, a 120 termination resistance is placed between the RS485 A and B pins."""
        pass

    def TurnaroundDelay(self):
        """Gets or sets a value in milliseconds specifying the delay to execute between receipt of a command from the host and the client (SMD4) sending the response. Applicable to RS485 mode only."""
        pass

    def StepFrequency(self):
        """Gets or sets the target step frequency in Hz, or steps per second. 
                This is the maximum speed the motor will be run at. The target frequency will only be reached 
                if there is enough time or distance to do so; if moving for a short time, for example, the 
                motor may only accelerate to some fraction of the target frequency before it is time to decelerate to a stop."""
        pass

    def StepFrequencyDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def StepInterpolation(self):
        """Gets or sets a value indicating whether the step input should be interpolated to 256 microsteps. Applicable in"""
        pass

    def StopFrequency(self):
        """Set the stop frequency in Hz. Must be greater than or equal to"""
        pass

    def StopFrequencyDetails(self):
        """Gets an object representing the configured property value and the actual property value as measured at the motor. Becuase the drive generates step frequencies
                by division of a reference clock, small errors can result between the configured value and the exact value that you get. This is most obvious when
                low step divisions/resoultions are used. The error is typically very small, less than 0.2 Hz with 256x microstepping. 
                If this is relevant to your application, then this command may be used to establish precise values."""
        pass

    def UseExternalEnable(self):
        """Gets or sets a value indicating whether the external enable signal should be respected.
                If not using the external enable and it remains disconnected, set to false"""
        pass

    def ZerowaitTime(self):
        """Gets or sets the waiting time after ramping down to a stop before the next movement or direction inversion can start.
                Can be used to avoid excess acceleration, e.g. from"""
        pass

    def BoostEnable(self):
        """Gets or sets a value indicating whether the boost supply should be enabled. The boost supply steps up the input voltage from 
                48 V to 67 V to maximise motor dynamic performance. Enable for best performance.
                Regardless of this setting, the boost supply is disabled when input voltage falls below 48 V, or the boost enable jumper is not fitted.  
                See"""
        pass

    def SerialComsMode(self):
        """Gets or sets the serial coms mode, either RS232 or RS485. Unplug from the host device before changing the mode"""
        pass

    def GetProtocol(self):
        """Gets the coms protocol being used on the current interface"""
        pass

    def EthernetLinkUp(self):
        """Gets a value indicating whether the ethernet interface link is up"""
        pass

    def DHCP(self):
        """Gets or sets a value indicating whether DHCP is enabled"""
        pass

    def IP(self):
        """Gets or sets the Ethernet IP Address"""
        pass

    def SubnetMask(self):
        """Gets or sets the Ethernet Netmask"""
        pass

    def Gateway(self):
        """Gets or sets the gateway address. When DHCP is enabled, the value read back will be the value assigned by 
                DHCP rather than any value you might have set. 
                Any value set however is retained, and will apply if DHCP is disabled at a later time."""
        pass

    def MAC(self):
        """Gets the Ethernet interface MAC address"""
        pass

    def JoystickIsConnected(self):
        """Gets a value indicating whether the joystick is connected.
                Note this wraps the"""
        pass

    def LimitNegativeInputActivate(self):
        """Gets a value indicating whether limit negative input is active.
                Note this wraps the"""
        pass

    def LimitPositiveInputActive(self):
        """Gets a value indicating whether limit positive input is active.
                Note this wraps the"""
        pass

    def ExternalEnableInputActive(self):
        """Gets a value indicating the external enable input state"""
        pass

    def MotorIsStationary(self):
        """Gets a value indicating whether the motor has come to a stop and is now stationary"""
        pass

    def BakeInProgress(self):
        """Gets a value indicating whether bake is in progress"""
        pass

    def TemperatureSensorShortCircuitError(self):
        """Gets a value indicating whether the motor temperature sensor is short circuited"""
        pass

    def TemperatureSensorOpenCircuitError(self):
        """Gets a value indicating whether the motor temperature sensor is open circuit"""
        pass

    def MotorOverTemperatureError(self):
        """Gets a value indicating whether the motor temperature has exceeded safe limits, and the motor has been disabled as a result"""
        pass

    def MotorShortCircuitError(self):
        """Gets a value indicating whether the motor is experiencing a short circuit error"""
        pass

    def ExternalInhibitDisablingDrive(self):
        """Gets a value indicating whether the drive is disabled on account of the external enable input"""
        pass

    def BoostUVLOError(self):
        """Gets a value indicating whether the boost circuit is disabled due to UVLO (Under-Voltage Lockout)
                This is set when input voltage falls significantly below 48 V, at which point the boost function is disabled automatically"""
        pass

    def IsEmergencyStopped(self):
        """Gets a value indicating whether the device is in emergency stop state"""
        pass

    def Clear(self):
        """Clear all error flags"""
        pass

    def FactoryReset(self):
        """Load factory default configuration. Run the"""
        pass

    def Load(self):
        """Load the last saved configuration"""
        pass

    def MoveClockwise(self):
        """Start continuous rotation clockwise. Step count increases"""
        pass

    def MoveCounterClockwise(self):
        """Start continuous rotation counter-clockwise. Step count decreases"""
        pass

    def QuickStop(self):
        """Decelerates the motor to a stop within 1 second, disregarding the current profile to do so"""
        pass

    def StartBake(self):
        """Start bake. Configure the bake temperature setpoint using"""
        pass

    def Stop(self):
        """Stop the motor, decelerating according to the current profile"""
        pass

    def Store(self):
        """Store the configuration so that it is preserved on power off"""
        pass

    def Reset(self):
        """Restart the board, equivelent to powering off and on again"""
        pass

    def ResetToBootloader(self):
        """Reset the board to the bootloader, preparing it for programming"""
        pass

"""
IMPORT API COMMANDS
---------------------------------------------------------------------------------

"""
import clr
clr.AddReference(r"C:\source\testdll\SMD3pythonAPI\SMD3 API py\helloworld90210\src\helloworld90210\SMD3API.dll") 
clr.AddReference(r"C:\source\testdll\SMD3pythonAPI\SMD3 API py\helloworld90210\src\helloworld90210\SMD4Api.dll")
clr.AddReference(r"C:\source\testdll\SMD3pythonAPI\SMD3 API py\helloworld90210\src\helloworld90210\EasyModbus.dll")

from Aml.Equipment.SMD4Api import SMD4 
from SMD3API import SMD3
from Aml.Equipment.SMD4Api.Protocol import *
"""
CREATE SMD3 AND SMD4 INSTANCES
---------------------------------------------------------------------------------
"""
smd3 = SMD3()
smd4 = SMD4()

