"""
.. module:: run_slab
   :synopsis: Python version of slab models

.. moduleauthor:: A. M. Arabhavi


"""
# # Imports
import numpy as np
import prodimopy.hitran as ht
import prodimopy.plot_slab as ps
import prodimopy.read_slab as rs
from astropy.io import fits
import pickle
from astropy.convolution import Gaussian1DKernel
from astropy.convolution import convolve as apy_convolve

# # Constant definitions
from scipy.constants import c,k,h
from scipy.constants import astronomical_unit as au
from scipy.constants import parsec as pc
from scipy.constants import atomic_mass as amu
percm2_to_perm2 = 1e4
gpercm3_to_kgperm3 = 1e3
cm2perg_to_m2perkg = 1e-1

kb = k*1.000
kmps = 1e3
um = 1e-6
cm_K = c*h/kb*1e2
jy = 1e-26


# # Function definitions
def boltzmann_distribution(E_level,g,Temperature,Partition_sum):
    '''
    Calculates LTE level population

    Parameters
    ----------
    E_level : scalar or numpy array
        Energy level (cm-1)

    g :  scalar or numpy array
        Statistical weight or degeneracy of the level

    Temperature :  scalar or numpy array
        Gas temperature in Kelvin

    Partition_sum :  scalar or numpy array
        (HITRAN) Partition sum 

    '''
    # c*h/k *1e2 # convert cm-1 to K
    return(g*np.exp(-E_level*c*h/k *1e2/Temperature)/Partition_sum)
def profile_function(nu,nu0,dnu):
    '''
    Calculates the profile function at a given spectral location.
    Assumes a Gaussian profile.
    Note that here the factor 1/(dnu*pi**0.5) is left out and is required to be multiplied wherever this function is used.
    All the input parameters should be in the same units.

    Parameters
    ----------

    nu : scalar or numpy array
        Spectral location where the profile function needs to be calculated

    nu0 : scalar or numpy array
        Spectral location of the line center

    dnu : scalar or numpy array
        The Doppler frequency shift
    '''
    return(np.exp(-((nu-nu0)/dnu)**2))
def planck(T,nu):
    '''
    Calculates the Planck function at a given frequency for a given temperature

    Parameters
    ----------

    T : scalar or numpy array
        Temperature of the Planck curve in Kelvin

    nu : scalar or numpy array
        Frequency in Hz
    '''
    return(2*h*nu**3/c**2/(np.exp(h*nu/kb/T)-1))

# # Fetching HITRAN partition sums (based on HITRAN python package)
QT_mol_id = {'H2O':1,'CO2':2,'O3':3,'N2O':4,'CO':5,'CH4':6,'O2':7,
'NO':8,'SO2':9,'NO2':10,'NH3':11,'HNO3':12,'OH':13,'HF':14,'HCl':15,
'HBr':16,'HI':17,'ClO':18,'OCS':19,'H2CO':20,'HOCl':21,'N2':22,'HCN':23,
'CH3Cl':24,'H2O2' :25,'C2H2':26,'C2H6':27,'PH3':28,'COF2':29,'SF6':30,'H2S':31,
'HCOOH':32,'HO2'  :33,'ClONO2':35,'NO+':36,'HOBr':37,'C2H4':38,'CH3OH':39,# no 34
'CH3Br':40,'CH3CN':41,'CF4':42,'C4H2':43,'HC3N':44,'H2':45,'CS':46,'SO3':47,'C2N2':48,
'COCl2':49,'SO':50,'CH3F':51,'GeH4':52,'CS2':53,'CH3I':54,'NF3':55,'C3H4':56,'CH3':57}

QT_niso = [0,9,13,18,5,9,4,6,3,4,2,2,2,3,2,4,4,2,2,6,3,2,3,3,2,1,3,3,1,
2,1,3,1,1,1,2,1,2,3,1,2,4,1,1,6,2,4,1,2,2,3,1,5,4,2,1,1,1]


