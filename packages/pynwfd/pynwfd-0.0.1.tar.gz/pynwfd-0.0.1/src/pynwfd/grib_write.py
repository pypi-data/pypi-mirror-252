import os,platform
from ctypes import *


def get_libapi():
    '''
    load lib....
    return: libapi handle
    if not linux and windows,return None.
    '''
    type_sys=platform.system()
    lib_dir=os.path.join(os.path.dirname(__file__),'lib64')
    if type_sys=='Linux':
        return CDLL(os.path.join(lib_dir,'libNwfd-grib2.so'),mode=1)
    elif type_sys=='Windows':
        return CDLL(os.path.join(lib_dir,'nwfd-grib2-win64.dll'))
    else:
        print('error: nwfd-lib python api just run in linux or windows...')
        return None

class Nwfd:
    def __init__(self):
        self.name='CMA Nwfd Grib C API'
        self.lib=get_libapi()
    
    def nwfd_create(self,cgrib,year,month,day,hour,minute,second,status):
        #status=0:业务产品 1:测试产品
        param=[year,month,day,hour,minute,second,status]
        st=[c_longlong(i) for i in param]
        # lens=self.lib.nwfd_create(byref(cgrib),st[0],st[1],st[2],st[3],st[4],st[5],st[6])
        lens=self.lib.nwfd_create(byref(cgrib),*st)
        return lens
    
    def nwfd_addgrid(self,cgrib,slon,elon,slat,elat,DX,DY,Ni,Nj):
        param=[slon,elon,slat,elat,DX,DY,Ni,Nj]
        st0=[c_float(i) for i in param[:-2]]
        st1=[c_longlong(i) for i in param[-2:]]
        # lens=self.lib.nwfd_addgrid(byref(cgrib),st0[0],st0[1],st0[2],st0[3],st0[4],st0[5],st1[0],st1[1])
        lens=self.lib.nwfd_addgrid(byref(cgrib),*st0,*st1)
        return lens

    def nwfd_addfield_simpled(self,cgrib,category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange, data, ngrdpts, leveltype, level, isforecast=True, istimepoint=False):
        param1=[category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange]
        param2=[ngrdpts, leveltype, level]

        st0=[c_longlong(i) for i in param1]
        st1=[c_longlong(i) for i in param2]

        data=data.reshape(ngrdpts)
        fld=(c_float*len(data))(*data)

        lens=self.lib.nwfd_addfield_simpled(byref(cgrib),*st0,byref(fld),*st1,bool(isforecast),bool(istimepoint))
        return lens

    def nwfd_addfield_complex(self,cgrib,category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange, data, ngrdpts, leveltype, level, isforecast=True, istimepoint=False):
        param1=[category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange]
        param2=[ngrdpts, leveltype, level]

        st0=[c_longlong(i) for i in param1]
        st1=[c_longlong(i) for i in param2]

        data=data.reshape(ngrdpts)
        fld=(c_float*len(data))(*data)

        lens=self.lib.nwfd_addfield_complex(byref(cgrib),*st0,byref(fld),*st1,bool(isforecast),bool(istimepoint))
        return lens

    def nwfd_addfield_png(self,cgrib,category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange, data, ngrdpts, leveltype, level, isforecast=True, istimepoint=False):
        param1=[category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange]
        param2=[ngrdpts, leveltype, level]

        st0=[c_longlong(i) for i in param1]
        st1=[c_longlong(i) for i in param2]

        data=data.reshape(ngrdpts)
        fld=(c_float*len(data))(*data)

        lens=self.lib.nwfd_addfield_png(byref(cgrib),*st0,byref(fld),*st1,bool(isforecast),bool(istimepoint))
        return lens

    def nwfd_addfield_jpeg(self,cgrib,category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange, data, ngrdpts, leveltype, level, isforecast=True, istimepoint=False):
        param1=[category,element,statistical, year, month, day, hour, minute,second, 
                                   forecasttime, timerange]
        param2=[ngrdpts, leveltype, level]

        st0=[c_longlong(i) for i in param1]
        st1=[c_longlong(i) for i in param2]

        data=data.reshape(ngrdpts)
        fld=(c_float*len(data))(*data)

        lens=self.lib.nwfd_addfield_jpeg(byref(cgrib),*st0,byref(fld),*st1,bool(isforecast),bool(istimepoint))
        return lens

    def nwfd_end(self,cgrib):
        lens=self.lib.nwfd_end(byref(cgrib))
        return lens

    def nwfd_savetofile(self,cgrib,lens,grib2file):
        
        lens=self.lib.nwfd_savetofile(byref(cgrib),c_longlong(lens),grib2file.encode())
        # return lens
        if lens:
            print('encode grib2 file Successful!')






