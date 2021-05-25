

import numpy as np

from classes.om import ObjectManager


def staggeredGrid(model_uid, wavelet_uid, sim_steps, **kwargs):

    
    OM = ObjectManager()
    model = OM.get(model_uid)
    wavelet = OM.get(wavelet_uid)
    
    layers = OM.list(parent_uid=model.uid)
    geo_layer_1 = layers[0]
    
    if len(layers) == 2:
        geo_layer_2 = layers[1]    
    elif len(layers) == 1:
        geo_layer_2 = layers[0]  
    else:
        raise Exception()
        
    # Discretization
    c1 = 20   # Number of grid points per dominant wavelength
    c2 = 0.5  # CFL-Number


    
    
    #dx = kwargs['dx']
    #dy = kwargs['dy']
    #dt = kwargs['dt']

    #f0 = kwargs['f0']
    #amp = kwargs['amp']



    
    # nx = input_vec.shape[0]  # Number of grid points in X
    # ny = input_vec.shape[1]  # Number of grid points in Y
    T = 1.0     # Total propagation time



    # Source Position
    sou_x = kwargs['sou_x']    # Source position (in grid points) in X
    sou_y = kwargs['sou_y']    # Source position (in grid points) in Y


    # No vetor grid, pontos com valor 1 estao associados a Fase 1 (rocha,
    # cor preta). Os pontos com valor 0 estao associados a Fase 2 (poros,
    # de cor branca).        
    # rho1 = 3.0
    # vp1 = 4000.0
    # #
    # rho2 = 2.2
    # vp2 = 2500.0




    

    vp_grid = np.where(model.data == geo_layer_1.value, geo_layer_1.vp, geo_layer_2.vp)
    rho_grid = np.where(model.data == geo_layer_1.value, geo_layer_1.rho, geo_layer_2.rho)


    ## Preparation
    
    # Init wavefields
    vx = np.zeros((model.ny, model.nx))
    vy = np.zeros((model.ny, model.nx))
    wavefield = np.zeros((sim_steps, model.ny, model.nx))
        
 
    # Calculate first Lame-Paramter
    #self.lame_lambda = self._rho_grid * self._vp_grid * self._vp_grid
    
    
    lambda1 =  geo_layer_1.rho * geo_layer_1.vp * geo_layer_1.vp
    lambda2 = geo_layer_2.rho * geo_layer_2.vp* geo_layer_2.vp
    
    lame_lambda = np.where(model.data == geo_layer_1.value, lambda1, lambda2)
    
    
    cmin = min(vp_grid.flatten())   # Lowest P-wave velocity
    cmax = max(vp_grid.flatten())   # Highest P-wave velocity
    
    
    fmax = 2 * wavelet.f0                   # Maximum frequency
    



    
    #dx = 15.0 #0.000001 * 74 * 4
    #dy = dx                         # Spatial discretization (in m)
    dt = model.dx / (cmax) * c2           # Temporal discretization (in s)
    
    
    
    dt_dx = dt / model.dx  
        
    #CFL_number = (cmax * dt) / dx        
    CFL_number = cmax * dt_dx
    
    
    print ()
    print("CFL_number: ")
    print(CFL_number)
    
    
    lampda_min = cmin / fmax        # Smallest wavelength
    
   
    
 
    
    
    
    #dx = cmin/(fmax*c1)             # Spatial discretization (in m)
    #dy = dx                         # Spatial discretization (in m)

    
    
    
    # ## Create space and time vector
    x = np.arange(0, model.dx * model.nx, model.dx) # Space vector in X
    y = np.arange(0, model.dy * model.ny, model.dy) # Space vector in Y
    
    
    
    time_ = np.arange(0, T, dt)            # Time vector
    nt = np.size(time_)                    # Number of time steps
    
            
    print()
    print('time_.shape:')
    print(time_.shape, T, dt, time_[0], time_[-1])
    print()    
    
    print(model.dx, model.dy, dt)
        
    
 
    significance = 0.0000001
    wavelet_data = wavelet.get_amplitude_data(time_)  
    
    ###
    idx = len(wavelet_data)-1
    segue = True
    for i in range(len(wavelet_data)-1, -1, -1):
        #print(str(i) + " - " + str(wavelet[i])) 
        if np.absolute(wavelet_data[i]) > (wavelet.amp*significance) and segue:
            idx = i
            segue = False


    print("\n\n")
    print("last idx: " + str(len(wavelet_data)-1))
    print("idx: ", idx)
    print("time: ", time_[idx])
    print("\n\n")    
    
    
    time_ = np.arange(0, (idx+2)*dt, dt)            # Time vector
    nt = np.size(time_)                             # Number of time steps
    
    wavelet_data = wavelet.get_amplitude_data(time_)      
    
    ###
    
    
    
    
    
    
    # # ## Source signal - Ricker-wavelet
    # tau = np.pi * f0 * (t - 1.5 / f0)
    
    
    # print('tau')
    # print(tau.min(), tau.max())
    

            
    print()
    print('wavelet_data.shape:')
    print(wavelet_data.shape)
    print()
    
    
    
    # ## Source signal - Ricker-wavelet