# H2O
QT_Tmax = [0, 5000.,5000.,5000.,5000.,5000.,5000.,6000.,6000.,6000.,
# CO2
5000.,5000.,3500.,3500.,3500.,3500.,5000.,3500.,5000.,5000.,3500.,5000.,5000.,
# O3
1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,1000.,
# N2O,                           CO
5000.,5000.,5000.,5000.,5000.,   9000.,9000.,9000.,9000.,9000.,9000.,9000.,9000.,9000.,
# CH4,                     O2,                                    NO,                  SO2
2500.,2500.,2500.,2500.,   7500.,7500.,7500.,7500.,7500.,7500.,   5000.,5000.,5000.,   5000.,5000.,5000.,5000.,
# NO2,         NH3,           HNO3,          OH,                  HF,            HCl
1000.,1000.,   6000.,6000.,   3500.,3500.,   9000.,5000.,5000.,   6000.,6000.,   6000.,6000.,6000.,6000.,
# HBr,                     HI,            ClO,           OCS,                                   H2CO
6000.,6000.,6000.,6000.,   6000.,6000.,   5000.,5000.,   5000.,5000.,5000.,5000.,5000.,5000.,   3500.,5000.,5000.,
# HOCl,        N2,                  HCN,                 CH3Cl,         H2O2,    C2H2, 
5000.,5000.,   9000.,9000.,9000.,   3500.,3500.,3500.,   5000.,5000.,   6000.,   5000.,5000.,5000.,   
# C2H6,              PH3,     COF2,          SF6,     H2S,                 HCOOH,   HO2,   O atom, ClONO2,
5000.,5000.,5000.,   4500.,   3500.,3500.,   5000.,   4000.,5000.,5000.,   5000.,   5000.,   0.,   5000.,5000.,   
#  NO+,  HOBr,          C2H4,                CH3OH,   CH3Br,         CH3CN,                     CF4
5000.,   5000.,5000.,   5000.,5000.,5000.,   3500.,   5000.,5000.,   5000.,5000.,5000.,5000.,   3010.,
# C4H2,  HC3N,                                  H2,            CS,                        SO3, 
5000.,   5000.,5000.,5000.,5000.,5000.,5000.,   6000.,6000.,   5000.,5000.,5000.,5000.,   3500.,
# C2N2,        COCl2,        SO,                 CH3F    GeH4                          
5000.,5000.,   5000.,5000.,  5000.,5000.,5000.,  5000.,  5000.,5000.,5000.,5000.,5000.,
# CS2                       CH3I,         NF3     C3H4,    CH3,  
  5000.,5000.,5000.,5000.,  5000.,5000.,  5000.,  5000.,   5000.]

def fetch_QT(mol,iso,T,QTpath,T_limit='warn',verbose=True):
    '''
    Retrieve the partition sum from HITRAN QTpy files

    Parameters
    ----------

    mol : string
        Molecule name, e.g. 'CO2'

    iso : integer
        Isotopologue number, see hitran.org for more information
    
    T : float
        Temperature in Kelvin

    QTpath : string
        Path pointing to directory containing the directory QTpy provided by HITRAN (see hitran.org)
    '''
    mol = int(QT_mol_id[mol])
    iso = int(iso)
    if not (iso>0 and iso<=QT_niso[mol]):
        raise ValueError('the range is',1,' to', QT_niso[mol],' try again')  
    file = QTpath+str(mol)+'_'+str(iso)+'.QTpy'
    QTdict = {}
    with open(file, 'rb') as handle:
        QTdict = pickle.loads(handle.read())
    if (type(T) is int) or (type(T) is float) or (type(T) is np.float64):
        if not (T>=1. and T<=QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso]):
            if T_limit=='warn':
                if(T<1.):
                    if verbose:
                        print('WARNING: ',T,' falls below the temperature range ',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                        print('resetting T = 1')
                    T = 1.
                else:
                    if verbose:
                        print('WARNING: ',T,' falls above the temperature range ',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                        print('resetting T = ',QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                    T = QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso]
            else:
                raise ValueError('the temperature range is',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso],' try again')  
        Q1 = float(QTdict[str(int(T))])
        if T==QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso]:
            Q2 = Q1
        else:
            Q2 = float(QTdict[str(int(T)+1)])
        QT = Q1+(Q2-Q1)*(T-int(T))
    else:
        T = np.array(T)
        if not (np.amin(T)>=1. and np.amax(T)<=QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso]):
            if T_limit=='warn':
                if(T<1.):
                    print('WARNING: ',T,' falls below the temperature range ',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                    print('resetting T = 1')
                    T = 1.
                else:
                    print('WARNING: ',T,' falls above the temperature range ',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                    print('resetting T = ',QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso])
                    T = QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso]
            else:
                raise ValueError('the temperature range is',1,' to', QT_Tmax[np.sum(QT_niso[1:mol],dtype=int)+iso],' try again')  
        QT = np.array([float(QTdict[str(int(t))])+(float(QTdict[str(int(t)+1)])-float(QTdict[str(int(t))]))*(t-int(t)) for t in T])
    return(QT)


