# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 00:37:20 2024
Creates CSV file with velocity values according to y-position and z-position for inlet with meshdata.
@author: Jose
"""
# Header definition.
hFormat="JMeshTDatas-200817"
hDataName="VelDir"
hDataUnits="[m/s]"
hDataType="float"
hData12="false"
Npt1=201
Npt2=81
Npt3=1
Npt=Npt1*Npt2*Npt3
PtRef=(0,0,0)
Vec1=(0,0.02,0)
Vec2=(0,0,0.02)
Vec3=(0,0,0)
DirDat=(1,0,0)

# Write CSV file.
file="MeshdataVel.csv"
with open(file,"w") as f:
    # Write header definition.
    f.write("Format;DataName;DataUnits;DataType;Data12;Npt1;Npt2;Npt3;PtRef.x [m];PtRef.y;PtRef.z;Vec1.x [m];Vec1.y;Vec1.z;Vec2.x;Vec2.y;Vec2.z;Vec3.x;Vec3.y;Vec3.z;DirDat.x;DirDat.y;DirDat.z\n")
    v=[hFormat]
    v=v+[hDataName]
    v=v+[hDataUnits]
    v=v+[hDataType]
    v=v+[hData12]
    v=v+[str(Npt1)]
    v=v+[str(Npt2)]
    v=v+[str(Npt3)]
    v=v+[str(x) for x in PtRef]
    v=v+[str(x) for x in Vec1]
    v=v+[str(x) for x in Vec2]
    v=v+[str(x) for x in Vec3]
    v=v+[str(x) for x in DirDat]
    f.write(";".join(v)+"\n")
    # Write data header.
    v=["time [s]"]+[f"v({v1}:{v2}:{v3})" for v3 in range(Npt3) for v2 in range(Npt2) for v1 in range(Npt1)]
    f.write(";".join(v)+"\n")
    
    # t=0.0 s, v=3 m/s
    v=[str(0.0)]+[str(3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")
    
    # t=0.5 s, v=3 m/s
    v=[str(0.5)]+[str(3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")
    
    # t=0.5001 s, v=0 m/s
    v=[str(0.5001)]+[str(0) for _ in range(Npt)]
    f.write(";".join(v)+"\n")
    
    # t=1.0 s, v=0 m/s
    v=[str(1.0)]+[str(0) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=1.5 s, v=2 m/s in selected area 0.66 <= y <= 1.34
    # ndiv=6
    # ny1=Npt1//ndiv;
    # ny2=int(2*Npt1/ndiv);
    ymin,ymax=0.66,1.34
    v1=[(2.0 if ymin<=(v1*max(Vec1))<=ymax else 0.0) for v3 in range(Npt3) for v2 in range(Npt2) for v1 in range(Npt1)]
    v=[str(1.5)]+[str(x) for x in v1]
    f.write(";".join(v)+"\n")

    # t=2.0 s, v=2 m/s in selected area 0.66 <= y <= 1.34
    v=[str(2.0)]+[str(x) for x in v1]
    f.write(";".join(v)+"\n")

    # t=2.5 s, v=2 m/s in selected area 0.66 <= y <= 1.34, v=6 m/s in selected area 2.68 <= y <= 3.34
    v2=[(6.0 if 2.68<=(v1*max(Vec1))<=3.34 else 0.0) for v3 in range(Npt3) for v2 in range(Npt2) for v1 in range(Npt1)]
    v=[str(2.5)]+[str(x+y) for x,y in zip(v1,v2)]
    f.write(";".join(v)+"\n")

    # t=3.5 s, v=2 m/s in selected area 0.66 <= y <= 1.34, v=6 m/s in selected area 2.68 <= y <= 3.34
    v=[str(3.5)]+[str(x+y) for x,y in zip(v1,v2)]
    f.write(";".join(v)+"\n")

    # t=4.0 s, v=2 m/s
    v=[str(4.0)]+[str(2) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=7.0 s, v=2 m/s
    v=[str(7.0)]+[str(2) for _ in range(Npt)]
    f.write(";".join(v)+"\n")
    
    # t=8.0 s, v=2 m/s according to the circle in pcen.
    pcen=2
    ra=0.5
    zmin=1
    vy=[v1*max(Vec1) for v3 in range(Npt3) for v2 in range(Npt2) for v1 in range(Npt1)]
    vz=[v2*max(Vec2) for v3 in range(Npt3) for v2 in range(Npt2) for v1 in range(Npt1)]
    v=[str(8.0)]+[str(2 if (y-pcen)**2+(z-zmin)**2<=ra*ra else 0) for y,z in zip(vy,vz)]
    f.write(";".join(v)+"\n")
    
    # t=8.5 s, v=5 m/s according to the circle in pcen.
    v=[str(8.5)]+[str(5 if (y-pcen)**2+(z-zmin)**2<=ra*ra else 0) for y,z in zip(vy,vz)]
    f.write(";".join(v)+"\n")

print(f"{file} file successfully created.")
