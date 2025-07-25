# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 00:37:20 2024
Creates CSV file with ZSurf values according to y-position for inlet with meshdata.
@author: Jose
"""
import math as m
# Header definition.
hFormat="JMeshTDatas-200817"
hDataName="Zsurf"
hDataUnits="[m]"
hDataType="float"
hData12="false"
Npt1=81
Npt2=1
Npt3=1
Npt=Npt1*Npt2*Npt3
PtRef=(0,0,0)
Vec1=(0,0.05,0)
Vec2=(0,0,0)
Vec3=(0,0,0)
DirDat=(1,0,0)

# Write CSV file.
file="MeshdataZsurf.csv"
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

    # t=0.0 s, zsurf=0.3 m
    v=[str(0.0)]+[str(0.3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=3.5 s, zsurf=0.3 m
    v=[str(3.5)]+[str(0.3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=4.0 s, zsurf according to y value.
    npz=81
    zmin,zmax=0.1,0.8
    zp=(zmax-zmin)/(npz-1);
    v=[str(4.0)]+[str(zmin+cy*zp) for cy in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=4.0001 s, zsurf=0.3 m
    v=[str(4.0001)]+[str(0.3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=5.0 s, zsurf according to y value.
    zmin,zmax=0.1,1.0
    zp=(zmax-zmin)/(npz-1);
    v=[str(5.0)]+[str(zmin+(npz-1-cy)*zp) for cy in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=5.0001 s, zsurf=0.3 m
    v=[str(5.0001)]+[str(0.3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=5.5 s, zsurf=1.0 m
    v=[str(5.5)]+[str(1.0) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=6.0 s, zsurf=1.0 m
    v=[str(6.0)]+[str(1.0) for _ in range(Npt)]
    f.write(";".join(v)+"\n")

    # t=6.0001 s, zsurf=0.3 m
    v=[str(6.0001)]+[str(0.3) for _ in range(Npt)]
    f.write(";".join(v)+"\n")
   
    # t=6.5 s, zsurf according to the circle in pcen.
    pcen=2
    ra=0.5
    zmin=1
    dp=Vec1[1]
    vy=[cy*dp for cy in range(Npt)]
    v=[str(6.5)]+[str(zmin+m.sqrt(ra*ra-(y-pcen)**2) if pcen-ra<=y<=pcen+ra else zmin) for y in vy]
    f.write(";".join(v)+"\n")

print(f"{file} file successfully created.")