def run_0D_slab(Ng,Tg,vturb,molecule,mol_mass,HITRANfile,R_grid,QTpath,output_filename,isotopolog=[1],wave_mol=[4,30],wave_spec=[4.9,28],write_output=True,overlap=True):
    '''
    This is a python implementation of 0D slab models, based on the FORTRAN version of 0D slab models in ProDiMo (https://prodimo.iwf.oeaw.ac.at/)
    This runs models with/without line overlap. More robust and efficient code is available on Fortran, please check the above website (especially for running large grids of models).
    The Fortran code also supports OMP and supports including multiple species.

    Ng : float
        Gas column density (cm-2)
    
    Tg: float
        Gas temperature (K)

    vturb : float
        Turbulent velocity of the gas (km/s)

    molecule : string
        Molecule name, e.g. 'CO2'

    mol_mass : float or int
        Molecular mass in atomic mass units (amu)

    HITRANfile : string
        Path to the HITRAN '.par' file containing the line data downloaded from HITRAN
    
    R_grid : float
        High resolution grid on which the spectra has to be calculated initially
        Recommend minimum of 1e5

    QTpath : string
        Path pointing to directory containing the directory QTpy provided by HITRAN (see hitran.org)

    output_filename: string
        Filename(+path) for the fits output file
        Use the extension '.fits.gz'

    isotopolog : list
        List containing isotopologue numbers (HITRAN format)

    wave_mol : list
        Wavelength limits in microns to select the lines from the HITRAN file

    wave_spec : list
        Wavelength limits in microns for calculating the spectra

    overlap : boolean
        Whether or not to perform line overlap calculations
    '''
    extension = '.fits.gz'
    if isinstance(output_filename,str):
        if not('.fits.gz' in output_filename):
            output_filename = str(output_filename)+extension
    else:
        raise TypeError('output_filename should be a string with extension .fits.gz')

# # Reading HITRAN data
    mol_data = ht.read_hitran(HITRANfile,molecule,isotopolog,wave_mol[0],wave_mol[1])

