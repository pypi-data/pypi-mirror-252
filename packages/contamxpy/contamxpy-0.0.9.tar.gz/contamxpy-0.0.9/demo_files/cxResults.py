#! python3
import contamxpy as cxLib


def writeMfZones(file, header, cxl: cxLib, date, time, ctmNum):
    """Output zone mass fractions to text file."""
    nz = cxl.nZones
    if header is True:
        file.write("Day\tTime")
        for iz in range(nz):
            file.write(f"\t{cxl.zones[iz].name}")
        file.write("\n")
    else:
        file.write(f"{date}\t{time}")
        for iz in range(nz):
            MF = cxl.getZoneMassFraction(cxl.zones[iz].nr, ctmNum)
            file.write(f"\t{MF:.4}")
        file.write("\n")


def printZoneMf(cxl: cxLib, date, time, nz, nc):
    """Output zone mass fractions to stdout. """
    # cxl.zones[0-nZones-1], CONTAM => zones[1..nZones]
    # cxl.contaminants AND CONTAM contaminants[0..nContaminants-1]
    for z in range(nz):
        for c in range(nc):
            MF = cxl.getZoneMassFraction(cxl.zones[z].nr, c)
            print(f"Day {date}\tTime {time}\tZone {cxl.zones[z].nr}\t{cxl.contaminants[c]}\t{MF:.4} kg/kg")


def calcEnvExfil(cxl: cxLib, totalEnvExfil):
    """Calculate the total envelope exfiltration for each Contaminant. """
    nCtm = cxl.nContaminants
    for ic in range(nCtm):
        for path in cxl.envPaths:
            mass = cxl.getEnvelopeExfil(path.envIndex, ic)
            totalEnvExfil[ic] = totalEnvExfil[ic] + mass


def writeEnvExfil(file, header, cxl: cxLib, date, time, ctmNum):
    """Write envelope exfiltration for each envelope flow path to file."""
    if header is True:
        file.write("Day\tTime")
        for path in cxl.envPaths:
            file.write(f"\t{path.nr}")
        file.write("\tkg\n")
    else:
        file.write(f"{date}\t{time}")
        for path in cxl.envPaths:
            Mass = cxl.getEnvelopeExfil(path.envIndex, ctmNum)
            file.write(f"\t{Mass:.4}")
        file.write("\n")


def writeAirflowRates(file, header: bool, cxl: cxLib, date: int, time: int):
    """Write airflows to file."""
    # Paths, DuctsTerminals, and DuctLeaks.
    # Paths include simple AHS (Rec, OA, Exh).
    AHS_I = int("0x0070", 16)   # implicit (R|O|X) AHS paths
    AHS_S = int("0x0008", 16)   # system supply or return path
    AHS_R = int("0x0010", 16)   # recirculation flow path (R)
    AHS_O = int("0x0020", 16)   # outside air flow path (O)
    AHS_X = int("0x0040", 16)   # exhaust flow path (X)

    if header is True:
        file.write("Day\tTime")
        for path in cxl.paths:
            strHeader = f"p{path.nr}"
            if (path.flags & AHS_I):
                if (path.flags & AHS_R):
                    strHeader += f"_ahs-{path.ahs_nr}-Rec"
                elif (path.flags & AHS_O):
                    strHeader += f"_ahs-{path.ahs_nr}-OA"
                elif (path.flags & AHS_X):
                    strHeader += f"_ahs-{path.ahs_nr}-Exh"
            elif (path.flags & AHS_S):
                strHeader += f"_ahs-{path.ahs_nr}-SR"
            file.write(f"\t{strHeader}")
        for term in cxl.ductTerminals:
            file.write(f"\tt{term.nr}")
        for leak in cxl.ductLeaks:
            file.write(f"\tl{leak.nr}")
        file.write("\t\"Net flows kg/s\"\n")
    else:
        file.write(f"{date}\t{time}")
        for path in cxl.paths:
            flows = cxl.getPathFlow(path.nr)
            file.write(f"\t{(flows[0] + flows[1]):.4}")
        for it in range(cxl.nDuctTerminals):
            flow = cxl.getDuctTerminalFlow(it + 1)
            file.write(f"\t{flow:.4}")
        for il in range(cxl.nDuctLeaks):
            flow = cxl.getDuctLeakFlow(il + 1)
            file.write(f"\t{flow:.4}")
        file.write("\n")


def writeControls(file, header: bool, cxl: cxLib, date: int, time: int):
    nc = cxl.nOutputControls
    if header is True:
        file.write("Day\tTime")
        for control in cxl.outputControls:
            file.write(f"\t{control.name}")
        file.write("\n")
    else:
        file.write(f"{date}\t{time}")
        for i in range(nc):
            val = cxl.getOutputControlValue(i + 1)
            file.write(f"\t{val:.4}")
        file.write("\n")