#    tau = np.pi*f0*(t-1.5/f0)
#    q = q0*(1.0-2.0*tau**2.0)*np.exp(-tau**2)
    
    
    

    #c1 = cmin/(fmax*model.dx)
    n_gp_wl = cmin/(fmax*model.dx)
    print("Number of gridpoints per minimum wavelength: ", n_gp_wl)  
        
   # print("Number of grid points per dominant wavelength: ", lampda_min/model.dx)  
    
    
    
    
    # Calculation of coefficients c1 and c2. 
    # These are used to obtain a second-order accurate time, fourth-order 
    # accurate space. (Levander, 1988)
    c1 = 9.0 / 8.0
    c2 = 1.0 / 24.0
    #
    # c1_dx = c1 / dx
    # c2_dx = c2 / dx
    # #
    # c1_dy = c1 / dy
    # c2_dy = c2 / dy
    #
    
    
    # The true calculation starts here...    
    #
    for it in range(sim_steps):
        
        # if (it % 10 == 0):
        
        #print('Calculating SG [' + str(it+1) + '/' + str(sim_steps) +']')
        
        if it<2:
            continue

        wavefield[it, :, :] = wavefield[it-1, :, :]
        
        
        
        # Update velocity
        for kx in range(5, model.nx-4):    
            for ky in range(5, model.ny-4):
                
                # Stress derivatives, p_dx(+) e p_dy(+) 
                
                p_x = c1 * (wavefield[it, ky, kx+1] - wavefield[it, ky, kx]) - \
                      c2 * (wavefield[it, ky, kx+2] - wavefield[it, ky, kx-1])  # Eq. A-2 Lavender, 1988
                
                p_y = c1 * (wavefield[it, ky+1, kx] - wavefield[it, ky, kx]) - \
                      c2 * (wavefield[it, ky+2, kx] - wavefield[it, ky-1, kx])


                # Velocity extrapolation using Euler Method
                
#                print("vy[ky, kx]: ", ky, kx, vy[ky, kx] )

                try:
                    vx[ky, kx] -=  (dt_dx / rho_grid[ky, kx]) * p_x 
                    vy[ky, kx] -=  (dt_dx / rho_grid[ky, kx]) * p_y   
                except:
                    print("rho_grid[ky, kx]: ", ky, kx, rho_grid[ky, kx] )
                    print("vx[ky, kx]: ", ky, kx, vx[ky, kx] )
                    print("vy[ky, kx]: ", ky, kx, vy[ky, kx] )
                    
                    pass
                #vx[ky, kx] = vx[ky, kx] - dt / rho_grid[ky, kx] * p_x
                #vy[ky, kx] = vy[ky, kx] - dt / rho_grid[ky, kx] * p_y



        # Inject source wavelet
        if it < np.size(wavelet_data):
            
            wavefield[it, sou_y, sou_x] += wavelet_data[it]

        # Verificar a possibilidade abaixo - Curso W4V8 
        #vx[sou_y, sou_x] = vx[sou_y, sou_x]  + dt * wavelet[it] / (dt * rho_grid[sou_y, sou_x])
        #vy[sou_y, sou_x] = vy[sou_y, sou_x]  + dt * wavelet[it] / (dt * rho_grid[sou_y, sou_x])
        #



        # Update wavefield
        for kx in range(5, model.nx-4):     
            for ky in range(5, model.ny-4):
                
                # Velocity derivatives, vx_dx(-) e vy_dy(-)  # Qian et al 2013
                vx_x = c1 * (vx[ky, kx] - vx[ky, kx-1]) - c2 * (vx[ky, kx+1] - vx[ky, kx-2])  # Dx-, 
                vy_y = c1 * (vy[ky, kx] - vy[ky-1, kx]) - c2 * (vy[ky+1, kx] - vy[ky-2, kx])  # Dy-, 
                #
                wavefield[it, ky, kx] -=  (dt_dx * lame_lambda[ky, kx]) * (vx_x + vy_y)
                
                
                # try:
                #     termo = lame_lambda[ky, kx] * dt #* (vx_x + vy_y)
                #     termo = (vx_dx + vy_dy) * termo
                # except:
                #     print()
                #     print(it)
                #     print(lame_lambda[ky, kx])
                #     print(vx_dx + vy_dy)
                #     print(dt)
                #     print()
                    
                    
                #wavefield[it, ky, kx] = wavefield[it, ky, kx] - termo   # lame_lambda[ky, kx] * dt * (vx_x + vy_y)
 
    
    print("Wavefield Min-Max: ", np.min(wavefield), " - ",  np.max(wavefield))   
    print(model.dx, model.dy, dt)
    return wavefield, model.dx, model.dy, dt, CFL_number, n_gp_wl