# # wavelength grid definitions and some reshaping  
    N_lines = len(mol_data)
    N_nu_lines = 1+int(np.log10(wave_spec[1]/wave_spec[0])/np.log10(1.0+1.0/R_grid))
    dnu_ovlp = (np.log10(c/wave_spec[0]*1e6)-np.log10(c/wave_spec[1]*1e6))/N_nu_lines
    nu_grid = np.zeros((N_nu_lines))
    for i in range(N_nu_lines):
        nu_grid[-(i+1)] = 10**(np.log10(c/wave_spec[1]*1e6)+(i)*dnu_ovlp)
    W_grid  = c/nu_grid/um
    nu_grid = nu_grid.reshape(1,1,N_nu_lines)
    W_grid  = W_grid.reshape(1,1,N_nu_lines)
    N_lines = len(mol_data)
    lambda_0 = np.array(mol_data['lambda']).reshape(1,N_lines,1)*um
    nu_0 = c/lambda_0
    Aul = np.array(mol_data['A']).reshape(1,N_lines,1)
    gu = np.array(mol_data['g_u']).reshape(1,N_lines,1)
    gl = np.array(mol_data['g_l']).reshape(1,N_lines,1)
    E_u = np.array(mol_data['E_u']).reshape(1,N_lines)
    E_l = np.array(mol_data['E_l']).reshape(1,N_lines)
    Ng*=percm2_to_perm2
    vturb*=kmps

    I_nu_line,tau_ret,pop_l,pop_u = run_0D_point(Ng,Tg,vturb,molecule,mol_mass,nu_0,Aul,E_u,E_l,gu,gl,QTpath,isotopolog,nu_grid,overlap)
    if write_output:
        write_0D_output(output_filename,nu_grid,I_nu_line,tau_ret,R_grid,Ng,Tg,vturb,pop_l,pop_u,mol_data,molecule,overlap)
    return

def run_0D_point(Ng,Tg,vturb,molecule,mol_mass,nu_0,Aul,E_u,E_l,gu,gl,QTpath,isotopolog,nu_grid,overlap=True):
    '''
    This runs a RT on a single point with/without line overlap.
    All variables use SI unit
    
    Ng : float
        Gas column density (m-2)
    
    Tg: float
        Gas temperature (K)

    vturb : float
        Turbulent velocity of the gas (m/s)

    molecule : string
        Molecule name, e.g. 'CO2'

    mol_mass : float or int
        Molecular mass in atomic mass units (amu)

    nu_0 : numpy array
        Line frequencies (Hz)
    
    Aul : numpy array
        Einstein A coefficient
    
    E_u : numpy array
        Upper energy level
    
    E_l : numpy array
        Lower energy level
    
    gu : numpy array
        Statistical weight / degeneracy of upper level
    
    gl : numpy array
        Statistical weight / degeneracy of lower level

    QTpath : string
        Path pointing to directory containing the directory QTpy provided by HITRAN (see hitran.org)

    isotopolog : list
        List containing isotopologue numbers (HITRAN format)

    nu_grid : numpy array
        Array containing spectral grid for the final spectra

    overlap : boolean
        Whether or not to perform line overlap calculations
    '''
    N_lines = len(nu_0[0,:,0])
    N_nu_lines = len(nu_grid[0,0,:])
# # Variable definitions and initializations
    vg_grid  = np.sqrt(vturb**2+2*kb*Tg/mol_mass/amu)

# # Level population calculation
    pop_u = boltzmann_distribution(E_u,gu[:,:,0],Tg,fetch_QT(molecule,isotopolog[0],Tg,QTpath)).reshape(1,N_lines,1)
    pop_l = boltzmann_distribution(E_l,gl[:,:,0],Tg,fetch_QT(molecule,isotopolog[0],Tg,QTpath)).reshape(1,N_lines,1)

# # Line optical depths
    Tauuu = (Aul*(c/nu_0)**3/(8.0*np.pi**1.5*vg_grid)*Ng*(gu/gl*pop_l-pop_u))
    sigma_thresh = 20
    sigma = vg_grid*(nu_0)/c

# # RT calculation
    if overlap:
        tau_ret = np.zeros((N_nu_lines))
        for inu,nu in enumerate(nu_0[0,:,0]):
            mask = np.abs(nu_grid - nu).reshape(N_nu_lines)<(sigma_thresh/2*sigma[0,inu,0]).reshape(1)
            prof = profile_function(nu_grid[0,0,mask],nu,vg_grid*nu/c)
            tau_ret[mask] += (Tauuu[0,inu,0]*prof).T
        I_nu_line = planck(Tg,nu_grid[0,0,:])*(1-np.exp(-tau_ret))
        return(I_nu_line,tau_ret)

    else:
        return(planck(Tg,nu_0[0,:,0])*growth_function(Tauuu[0,:,0])*vg_grid*nu_0[0,:,0]/c,Tauuu[0,:,0],pop_l[0,:,0],pop_u[0,:,0])


