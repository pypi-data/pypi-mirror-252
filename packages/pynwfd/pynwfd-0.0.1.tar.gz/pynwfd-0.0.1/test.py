from pynwfd.grib_write import *
import numpy as np

data_size=193*220
grib_size=(500+data_size*4)*12 #12 hour,193*220 points,float type 
cgrib=(c_ubyte*grib_size)()

data=np.zeros((12,193,220))-1
data[1,10:20,10:20]=63

filename='leo-null.grb2'
#status=0:业务产品 1:测试产品 2:科研产品 3:再分析 
lens=Nwfd().nwfd_create(cgrib,2021, 3, 28, 8, 0, 0,status=0)
# def nwfd_addgrid(self,cgrib,slon,elon,slat,elat,DX,DY,Ni,Nj):
lens=Nwfd().nwfd_addgrid(cgrib, 101.05, 112, 22.1, 31.7, 0.05, 0.05, 220, 193)
for i in range(12):
    #  def nwfd_addfield_jpeg(self,cgrib,category,element,statistical, year, month, day, hour, minute,second, 
    #                                forecasttime, timerange, data, ngrdpts, leveltype, level, isforecast=True, istimepoint=False):
    lens=Nwfd().nwfd_addfield_jpeg(cgrib,1,201,0,2021,3,28,8,0,0,i+1,1,data[i,:,:],data_size,1,0,True,False)
lens=Nwfd().nwfd_end(cgrib)
lens=Nwfd().nwfd_savetofile(cgrib, lens, grib2file=filename)