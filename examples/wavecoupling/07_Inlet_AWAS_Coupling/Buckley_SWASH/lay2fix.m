%----------------------------------------------------------------------
% lay2fix: convert SWASH layer velocity output to fixed position output 
% Created by Tomohiro SUZUKI (Flanders Hydraulics) on 2019/01/04 
% Modified by Corrado ALTOMARE (UPC) on 2024/02/26
%----------------------------------------------------------------------

clear variables
close all

nlay = 10;
dep  = 0.7396;
dpx  = 0.01;
dpz  = dep/nlay;
firstline=[0,0,0,0,0,0,0,0,0,0,0,0];

gain=1; %factor to amplify SWASH signal

%% file names
% x coupling =17m
velname='Buckley_OBC_SWASH.vel';
etaname='Buckley_OBC_SWASH.tbl';
awasname='Buckley_OBC_SWASH.tbla';


%%

F = fopen(velname);
TEMP = textscan(F,'%f %f %f %f %f %f %f %f %f %f','Headerlines',10);
for k=1:nlay
  VELS(:,k) = TEMP{1,(nlay+1)-k}(:,1); % SWASH layer velocity: first layer is top layer in SWASH!
end

ETA = load(etaname); % SWASH time ETA(:,1) and water surface ETA(:,2)
for j=1:length(ETA(:,1)) 
  VELF(j,1) = VELS(j,1);      % first fixed point (bottom) is assumed the same as SWASH bottom velocity  
  for i=2:nlay+1

    VELF(j,i) = interp1(...
                [(ETA(j,2)+dep)/nlay/...
                2:(ETA(j,2)+dep)/nlay:(ETA(j,2)+dep)*(1-1/nlay/2)],...
                [VELS(j,1:nlay)],...
                dep*(i-1)/nlay,'linear','extrap');
  end
end

VELF(:,end)=VELS(:,end);


OUT(:,1)           = ETA(:,1)-ETA(1,1);
OUT(:,2:nlay+2)    = [VELF(:,1:nlay+1)*gain];

% csvoutput for velocity

INC_io_name = strcat('CaseBuckley_inlet.csv');
fid=fopen(INC_io_name, 'wt');
fprintf(fid,'fmtversion;grid_dpx;grid_dpz;grid_nx;grid_nz;vars\n');

T=[dpx dpz 1 nlay+1];
fprintf(fid,'1;%.4f;%.5f;%d;%d;velx\n',T);
fprintf(fid,'%s\n',' ');
fprintf(fid,'time;vx_x0_z0;vx_x0_z1;vx_x0_z2;vx_x0_z3;vx_x0_z4;vx_x0_z5;vx_x0_z6;vx_x0_z7;vx_x0_z8;vx_x0_z9;vx_x0_z10;vz_x0_z0;vz_x0_z1;vz_x0_z2;vz_x0_z3;vz_x0_z4;vz_x0_z5;vz_x0_z6;vz_x0_z7;vz_x0_z8;vz_x0_z9;vz_x0_z10\n')
fprintf(fid,'%.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f; %.4f\n', OUT')
fclose(fid)

ETAinc(:,2)=ETA(:,2)*gain+dep;
ETAinc(:,1)= ETA(:,1)-ETA(1,1);
% csvoutput for zsurf
csvwrite('CaseBuckley_zsurf.csv',ETAinc);

ETAa = load(awasname); % SWASH AWAS time ETAa(:,1) and water surface ETAa(:,2)
ETAa(:,2)=ETAa(:,2)*gain+dep;
ETAa(:,1)= ETAa(:,1)-ETAa(1,1);										  
% csvoutput for awas
csvwrite('CaseBuckley_awasIn.csv',ETAa);

% Figure 1 (Plot to compared the SWASH results for the uppermost two layers and the results from interpolation at fixed z-coordinates below the still water level)---------
fg1     = figure; 
figsize = [150 50 1000 600];
set(fg1,'Units','Pixels','NumberTitle','Off','Resize','on',...
        'Name',['Velocities for Inlet'],'Position', figsize ); 
plot(OUT(:,1),VELF(:,end),'k')
hold on
plot(OUT(:,1),VELS(:,end),'--r')
plot(OUT(:,1),VELF(:,end-1),'b')
plot(OUT(:,1),VELS(:,end-1),'--m')
plot(OUT(:,1),VELF(:,end-2),'g')
plot(OUT(:,1),VELS(:,end-2),'--c')
legend('SWL','Top SWASH','SWL-dz','top SWASH-1','SWL-2dz','top SWASH-2')
xlim([150 200])
xlabel('time (s)')
ylabel('u (m/s)')