def write_0D_output(output_filename,nu_grid,I_nu_line,tau_ret,R_grid,Ng,Tg,vturb,pop_l,pop_u,mol_data,molecule,overlap):
    '''
    Writes output file containing the output of the 0D slab model
    '''
    if overlap:
        hder = fits.Header(cards=[fits.Card('NMODELS',1)])
        hdu = fits.PrimaryHDU([0.0,0.0],header=hder)
        data = np.zeros((len(I_nu_line),5))
        data[:,0] = I_nu_line[::-1]*1e3
        data[:,1] = tau_ret[::-1]
        data[:,2] = I_nu_line*0.0
        data[:,3] = I_nu_line*0.0
        data[:,4] = nu_grid[0,0,::-1]*1e-9
        hder = fits.Header(cards=[fits.Card('NAXIS',2),
                                fits.Card('NAXIS1',5),
                                fits.Card('NAXIS2',len(I_nu_line)),
                                fits.Card('MODEL',1),
                                fits.Card('NLINE',len(I_nu_line)),
                                fits.Card('R_OVLP',R_grid),
                                fits.Card('NHTOT',Ng/percm2_to_perm2),
                                fits.Card('TG',Tg),
                                fits.Card('TD',10),
                                fits.Card('VTURB',vturb/kmps)])
        hdu1 = fits.ImageHDU(data,header=hder)
        hdul = fits.HDUList([hdu,hdu1])
        hdul.writeto(output_filename,overwrite=True)
    
    else:
        with open(output_filename+'.out','w') as f:
            f.write('1  ! Nmodels\n')
            f.write('1 ! model\n')
            
            f.write('1  ! Number of species\n')
            f.write(f'{Ng:12.5e} ! Gas column density\n')
            f.write(f'{Ng:12.5e} ! Total gas density\n')
            f.write(f'{1:12.5e} ! electron density [cm^-3]\n')
            f.write(f'{1:12.5e} ! He density [cm^-3]\n')
            f.write(f'{1:12.5e} ! HII density [cm^-3]\n')
            f.write(f'{1:12.5e} ! HI density [cm^-3]\n')
            f.write(f'{1:12.5e} ! H2 density [cm^-3]\n')
            f.write(f'{1:12.5e} ! dust_to_gas\n')
            f.write(f'{1:12.5e} ! turbulent velocity [km/s]\n')
            f.write(f'{Tg:6.1f} ! Tgas [K]\n')
            f.write(f'{0:6.1f} ! Tdust [K]\n')
            f.write(f'{0:d} ! Num\n')
            f.write(f'{molecule}\n')
            f.write(f'{1:.1f} ! relative abundance\n')
            f.write(f'{vturb*1e3:12.5e} ! dv [cm/s]\n')
            f.write(f'{2*len(mol_data):12d} ! Nlev\n')
            f.write(f'! i   g       Ener(K)   pop           ltepop      e   v   J\n')
            for i in range(len(mol_data)):
                f.write(f"{2*i:8d} {mol_data.iloc[i]['g_u']:9.1f} {mol_data.iloc[i]['E_u']:9.1f}{0.0:14.5E}{pop_u[i]:14.5E}{0:4d} {0:4d} {0:4d} \n")
                f.write(f"{2*i+1:8d} {mol_data.iloc[i]['g_l']:9.1f} {mol_data.iloc[i]['E_l']:9.1f}{0.0:14.5E}{pop_l[i]:14.5E}{0:4d} {0:4d} {0:4d} \n")
            f.write(f'{len(mol_data):12d} ! Nline\n')
            f.write(f'! i u l e v J gu Eu A B GHz tauD Jback pop ltepop tauNLTE\n')
            f.write(f'tauLTE bNLTE bLTE pNLTE pLTE FNLTE FLTE globU globL locU locL\n')
            for i in range(len(mol_data)):
                Bul = mol_data.iloc[i]['A']*0.5*c**2/(h*(mol_data.iloc[i]['nu']*c*1e2)**3)
                f.write(f"{i:8d} {2*i:8d} {2*i+1:8d} {0:4d} {0:4d} {0:4d} {mol_data.iloc[i]['g_u']:14.5E} {mol_data.iloc[i]['E_u']:14.5E} {mol_data.iloc[i]['A']:14.5E} {Bul:14.5E} {mol_data.iloc[i]['nu']*c*1e2*1e-9:14.5E} {0.0:14.5E} {0.0:14.5E} {0.0:14.5E} {pop_u[i]:14.5E} {0.0:14.5E} {tau_ret[i]:14.5E} {0.0:14.5E} {0.0:14.5E} {0.0:14.5E} {0.0:14.5E} {0.0:14.5E} {I_nu_line[i]:14.5E} {mol_data.iloc[i]['global_l']:20} {mol_data.iloc[i]['global_u']:20} {mol_data.iloc[i]['local_l']:20} {mol_data.iloc[i]['local_u']:20} \n")

    return


