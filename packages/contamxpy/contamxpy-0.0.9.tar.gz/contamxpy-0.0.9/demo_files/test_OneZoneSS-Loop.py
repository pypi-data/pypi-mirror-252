from contamxpy import cxLib
import cxResults as cxr
import os
import sys
from optparse import OptionParser
import numpy as np

g_dataIndex = 0

Pambt_data   = np.array([   101325,    101325,  101325,  101325,  101325,  101325])
WSambt_data  = np.array([      0.0,     7.397,     0.0,   7.397,     0.0,     0.0])
WDambt_data  = np.array([      0.0,     270.0,     0.0,    90.0,     0.0,     0.0])
MFambt_data  = np.array([0.0023254, 0.0023254,     0.0,     0.0,     0.0,     0.0])
Tambt_data   = np.array([   273.15,    293.15,  293.15,  293.15,  293.15,  293.15])
Tzone_data   = np.array([   283.15,    288.15,  293.15,  298.15,  290.15,  283.15])
#                      C        10         15       20       25       17       10

# ============================================================================ setWthCtmInit() =====
# Set the initial conditions for the SetAmbt API test.
# This function is set as a parameter to instantiation of cxLib
#   to be called by the contamxpy.prjDataReadyFcnP() in order to set 
#   ambient boundary conditions for steady-state initialization.
# NOTE: The parameter {cxl as cxLib} is passed through contamx-lib to 
#   contamxpy.prjDataReadyFcnP() which in turn passes it to this function
#   to distinguish the instance of cxLib to be used.
#


def setWthCtmInit( cxl ):
    cxl.setAmbtPressure(Pambt_data[g_dataIndex])          # Pa
    cxl.setAmbtTemperature(Tzone_data[g_dataIndex])       # K
    cxl.setAmbtWindSpeed(WSambt_data[g_dataIndex])        # m/s
    cxl.setAmbtWindDirection(WDambt_data[g_dataIndex])    # deg
    cxl.setAmbtMassFraction(0, MFambt_data[g_dataIndex])  # 0.0023254 kg/kg = 2800 mg/m3


# ===================================================================================== main() =====


def main():
    global g_dataIndex

    # ----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=PRJ filename\n")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                      help="define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    # ----- Process command line options -v
    verbose = options.verbose

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = PRJ file.")
        return
    else:
        # Get PRJ file name
        prjPath  = args[0]

    if ( not os.path.exists(prjPath) ):
        print("ERROR: PRJ file not found.")
        return

    msg_cmd = "Running test_OneZoneSS.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    nIts = Tzone_data.__len__()

    for i in range(nIts):
        print(f"\n===== Iteration: {g_dataIndex + 1} =====")

        # ----- Initialize contamx-lib object w/ wp_mode and cb_option.
        #      wp_mode = 0 => use wind pressure profiles, WTH and CTM files or associated API calls.
        #      cb_option = True => set callback function to get PRJ INFO from the ContamXState.
        myPrj = cxLib(prjPath, 0, True, setWthCtmInit)

        myPrj.setVerbosity(verbose)

        # ----------------------------------------------------------------
        # ------------------------------------ Initialize Simulation -----
        # ----------------------------------------------------------------
        # Returns 1 if not ok, else 0
        sim_not_ok = myPrj.setupSimulation(1)
        if (sim_not_ok > 0):
            print(f"ABORT - sim_not_ok Returned by setupSimulation() = {sim_not_ok}")
            print(" => invalid simulation parameters for co-simulation.")
            myPrj.endSimulation()
            return

        # ----- Get simulation run info
        dayStart = myPrj.getSimStartDate()
        dayEnd   = myPrj.getSimEndDate()
        secStart = myPrj.getSimStartTime()
        secEnd   = myPrj.getSimEndTime()
        tStep    = myPrj.getSimTimeStep()

        buildingVolume = 0.0
        for zone in myPrj.zones:
            buildingVolume += zone.volume
        buildingMass = 1.2041 * buildingVolume

        # ----- Calculate the simulation duration in seconds and total time steps
        simBegin = (dayStart - 1) * 86400 + secStart
        simEnd = (dayEnd - 1) * 86400 + secEnd
        if (simBegin <= simEnd):
            simDuration = simEnd - simBegin
        else:
            simDuration = 365 * 86400 - simEnd + simBegin
        numTimeSteps = 0
        if (simDuration != 0):
            numTimeSteps = int(simDuration / tStep)
            print(f"ABORT - PRJ settings => Transient simulation w/ {numTimeSteps} time steps.")
            return
        elif (verbose > 0):
            print("PRJ settings => Steady state simulation.")

        # ----- Get the current date/time after initial steady state simulation
        currentDate = myPrj.getCurrentDayOfYear()
        currentTime = myPrj.getCurrentTimeInSec()
        if verbose > 0:
            print(f"Sim days = {dayStart}:{dayEnd}")
            print(f"Sim times = {secStart}:{secEnd}")
            print(f"Sim time step = {tStep}")
            print(f"date = {currentDate} time = {currentTime}")

        # ----- Output SS results.
        cxr.printZoneMf(myPrj, currentDate, currentTime, myPrj.nZones, myPrj.nContaminants)
        cxr.writeAirflowRates(sys.stdout, True, myPrj, currentDate, currentTime)
        cxr.writeAirflowRates(sys.stdout, False, myPrj, currentDate, currentTime)

        # Calculate building Air Change Rate
        sumAbsFlows = 0.0
        for path in myPrj.paths:
            if path.envIndex > 0:
                flows = myPrj.getPathFlow(path.nr)
                netPathFlow = flows[0] + flows[1]
                sumAbsFlows += abs(netPathFlow)
        buildingAcr = 0.5 * 3600. * sumAbsFlows / buildingMass
        if verbose > 0:
            print(f"sumAbsFlows    = {sumAbsFlows:.4} kg/s")
            print(f"buildingVolume = {buildingVolume:.4} m3")
            print(f"buildingMass   = {buildingMass:.4} kg")
        print(f"buildingAcr    = {buildingAcr:.4} 1/h")

        if verbose > 0:
            print("Performed SS simulation.\n")
        myPrj.endSimulation()

        # ----- Increment index into data arrays
        g_dataIndex = g_dataIndex + 1

# --- End main() ---#


if __name__ == "__main__":
    main()