def run_1D_radial_slab(Ng,Tg,R,d,vturb,molecule,mol_mass,HITRANfile,R_grid,QTpath,output_filename,width='area_given',Rin_limit=0,Rout_limit=1e99,isotopolog=[1],wave_mol=[4,30],wave_spec=[4.9,28]):
    '''
    This is a python implementation of 1D radial slab models, based on the FORTRAN version of 1D slab models in ProDiMo (https://prodimo.iwf.oeaw.ac.at/)
    This runs models with line overlap. More robust and efficient code (including vertical slab model) is available in Fortran, please check the above website (especially for running large grids of models).
    The Fortran code also supports OMP and supports including multiple species.

    Ng : numpy array or list
        Gas column density (cm-2)
    
    Tg : numpy array or list
        Gas temperature (K)
    
    R : numpy array or list
        Radius (AU)
    
    d : float
        Distance of the disk (parsec)

    vturb : float
        Turbulent velocity of the gas (km/s)

    molecule : string
        Molecule name, e.g. 'CO2'

    mol_mass : float or int
        Molecular mass in atomic mass units (amu)

    HITRANfile : string
        Path to the HITRAN '.par' file containing the line data downloaded from HITRAN
    
    R_grid : float
        High resolution grid on which the spectra has to be calculated initially
        Recommend minimum of 1e5

    QTpath : string
        Path pointing to directory containing the directory QTpy provided by HITRAN (see hitran.org)

    output_filename : string
        Filename(+path) for the fits output file
        Use the extension '.fits.gz'

    width : string or list or float
        'area_given' - the provided radii array is used as the emitting area equivalent radius
        'infer' - Assumes the provided radius as radial distance from the star and calculates the width of individual rings of slab grids
        list - List containing emitting area equivalent radii
        float - Constant emitting area equivalent radius, used for all grid points
    
    Rin_limit : float
        Inner radius limit of the disk (AU)
    
    Rout_limit : float
        Outer radius limit of the disk (AU)

    isotopolog : list
        List containing isotopologue numbers (HITRAN format)

    wave_mol : list
        Wavelength limits in microns to select the lines from the HITRAN file

    wave_spec : list
        Wavelength limits in microns for calculating the spectra
    '''
    extension = '.fits.gz'
    if isinstance(output_filename,str):
        if not('.fits.gz' in output_filename):
            output_filename = str(output_filename)+extension
    else:
        raise TypeError('output_filename should be a string with extension .fits.gz')

# # Reading HITRAN data
    mol_data = ht.read_hitran(HITRANfile,molecule,isotopolog,wave_mol[0],wave_mol[1])

# # wavelength grid definitions and some reshaping  
    N_lines = len(mol_data)
    N_nu_lines = 1+int(np.log10(wave_spec[1]/wave_spec[0])/np.log10(1.0+1.0/R_grid))
    dnu_ovlp = (np.log10(c/wave_spec[0]*1e6)-np.log10(c/wave_spec[1]*1e6))/N_nu_lines
    nu_grid = np.zeros((N_nu_lines))
    for i in range(N_nu_lines):
        nu_grid[-(i+1)] = 10**(np.log10(c/wave_spec[1]*1e6)+(i)*dnu_ovlp)
    W_grid  = c/nu_grid/um
    nu_grid = nu_grid.reshape(1,1,N_nu_lines)
    W_grid  = W_grid.reshape(1,1,N_nu_lines)
    N_lines = len(mol_data)
    lambda_0 = np.array(mol_data['lambda']).reshape(1,N_lines,1)*um
    nu_0 = c/lambda_0
    Aul = np.array(mol_data['A']).reshape(1,N_lines,1)
    gu = np.array(mol_data['g_u']).reshape(1,N_lines,1)
    gl = np.array(mol_data['g_l']).reshape(1,N_lines,1)
    E_u = np.array(mol_data['E_u']).reshape(1,N_lines)
    E_l = np.array(mol_data['E_l']).reshape(1,N_lines)
    Ng = np.array(Ng)*percm2_to_perm2
    vturb = np.array(vturb)*kmps
    R = np.array(R)*au
    Rin_limit *= au
    Rout_limit *= au
    Rr = np.zeros_like(R)
    if width == 'infer':
        if len(R)>1:
            if ((R[1]-R[0])/2>R[0]) or ((R[1]-R[0])/2>(R[0]-Rin_limit)) :
                Rr[0] = (R[0]+(R[1]-R[0])/2)**2-Rin_limit**2
            else:
                Rr[0] = (R[0]+(R[1]-R[0])/2)**2-(R[0]-(R[1]-R[0])/2)**2
            if ((R[-2]-R[-1])/2>(Rout_limit-R[-1])) :
                Rr[-1] = Rout_limit**2-(R[-2]+(R[-1]-R[-2])/2)**2
            else:
                Rr[-1] = ((R[-1]-R[-2])/2+R[-1])**2-(R[-1]-(R[-1]-R[-2])/2)**2
            if len(R)>2:
                for i in range(len(Ng)-2):
                    Rr[i+1] = (R[i+1]+(R[i+2]-R[i+1])/2)**2-(R[i+1]-(R[i+1]-R[i])/2)**2
        else:
            Rr = R**2
    elif width == 'area_given':
        Rr = R**2
    elif isinstance(width,float) or isinstance(width,int):
        Rr+=width**2
    else:
        for i in range(len(Ng)):
            Rr[i] = (R[i]+width[i]/2)**2-(R[i]-width[i]/2)**2
    d *= pc
    if isinstance(vturb,float) or isinstance(vturb,int): vturb = np.ones_like(Ng)*vturb
    total_flux = np.zeros((N_nu_lines))
    for i in range(len(Ng)):
        I_nu_line,tau_ret = run_0D_point(Ng[i],Tg[i],vturb[i],molecule,mol_mass,nu_0,Aul,E_u,E_l,gu,gl,QTpath,isotopolog,nu_grid)
        total_flux += I_nu_line*np.pi*Rr[i]/d**2
    write_0D_output(output_filename,nu_grid,total_flux,tau_ret*0.0,R_grid,0,0,0)
    return

def growth_function(tau):
    '''
    This function returns the growth function, or the flux growth for the given line optical depth(s)

    tau : numpy array or list
        line optical depth 
    '''
    tau = np.array(tau)
    growth = np.zeros_like(tau)
    mask1 = tau<1e-13
    mask2 = (~mask1) & (tau<10)
    mask3 = (~mask1) & (~mask2)
    growth[mask1] = 0.0
    growth[mask2] = 7.98554359*tau[mask2]**0.9999470274/(4.509393063+1.72466517*tau[mask2]**1.062901665)
    growth[mask3] = 2.8859693*(np.log10(tau[mask3])**0.50868585)+0.40682335
    return(growth)