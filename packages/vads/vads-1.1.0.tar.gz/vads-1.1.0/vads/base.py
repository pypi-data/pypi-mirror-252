import numpy as np
from scipy import interpolate
from scipy.signal import savgol_filter as sv
import matplotlib
import matplotlib.pyplot as plt
import time
import copy
import ipywidgets
import math
import scipy
global ANALYZER_WORKFUNCTION
ANALYZER_WORKFUNCTION = 4.434


def updateWorkfunction(value):
	global ANALYZER_WORKFUNCTION
	ANALYZER_WORKFUNCTION=value

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 80, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	Courtesy of S.O. user Greenstick, https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	# Print New Line on Complete
	if iteration == total: 
		print()


def SBZ():
	""" Here be a doc string """
	def SBZ_plot(structure,surface,a,b,c):
		font = {'size'   : 14}
		matplotlib.rc('font', **font)

		fig,ax=matplotlib.pyplot.subplots(figsize=(4,4)) 

		if structure == 'cubic-fcc' and surface=='(100)':

			a_surface = a/math.sqrt(2)
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX

			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=4,radius=GM,orientation=math.radians(45),linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GM/math.sqrt(2),GM/math.sqrt(2),"$\overline{M}$"],[0,GX,"$\overline{X}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GM/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GM*0.05,y=point[1]+GM*0.05,s=point[2])

			ax.set_ylim([-GM*1.5,GM*1.5])
			ax.set_xlim([-GM*1.5,GM*1.5])

		if structure == 'cubic-fcc' and surface=='(111)':

			a_surface =  a/math.sqrt(2)
			GM = 2*math.pi/(np.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))

			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=6,radius=GK,orientation=0,linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GM,0,"$\overline{M}$"],[0,GK,"$\overline{K}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GK/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GK*0.05,y=point[1]+GK*0.05,s=point[2])

			ax.set_ylim([-GK*1.5,GK*1.5])
			ax.set_xlim([-GK*1.5,GK*1.5])

		if structure == 'cubic-fcc' and surface=='(110)':
			GX = math.pi*math.sqrt(2) / a
			GY = math.pi/ a
			GS = math.sqrt(GX**2 + GY**2)

			ax.add_patch(matplotlib.patches.Rectangle(xy=(0-GX,0-GY),width=2*GX,height=2*GY,angle=0,linestyle='--',color='tab:blue',fill=False,lw=2))

			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GX,0,"$\overline{X}$"],[GX,GY,"$\overline{S}$"],[0,GY,"$\overline{Y}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GS/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GS*0.05,y=point[1]+GS*0.05,s=point[2])

			ax.set_ylim([-GS*1.5,GS*1.5])
			ax.set_xlim([-GS*1.5,GS*1.5])

		if structure == 'cubic-bcc' and surface=='(100)':
			a_surface = a
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX
			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=4,radius=GM,orientation=math.radians(45),linestyle='--',color='tab:blue',fill=False,lw=2))
			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GM/math.sqrt(2),GM/math.sqrt(2),"$\overline{M}$"],[0,GX,"$\overline{X}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GM/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GM*0.05,y=point[1]+GM*0.05,s=point[2])
			ax.set_ylim([-GM*1.5,GM*1.5])
			ax.set_xlim([-GM*1.5,GM*1.5])

		if structure == 'cubic-bcc' and surface=='(111)':
			a_surface =  math.sqrt(2)*a
			GM = 2*math.pi/(np.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))
			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=6,radius=GK,orientation=0,linestyle='--',color='tab:blue',fill=False,lw=2))
			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GM,0,"$\overline{M}$"],[0,GK,"$\overline{K}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GK/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GK*0.05,y=point[1]+GK*0.05,s=point[2])
			ax.set_ylim([-GK*1.5,GK*1.5])
			ax.set_xlim([-GK*1.5,GK*1.5])

		if structure == 'hexagonal' and surface=='(0001)':

			GM = 2*math.pi/(np.sqrt(3)*a)
			GK = GM/np.cos(np.deg2rad(30))
			KM = GM*np.tan(np.deg2rad(30))
			ax.add_patch(matplotlib.patches.RegularPolygon(xy=(0,0),numVertices=6,radius=GK,orientation=0,linestyle='--',color='tab:blue',fill=False,lw=2))
			symmetryPoints=[[0,0,"$\overline{\Gamma}$"],[GM,0,"$\overline{M}$"],[0,GK,"$\overline{K}$"]]
			for point in symmetryPoints:	
				ax.add_patch(matplotlib.patches.Circle(xy=point[0:2],radius=GK/20,linestyle='-',color='tab:blue',fill=True,lw=1))
				ax.text(x=point[0]+GK*0.05,y=point[1]+GK*0.05,s=point[2])
			ax.set_ylim([-GK*1.5,GK*1.5])
			ax.set_xlim([-GK*1.5,GK*1.5])



		matplotlib.pyplot.axis('off')
		matplotlib.pyplot.show()

	def SBZ_text(structure,surface,a,b,c,hv):
		print("\n\n")

		if structure == 'cubic-fcc' and surface=='(100)':
			a_surface = a/math.sqrt(2)
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX

			GXdeg = k_to_polar_manipulator(kx=GX,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-ANALYZER_WORKFUNCTION)		
			if np.isnan(GXdeg): GXdegString = "inaccessible"
			else: GXdegString = "{:.1f}\u00B0 off normal".format(GXdeg)

			GMdeg = k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-ANALYZER_WORKFUNCTION)
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			print("\n\tIn-plane surface lattice constant\t= a/\u221A2 \t= {:.3f} Å".format(a_surface))
			print("\tMonoatomic spacing\t\t\t= a/2 \t= {:.3f} Å".format(a/2))
			print("\n\t\u0393-X = \u03c0/a_001 \t= {:.3f} Å-1\t({} at Ef, hv={}eV)".format(GX,GXdegString,hv))

			print("\t\u0393-M = \u221A2 \u0393-X \t= {:.3f} Å-1\t({} at Ef, hv={}eV)".format(GM,GMdegString,hv))

		if structure == 'cubic-fcc' and surface=='(111)':	
			a_surface =  a/math.sqrt(2)
			GM = 2*math.pi/(math.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))

			print("\n\tIn-plane surface lattice constant \t= sqrt(2)*a \t= {:.3f} Å".format(a_surface))
			print("\tMonoatomic step height\t\t\t= a*sqrt(3)/3 \t= {:.3f} Å".format(a*np.sqrt(3)/3))

			print("\n\t\u0393-M \t= 2pi/(sqrt(3)*a_111)\t= {0:.3f} Å-1".format(GM))
			print("\t\u0393-K \t= \u0393-M/cos(30) \t\t= {0:.3f} Å-1".format(GK))
			print("\tK-M \t= tan(30)\u0393-M \t\t= {0:.3f} Å-1".format(KM))

		if structure == 'cubic-fcc' and surface=='(110)':
			a1 = a
			a2 = a/math.sqrt(2)

			GX = math.pi*math.sqrt(2) / a
			GY = math.pi/ a
			GS = math.sqrt(GX**2 + GY**2)

			print("\n\tIn-plane surface lattice constants:\ta1 = a ={:.3f} Å, a2=a/\u221A2 = {:.3f} Å".format(a1,a2))
			print("\n\t\u0393-X = \u03c0/a2 \t\t= {0:.3f} Å-1".format(GX))
			print("\t\u0393-Y = \u03c0/a1 \t\t= {0:.3f} Å-1".format(GY))
			print("\t\u0393-S = \u221A(\u0393X^2 + \u0393Y^2)\t= {0:.3f} Å-1".format(GS))

		if structure == 'cubic-bcc' and surface=='(100)':
			a_surface = a
			GX = np.pi/a_surface
			GM = math.sqrt(2)*GX
			print("\n\tIn-plane surface lattice constant\t= a \t= {:.3f} Å".format(a))
			print("\tMonoatomic spacing\t\t\t= a/2 \t= {:.3f} Å".format(a/2))
			print("\n\t\u0393-X = \u03c0/a_001 \t= {0:.3f} Å-1".format(GX))
			print("\t\u0393-M = \u221A2 \u0393-X \t= {0:.3f} Å-1".format(GM))

		if structure == 'cubic-bcc' and surface=='(111)':
			a_surface =  math.sqrt(2)*a
			GM = 2*math.pi/(np.sqrt(3)*a_surface)
			GK = GM/math.cos(math.radians(30))
			KM = GM*math.tan(math.radians(30))

			print("\n\tIn-plane surface lattice constant \t= sqrt(2)*a \t= {:.3f} Å".format(a_surface))
			print("\tMonoatomic step height\t\t\t= a*sqrt(3)/3 \t= {:.3f} Å".format(a*np.sqrt(3)/3))

			print("\n\t\u0393-M \t= 2pi/(sqrt(3)*a_111)\t= {0:.3f} Å-1".format(GM))
			print("\t\u0393-K \t= \u0393-M/cos(30) \t\t= {0:.3f} Å-1".format(GK))
			print("\tK-M \t= tan(30)\u0393-M \t\t= {0:.3f} Å-1".format(KM))

		if structure == 'hexagonal' and surface=='(0001)':
			GM = 2*math.pi/(np.sqrt(3)*a)
			GK = GM/np.cos(np.deg2rad(30))
			KM = GM*np.tan(np.deg2rad(30))

			GKdeg = k_to_polar_manipulator(kx=GK,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-ANALYZER_WORKFUNCTION)		
			if np.isnan(GKdeg): GKdegString = "inaccessible"
			else: GKdegString = "{:.1f}\u00B0 off normal".format(GKdeg)

			GMdeg = k_to_polar_manipulator(kx=GM,ky=0,polar_offset=0,tilt_offset=0,Ek=hv-ANALYZER_WORKFUNCTION)
			if np.isnan(GMdeg): GMdegString = "inaccessible"
			else: GMdegString = "{:.1f}\u00B0 off normal".format(GMdeg)

			print("\t\u0393-M \t= 2\u03c0/a\u221A3 \t= {:.3f} Å-1\t({} at Ef, hv={}eV)".format(GM,GMdegString,hv))
			print("\t\u0393-K \t= \u0393-M/cos(30) \t= {:.3f} Å-1\t({} at Ef, hv={}eV)".format(GK,GKdegString,hv))
			print("\tK-M \t= tan(30)\u0393-M \t= {0:.3f} Å-1".format(KM))	

	box_layout = ipywidgets.widgets.Layout(
		border='dashed 1px gray',
		margin='0px 10px 10px 0px',
		padding='5px 5px 5px 5px',
		width='700px')



	structureSelector = ipywidgets.widgets.Dropdown(
		options=['cubic-fcc','cubic-bcc','hexagonal'],
		value='cubic-fcc',
		description='Lattice')


	surfaceSelector = ipywidgets.widgets.Dropdown(
		options=['(100)','(111)','(110)'],
		value='(100)',
		description='Surface')


	lattice_entries={}
	lattice_entries['a']=ipywidgets.widgets.BoundedFloatText(
								value=1,
								min=0,
								max=10,
								step=0.001,
								description='a',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px')
								)	
	lattice_entries['b']=ipywidgets.widgets.BoundedFloatText(
								value=1,
								min=0,
								max=10,
								step=0.001,
								disabled=True,
								description='b',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px')
								)	
	lattice_entries['c']=ipywidgets.widgets.BoundedFloatText(
								value=1,
								min=0,
								max=10,
								step=0.001,
								disabled=True,
								description='c',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px')
								)	

	photonEnergy=ipywidgets.widgets.BoundedFloatText(
								value=20,
								min=5,
								max=250,
								step=0.1,
								disabled=False,
								description='hv',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px')
								)	
	sketch_output = ipywidgets.widgets.interactive_output(SBZ_plot,{
		'structure':structureSelector,
		'surface':surfaceSelector,
		'a':lattice_entries['a'],
		'b':lattice_entries['b'],
		'c':lattice_entries['c']})


	text_output = ipywidgets.widgets.interactive_output(SBZ_text,{
		'structure':structureSelector,
		'surface':surfaceSelector,
		'a':lattice_entries['a'],
		'b':lattice_entries['b'],
		'c':lattice_entries['c'],
		'hv':photonEnergy})

	def structureUpdated(change):
		if change['new'] in ['cubic-fcc','cubic-bcc']:
			lattice_entries['b'].disabled=True
			lattice_entries['c'].disabled=True
			if change['new']=='cubic-fcc':
				surfaceSelector.options=['(100)','(111)','(110)']
				surfaceSelector.value=surfaceSelector.options[0]
			else:
				surfaceSelector.options=['(100)','(111)']
				surfaceSelector.value=surfaceSelector.options[0]				
		elif change['new'] in ['hexagonal']:
			lattice_entries['b'].disabled=True
			lattice_entries['c'].disabled=False
			surfaceSelector.options=['(0001)']
			surfaceSelector.value=surfaceSelector.options[0]
		#elif change['new']=='orthorhombic':
		#	lattice_entries['b'].disabled=False
		#	lattice_entries['c'].disabled=False
		#	surfaceSelector.options=['(001)','(111)','(110)']
		#	surfaceSelector.value=surfaceSelector.options[0]			

	structureSelector.observe(structureUpdated, names='value')
	structure_panel = ipywidgets.widgets.VBox([structureSelector,surfaceSelector,lattice_entries['a'],lattice_entries['b'],lattice_entries['c'],photonEnergy],layout=box_layout)
	output_panel = ipywidgets.widgets.HBox([sketch_output,text_output])
	metaPanel = ipywidgets.widgets.VBox([structure_panel,output_panel],layout=ipywidgets.Layout(width='1000px'))

	return metaPanel



def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

def find(reg,linhas):
    #cria a lista que vai ser retornada como resultado da funcao com a palavra e seu valor
    busca_resultado=[]
    #for para varrer todas as linhas, o valor de i indica qual á linha em linhas[i]
    for i in range(len(linhas)):
        #for para varrer cada linha a procura da palavra buscada
        for item in linhas[i]:
            #verifica se o registro esta na linha
            if item == reg:
                #este for e para varrer novamente a linha se achar o registro para gravar todos os valores da linha em uma lista
                for item in linhas[i]:
                    if item != reg:
                        busca_resultado.append(item)
    return busca_resultado

def find_n_line(reg,linhas):
    #cria a lista que vai ser retornada como resultado da funcao com a palavra e seu valor
    busca_resultado=[]
    #for para varrer todas as linhas, o valor de i indica qual á linha em linhas[i]
    j=0
    for i in range(0,len(linhas)):
        #for para varrer cada linha a procura da palavra buscada
        for item in linhas[i]:
            #verifica se o registro esta na linha
            if item == reg:
                #este for e para varrer novamente a linha se achar o registro para gravar todos os valores da linha em uma lista
                    busca_resultado.append(j)
        j+=1
    return busca_resultado

def open_file(name):                                    #function that transform file in to list. input name: path and the name of the file.
    file = open(name,'r',encoding='utf-8',
                 errors='ignore')                               #open the file.
    file_list = []                                      #creat a list that will be full filed with the file with a line as a list element.
    for line in file:                                   #open a loop that cover the file.
        line = line.strip('\n')                         #drop out all '\n' contained in every line.
        line = line.split()                             #change the spaces for a element of a list, ex: 'the energy is' --> ['the','energy','is'].
        file_list.append(line)                          #add the line in the list file_list.
    file.close()                                        #close de file.
    return file_list                                    #return file_list as output, the list where every element is a line of the vanila file and every element is a list with every word of the line.

def to_matrix2(file_arpes_exist,file_arpes_dir,file_arpes_name,file_arpes_name_pp,parameter):
        if file_arpes_exist == False:
            file_arpes_raw = open_file(file_arpes_dir + file_arpes_name)
            parameter = '"'+parameter
            line_tilt = find_n_line(parameter,file_arpes_raw)                 #create a list with every line number that contai the information about the tilt angle
            #line_tilt = find_n_line('"tilt',file_arpes_raw)                 #create a list with every line number that contai the information about the tilt angle
            for i in range(len(line_tilt)):                         #open a loop that cover the indices of list line_tilt
               if i == 0:                                          #this conditional exist to create a dictinary that contains the tilt and the line number
                   tilt_dict = {}                                  #create a dictionary
                   tilt_line = file_arpes_raw[line_tilt[0]]                  #list that contain the for the first tilt angle
                   cicle = '0'                            #cicle in the file indicate the tilt angle, ex: cycle 0 is the first tilt, cycle 1 is the second tilt.
                   tilt = float(tilt_line[len(tilt_line)-1])       #grab the tilt value 
                   tilt_dict[0] = round(tilt,2)                             #burn the tilt on the dictionary with the key been the cyclye number
               else:
                   tilt_line = file_arpes_raw[line_tilt[i]]                  #list that contain the for the i-essimo tilt angle
                   cicle = i                        #cicle in the file indicate the tilt angle, ex: cycle 0 is the first tilt, cycle 1 is the second tilt.
                   tilt = float(tilt_line[len(tilt_line)-1])       #grab the tilt value 
                   tilt_dict[i] = round(tilt,2)                             #burn the tilt on the dictionary with the key been the cyclye number
            tilt_cycle = tilt_dict
            
            w =[]
            for tilt in range(len(tilt_cycle)-1):
                count = 0                                                                   #marker that is used to pull over all energy values pro one y value, this marker will be the line number
                y_dict = {}                                                                 #dictionary where the line number of y is the key and the y value is the value for that key
                for line in file_arpes_raw:                                                           #create a loop for every line in the file
                    if len(line) == 5:                                                      # we only need lines that have 5 elements because the line thar ontins de Curve only have 5 elements.
                        if line[1] == 'Cycle:' and line[2] == str(tilt) + ',':             #the line that contains the y value has the second element 'Cycle:' and the third element ex: '0,', indicated which tilt angle for this
                            y_dict[count+1] = round(float(file_arpes_raw[count+2][2]),3)                        #we add the y_value with the line number been the key
                    count+=1
                y_array = np.array(list(y_dict.values()),dtype = float)
                y_n_line_array = np.array(list(y_dict.keys()),dtype = int)
                if tilt == 0:
                    n_E_old = y_n_line_array[1] - y_n_line_array[0]
                for j in range(len(y_array)): 
                    index = 0
                    for i in range(y_n_line_array[j],y_n_line_array[j]+n_E_old):
                        if len(file_arpes_raw[i]) >=1 and file_arpes_raw[i][0] != '#':
                            w.append(np.array([y_array[j],file_arpes_raw[i][0],tilt_cycle[tilt],file_arpes_raw[i][1]],dtype= float))   #add new line on dataframe
                            index+=1
                    if j == 0:
                        n_E = index
                        n_y = len(y_array)
                        n_tilt = len(tilt_cycle)-1
                print('Cycle %s, Tilt angle: %s' %(tilt,tilt_dict[tilt]))
            matrix = w
            n_tilt = n_tilt
            n_emission_angle = n_y
            n_energy = n_E
            
            Ekccd = float(find('Kinetic',file_arpes_raw)[6])
            E_photon = float(find('Excitation',file_arpes_raw)[2])
            Ep = float(find('Pass',file_arpes_raw)[2])
            lens = find('Lens:',file_arpes_raw)[2]
            Lens = ''
            for car in lens:
                if car == ':':
                    break
                else:
                    Lens+=car
            E_work = float( find('Workfunction:',file_arpes_raw)[2])

            print('Energy kinetic ccd: %s eV \n' %Ekccd)
            print('Energy Excitation Energy: %s eV \n' %E_photon)
            print('Pass Energy: %s eV \n' %Ep)
            print('Analyzer Lens: %s \n' %Lens)
            print('Workfunction: %s eV \n' %E_work)
 
        
            new_name = file_arpes_dir + file_arpes_name_pp
            file_arpes = open(new_name,'w')
            file_arpes.writelines('# Excitation Energy: ' + str(E_photon) +   '\n')
            file_arpes.writelines('# Kinetic Energy:   ' + str(Ekccd) +   '\n')
            file_arpes.writelines('# Pass Energy:        ' + str(Ep) +   '\n')
            file_arpes.writelines('# Eff. Workfunction:   ' + str(E_work) +   '\n')
            file_arpes.writelines('# Analyzer Lens:   ' + str(Lens ) +   '\n')
            file_arpes.writelines('# Number os elements \n')
            file_arpes.writelines('# n_tilt    n_emission  n_energy  \n')
            line = '# '
            for item in (n_tilt,n_emission_angle,n_energy):
                line+= str(item)+ '     '
            line +='\n'
            file_arpes.writelines(line)
            file_arpes.writelines('# emission_angle   kinect_energy   tilt_angle  count \n')
            for j in range(len(matrix)):
                line = ''
                for item in matrix[j]:
                    line+= str(item)+ '     '
                line +='\n'
                file_arpes.writelines(line)
            file_arpes.close()
			
            print('File arpes created.')
            
            return [matrix,n_tilt,n_emission_angle,n_energy,[E_photon,Ekccd,Ep,E_work,Lens]]
        
        elif file_arpes_exist == True:
            with open(file_arpes_dir+file_arpes_name_pp, 'r', encoding='utf-8') as file:
                lines = file.readlines()                      #open the file.
            file_list = []                                  #creat a list that will be full filed with the file with a line as a list element.
            index = 1
            for line in lines:                                   #open a loop that cover the file.
                line = line.strip('\n')                         #drop out all '\n' contained in every line.
                line = line.split()
                if line[0] == '#':
                    if line[1] == 'n_tilt':
                        l = lines[index].strip('\n')
                        l = l.split()
                        number_list = np.array(l[1:],dtype = int)
                else:
                    file_list.append(np.array(line,dtype=float))                          #add the line in the list file_list.
                index +=1
    
            file.close()                                        #close de file.
            
            
            matrix = file_list
            n_tilt = number_list[0]
            n_emission_angle = number_list[1]
            n_energy = number_list[2]
            
            file_arpes_pp = open_file(file_arpes_dir+file_arpes_name_pp)
            Ekccd = float(find('Kinetic',file_arpes_pp)[2])
            E_photon = float(find('Excitation',file_arpes_pp)[2])
            Ep = float(find('Pass',file_arpes_pp)[2])
            lens = find('Lens:',file_arpes_pp)[2]
            Lens = ''
            for car in lens:
                if car == ':':
                    break
                else:
                    Lens+=car
            E_work = float( find('Workfunction:',file_arpes_pp)[2])

            print('Energy kinetic ccd: %s eV \n' %Ekccd)
            print('Energy Excitation Energy: %s eV \n' %E_photon)
            print('Pass Energy: %s eV \n' %Ep)
            print('Analyzer Lens: %s \n' %Lens)
            print('Workfunction: %s eV \n' %E_work) 
            print('File loaded susccefully. ')
            return [matrix,n_tilt,n_emission_angle,n_energy,[E_photon,Ekccd,Ep,E_work,Lens]]
        else:
            print('file_arpes_exist is not correctly fullfiled.')
			
def to_matrix(file_arpes_exist,file_arpes_raw,file_arpes_name,parameter):
        if file_arpes_exist == False:
            #file_arpes_raw = open_file(file_arpes_name)
            #parameter = '"'+parameter
            line_tilt = find_n_line(parameter,file_arpes_raw)                 #create a list with every line number that contai the information about the tilt angle
            #line_tilt = find_n_line('"tilt',file_arpes_raw)                 #create a list with every line number that contai the information about the tilt angle
            for i in range(len(line_tilt)):                         #open a loop that cover the indices of list line_tilt
               if i == 0:                                          #this conditional exist to create a dictinary that contains the tilt and the line number
                   tilt_dict = {}                                  #create a dictionary
                   tilt_line = file_arpes_raw[line_tilt[0]]                  #list that contain the for the first tilt angle
                   cicle = '0'                            #cicle in the file indicate the tilt angle, ex: cycle 0 is the first tilt, cycle 1 is the second tilt.
                   tilt = float(tilt_line[len(tilt_line)-1])       #grab the tilt value 
                   tilt_dict[0] = round(tilt,2)                             #burn the tilt on the dictionary with the key been the cyclye number
               else:
                   tilt_line = file_arpes_raw[line_tilt[i]]                  #list that contain the for the i-essimo tilt angle
                   cicle = i                        #cicle in the file indicate the tilt angle, ex: cycle 0 is the first tilt, cycle 1 is the second tilt.
                   tilt = float(tilt_line[len(tilt_line)-1])       #grab the tilt value 
                   tilt_dict[i] = round(tilt,2)                             #burn the tilt on the dictionary with the key been the cyclye number
            tilt_cycle = tilt_dict
            
            w =[]
            for tilt in range(len(tilt_cycle)-1):
                count = 0                                                                   #marker that is used to pull over all energy values pro one y value, this marker will be the line number
                y_dict = {}                                                                 #dictionary where the line number of y is the key and the y value is the value for that key
                for line in file_arpes_raw:                                                           #create a loop for every line in the file
                    if len(line) == 5:                                                      # we only need lines that have 5 elements because the line thar ontins de Curve only have 5 elements.
                        if line[1] == 'Cycle:' and line[2] == str(tilt) + ',':             #the line that contains the y value has the second element 'Cycle:' and the third element ex: '0,', indicated which tilt angle for this
                            y_dict[count+1] = round(float(file_arpes_raw[count+2][2]),3)                        #we add the y_value with the line number been the key
                    count+=1
                y_array = np.array(list(y_dict.values()),dtype = float)
                y_n_line_array = np.array(list(y_dict.keys()),dtype = int)
                if tilt == 0:
                    n_E_old = y_n_line_array[1] - y_n_line_array[0]
                for j in range(len(y_array)): 
                    index = 0
                    for i in range(y_n_line_array[j],y_n_line_array[j]+n_E_old):
                        if len(file_arpes_raw[i]) >=1 and file_arpes_raw[i][0] != '#':
                            w.append(np.array([y_array[j],file_arpes_raw[i][0],tilt_cycle[tilt],file_arpes_raw[i][1]],dtype= float))   #add new line on dataframe
                            index+=1
                    if j == 0:
                        n_E = index
                        n_y = len(y_array)
                        n_tilt = len(tilt_cycle)-1
                print('Cycle %s, %s angle: %s' %(tilt,parameter[1:],tilt_dict[tilt]))
            matrix = w
            n_tilt = n_tilt
            n_emission_angle = n_y
            n_energy = n_E
            
            Ekccd = float(find('Kinetic',file_arpes_raw)[6])
            E_photon = float(find('Excitation',file_arpes_raw)[2])
            Ep = float(find('Pass',file_arpes_raw)[2])
            lens = find('Lens:',file_arpes_raw)[2]
            Lens = ''
            for car in lens:
                if car == ':':
                    break
                else:
                    Lens+=car
            E_work = float( find('Workfunction:',file_arpes_raw)[2])

            print('Energy kinetic ccd: %s eV \n' %Ekccd)
            print('Energy Excitation Energy: %s eV \n' %E_photon)
            print('Pass Energy: %s eV \n' %Ep)
            print('Analyzer Lens: %s \n' %Lens)
            print('Workfunction: %s eV \n' %E_work)
 
            metadat = metadata(file_arpes_raw)
            new_name = file_arpes_name[:-3]+'.ARPES'
            file_arpes = open(new_name,'w')
            for lines in metadat:
                line = '#'
                for item in lines:
                    line+=item +' '
                line += line +'\n'
                file_arpes.writelines(line)
            file_arpes.writelines("# end_metadata \n")

            file_arpes.writelines('# Excitation Energy: ' + str(E_photon) +   '\n')
            file_arpes.writelines('# Kinetic Energy:   ' + str(Ekccd) +   '\n')
            file_arpes.writelines('# Pass Energy:        ' + str(Ep) +   '\n')
            file_arpes.writelines('# Eff. Workfunction:   ' + str(E_work) +   '\n')
            file_arpes.writelines('# Analyzer Lens:   ' + str(Lens ) +   '\n')
            file_arpes.writelines('# Number os elements \n')
            file_arpes.writelines('# n_tilt    n_emission  n_energy  \n')
            line = '# '
            for item in (n_tilt,n_emission_angle,n_energy):
                line+= str(item)+ '     '
            line +='\n'
            file_arpes.writelines(line)
            file_arpes.writelines('# emission_angle   kinect_energy   tilt_angle  count \n')
            for j in range(len(matrix)):
                line = ''
                for item in matrix[j]:
                    line+= str(item)+ '     '
                line +='\n'
                file_arpes.writelines(line)
            file_arpes.close()
			
            print('File arpes created.')
            
            return [matrix,n_tilt,n_emission_angle,n_energy,[E_photon,Ekccd,Ep,E_work,Lens],metadat]
        
        elif file_arpes_exist == True:
            with open(file_arpes_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()                      #open the file.
            file_list = []                                  #creat a list that will be full filed with the file with a line as a list element.
            index = 1
            head = []
            for line in lines:                                   #open a loop that cover the file.
                line = line.strip('\n')                         #drop out all '\n' contained in every line.
                line = line.split()
                if line[0] == '#':
                    if line[1] == 'n_tilt':
                        l = lines[index].strip('\n')
                        l = l.split()
                        number_list = np.array(l[1:],dtype = int)
                    head.append(line)
                elif line[0] == '##':
                    pass
                else:
                    file_list.append(np.array(line,dtype=float))                          #add the line in the list file_list.
                index +=1
    
            file.close()                                        #close de file.
            

            metadat = metadata(file_arpes_raw)
            matrix = file_list
            n_tilt = number_list[0]
            n_emission_angle = number_list[1]
            n_energy = number_list[2]
            
     
            Ekccd = float(find('Kinetic',head)[2])
            E_photon = float(find('Excitation',head)[2])
            Ep = float(find('Pass',head)[2])
            lens = find('Lens:',head)[2]
            Lens = ''
            for car in lens:
                if car == ':':
                    break
                else:
                    Lens+=car
            E_work = float( find('Workfunction:',head)[2])

            print('Energy kinetic ccd: %s eV \n' %Ekccd)
            print('Energy Excitation Energy: %s eV \n' %E_photon)
            print('Pass Energy: %s eV \n' %Ep)
            print('Analyzer Lens: %s \n' %Lens)
            print('Workfunction: %s eV \n' %E_work) 
            print('File loaded susccefully. ')
            return [matrix,n_tilt,n_emission_angle,n_energy,[E_photon,Ekccd,Ep,E_work,Lens],metadat]
        else:
            print('file_arpes_exist is not correctly fullfiled.')

def Shape(M):
    marker = False
    ct = 1
    n = M[0]
    while marker == False:
        if type(n)==list or type(n)==np.ndarray:
            n=n[0]
            ct+=1
        else:
            marker = True
    return ct


def change_matrix(Z_1,n_energy,n_emission_angle,n_tilt):
	z1new = []
	for i in range(n_energy):
		col1 = []
		for j in range(n_emission_angle):
			col2 = []
			for k in range(n_tilt):
				col2.append(Z_1[k][j][n_energy- i-1])
			col1.append(col2)
		z1new.append(col1)
	return z1new

def Process(matrix,n_tilt,n_emission_angle ,n_energy ):                                                                    #this class is relative to treatement of the raw data in to a better analize format 
        
        X =[]; Y=[];  Z_l = []; W = []
        for k in range(n_tilt):
            Z=[]
            for j in range(n_emission_angle):
                z=[]
                for i in range(n_energy ):
                    if j == 0 and k ==0 :
                        Y.append(matrix[i+j*n_energy +k*n_emission_angle*n_energy ][1])
                    z.append(matrix[i+j*n_energy +k*n_emission_angle*n_energy ][3])
                if k == 0:
                    X.append(matrix[j*n_energy +k*n_emission_angle*n_energy ][0])
                Z.append(np.array(z))
            Z_l.append(np.array(Z))
            W.append(matrix[j*n_energy +k*n_emission_angle*n_energy ][2])
        #print('y', 'energy','tilt', 'count')
        emission_angle = np.array(X,dtype = float)
        kinect_energy_temp = np.array(Y,dtype = float)
        kinect_energy = []
        for i in range(n_energy):
            kinect_energy.append(kinect_energy_temp[n_energy-i-1])
        kinect_energy = np.array(kinect_energy)
        tilt_angle = np.array(W,dtype = float)
        z1new = change_matrix(Z_l,n_energy,n_emission_angle,n_tilt)
        matrix3D = np.array(z1new,dtype = float)
        data = {'Metadata':[],'Axis':[kinect_energy,emission_angle,tilt_angle],'AxisLabel':['Kinect Energy','Emission angle','Deflector Angle'],'AxisUnits':['eV','$\\degree$','$\\degree$'],'data':matrix3D}
        return data

def metadata(file):
    for i in range(len(file)):
        if len(file[i])>=2 and file[i][1] == 'Cycle:':
            ct = i
            break
        elif len(file[i])>=2 and file[i][1] == 'end_metadata':
            ct = i
            break	
    return file[:ct]

def load_spectrum2(name_input='input_arpes.txt'):                                                        #load the input file
        
        input_file_name = name_input
    
        input_file = open_file(input_file_name)

        file_arpes_exist = strtobool(find('file_arpes_exist',input_file)[1])
        if file_arpes_exist:
            file_arpes_name = find('file_name_pp',input_file)[1][:-4]+'ARPES'
        
            file_arpes_name_pp = find('file_name_pp',input_file)[1]
        else:
            file_arpes_name = find('file_name',input_file)[1]
            file_arpes_name_pp = find('file_name',input_file)[1][:-4]+'ARPES'
            metadat= metadata(input_file)
			

        file_arpes_dir = find('file_dir',input_file)[1]
        
        file_parameter = find('cicle_parameter_(ShiftX_or_tilt)',input_file)[1]
    
        
        matrix,tilt,n_emission_angle,n_energy,par = to_matrix(file_arpes_exist,file_arpes_dir,file_arpes_name,file_arpes_name_pp,file_parameter)
        #matrix,tilt,n_emission_angle,n_energy,par =matrix,tilt,n_emission_angle,n_energy,par 
        print(ANALYZER_WORKFUNCTION )
        updateWorkfunction(par[3])
        print(ANALYZER_WORKFUNCTION )
        data = Process(matrix,tilt,n_emission_angle ,n_energy )
        return data


def load_spectrum(name_input):                                                        #load the input file
        
        input_file = open_file(name_input)
        if name_input.endswith('.xy'): 
            parameter = '"tilt'; marker = False
            file_arpes_exist = False
            for line in input_file:
                for item in line:
                    if 'ShiftX' in item:
                        parameter = '"ShiftX'
                        marker = True
                        break
                if marker == True:
                    break
    
        elif name_input.endswith('.ARPES') or name_input.endswith('.arpes'):
            file_arpes_exist = True
            parameter = "ShiftX"
        matrix,tilt,n_emission_angle,n_energy,par,metadat = to_matrix(file_arpes_exist,input_file,name_input,parameter)

        updateWorkfunction(par[3])
        data = Process(matrix,tilt,n_emission_angle ,n_energy )
        data['Metadata'] = metadat
        return data

def drawHighSymmetryLabels(points,axis,fontsize = 12):

	tform = matplotlib.transforms.blended_transform_factory(axis.transData, axis.transAxes)
	yMax,yMin = axis.get_ylim()[1],axis.get_ylim()[0]


	pointsWithinAxis = [x for x in points if (x[1]>=axis.get_xlim()[0] and x[1] <=axis.get_xlim()[1])]
	pointsOutsideLeft=[x for x in points if x[1]<axis.get_xlim()[0]]
	pointsOutsideRight=[x for x in points if x[1]>axis.get_xlim()[1]]

	for line in pointsWithinAxis:
		axis.plot([line[1],line[1]],[yMin,yMax],'--',color='black',lw=0.2)
		axis.text(x=line[1],y=1,s=line[0],va='bottom', ha='center',transform=tform)

	if len(pointsOutsideRight)>0:
		axis.text(1,1,r"$ \rightarrow$"+pointsOutsideRight[0][0],ha='right', va='bottom',transform=axis.transAxes,fontsize=fontsize)

	if len(pointsOutsideLeft)>0:
		axis.text(0,1,pointsOutsideLeft[0][0]+r"$\leftarrow$",ha='left', va='bottom',transform=axis.transAxes,fontsize=fontsize)  	

def interpolation(spectrum,dx = 1000, dy= 1000,filter_sv = False, p =[10,1]):
    def inter_x(x,y,z,dx = dx, dy= dy):
        x = np.array(x);y= np. array(y)
        interp = interpolate.RegularGridInterpolator((x,y),z)
        xnew = np.linspace(x.min(),x.max(),dx)
        ynew = np.linspace(y.min(),y.max(),dy)
        
        M_int = []
        for i in range(len(xnew)):
            pts = []
            for j in range(len(ynew)):
                pts.append([xnew[i],ynew[j]])
            pts = np.array(pts)
            col = interp(pts)
            if filter_sv:
                M_int.append(sv(np.array(col),p[0],p[1]))
            else:
                M_int.append(col)
        return [xnew,ynew,np.array(M_int)]
	
    if Shape(spectrum['data'])==2:
        x,y,z = inter_x(spectrum['Axis'][0],spectrum['Axis'][1],spectrum['data'])
        spectrum['Axis'] = [np.array(list(reversed(x))),y]
        spectrum['data'] = np.array(list(reversed(z)))
        return spectrum
    else:
        print("only for 2D data")

def quickPlot(spectrum,hv=0,axis=None,label=None,cmap='terrain',cmin=None,cmax=None,lw=1,color=None,logscale=False,beQuiet=True):

	assert(Shape(spectrum['data']) < 3), "Expected a 1D or 2D spectrum as input"

	#if beQuiet==False:
		#printMetaData(spectrum)
	
	#if 'Lens Mode' in spectrum['Metadata']:
	#	if spectrum['Metadata']['Lens Mode'] in ["Transmission","HighMagnification2"]:
	#		return quickPlotXPS(spectrum=spectrum,hv=hv,axis=axis,label=label,lw=lw,color=color,logscale=logscale)
	
	#if 'Analyzer' in spectrum['Metadata']:
	#	if spectrum['Metadata']['Analyzer']=="PhoibosSpin":
	#		return pesto.spin.quickPlot(spectrum=spectrum)


	#--------------------------------
	# Line profiles

	#validMeasurementTypes = ['line profile']
	if Shape(spectrum['data'])==1:
		x = spectrum['Axis']
		y = spectrum['data']
		if axis==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = axis


		#If the energy scale is kinetic BUT a photon energy was passed in, plot in binding energy
		if hv!=0 and spectrum['AxisLabel'].startswith("Kinetic"): 
			Eb = [hv-ANALYZER_WORKFUNCTION-ii for ii in x]
			ax.plot(Eb,y,label=label,lw=lw,color=color)
			ax.set_xlabel('Binding energy (eV)')	
			ax.invert_xaxis()

		elif spectrum['AxisLabel'].startswith("Binding"): 
			ax.plot(x,y,label=label,lw=lw,color=color)
			ax.set_xlabel(spectrum['AxisLabel'])
			ax.invert_xaxis()		
		else:
			ax.plot(x,y,label=label,lw=lw,color=color)
			ax.set_xlabel(spectrum['AxisLabel'])
			
		ax.set_ylabel('Intensity (a.u.)')

		if logscale==True:
			ax.set_yscale("log")
		if axis==None:
			matplotlib.pyplot.show()
		return


	#--------------------------------
	# 2D images

	if Shape(spectrum['data'])==2:
		x = spectrum['Axis'][1]
		y = spectrum['Axis'][0]
		

		if logscale==True:
			im = np.log(copy.deepcopy(spectrum['data']))
		else:
			im=spectrum['data']
		if spectrum['AxisUnits'][0]==spectrum['AxisUnits'][1]: aspect='equal'
		else: aspect = 'auto'
		if spectrum['AxisLabel'][1] == 'Photon energy': aspect = 'auto' # You don't want equal aspect ratio in an Eb vs photon energy frame, despite having the same units

		if axis==None: fig,ax=matplotlib.pyplot.subplots(figsize=(7,5))
		else: ax = axis

		if cmin!=None and cmax!=None:
			if cmin>cmax:
				cmin,cmax = cmax,cmin
				if cmap[-2:]=='_r':cmap=cmap[:-2]
				else:cmap=cmap+'_r'	

		# Covert to Eb for the plot if requested and if the energy axis is not already converted
		if hv!=0 and (spectrum['AxisLabel'][0].startswith("Kinetic") or spectrum['AxisLabel'][0].startswith("Ek")):  
			Eb = [hv-ANALYZER_WORKFUNCTION-ii for ii in y]
			ax.imshow(im,clim=[cmin,cmax],aspect=aspect,cmap=cmap,extent=[x[0],x[-1],Eb[-1],Eb[0]])
			ax.set_ylabel('Binding energy (eV)')	
			ax.invert_yaxis()
		elif hv==0 and (spectrum['AxisLabel'][0].startswith("Kinetic") or spectrum['AxisLabel'][0].startswith("Ek")):  
			ax.imshow(im,clim=[cmin,cmax],aspect=aspect,cmap=cmap,extent=[x[0],x[-1],y[-1],y[0]])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))
			ax.invert_yaxis()

		elif(spectrum['AxisLabel'][0].startswith("Binding") or spectrum['AxisLabel'][0].startswith("Eb")): 
			ax.imshow(im,clim=[cmin,cmax],aspect=aspect,cmap=cmap,extent=[x[0],x[-1],y[-1],y[0]])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))
			ax.invert_yaxis()
		else:
			ax.imshow(im,clim=[cmin,cmax],aspect=aspect,cmap=cmap,extent=[x[0],x[-1],y[-1],y[0]])
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0]))


		
		ax.set_xlabel("{} ({})".format(spectrum['AxisLabel'][1],spectrum['AxisUnits'][1]))

		return



	print("quickPlot: Sorry, I don't know how to deal data types of 3+ dimensions")


def getSlice(spectrum,axis,axisValue,sliceIntegration=0,normalized=False,beQuiet=True):


	assert(Shape(spectrum['data']) == 3), "Expected a 3D spectrum as input"
	assert(axis in [0,1,2]), "Invalid 'axis' parameter. Valid axis choices are 0 (typically energy axis), 1 (typically analyzer angle axis) or 2"

	def array_slice(a, axis, start, end, step=1):
		if start==end: end=start+1
		return a[(slice(None),) * (axis % a.ndim) + (slice(start, end, step),)]

	a = np.asarray(spectrum['Axis'][axis])
	if sliceIntegration==0:
		frameIndex = (np.abs(a - axisValue)).argmin()
		image=array_slice(spectrum['data'],axis=axis,start=frameIndex,end=frameIndex)
		image=np.sum(image,axis=axis)

	else:
		value = axisValue-(sliceIntegration/2)
		startFrameIndex = (np.abs(a - value)).argmin()

		value = axisValue+(sliceIntegration/2)
		endFrameIndex = (np.abs(a - value)).argmin()

		if startFrameIndex>endFrameIndex: startFrameIndex,endFrameIndex=endFrameIndex,startFrameIndex

		if beQuiet==False: 		
			print("Requested axisValue {} along axis {} ('{}')".format(axisValue,axis,spectrum['AxisLabel'][axis]))
			print("That axis spans {:.4f} ... {:.4f} and contains {} points".format(a[0],a[-1],len(a)))
			if startFrameIndex == endFrameIndex and sliceIntegration!=0:
				print("Requested integration is too small, only returning a single frame")
			if startFrameIndex == endFrameIndex: print("Extracting frame index {} ({:.4f}) of axis '{}'".format(startFrameIndex,a[startFrameIndex],spectrum['AxisLabel'][axis]))
			else: print("An integration of {} {} means summing over indices {} through {}".format(sliceIntegration,spectrum['AxisUnits'][axis],startFrameIndex,endFrameIndex))

		#image=spectrum['data'].take(indices=range(startFrameIndex, endFrameIndex+1), axis=axis)
		image=array_slice(spectrum['data'],axis=axis,start=startFrameIndex,end=endFrameIndex)

		image=np.sum(image,axis=axis)
		if normalized==True:
			image=image/(1+endFrameIndex-startFrameIndex)

	
	if axis==0: ii,jj = 1,2
	if axis==1: ii,jj = 0,2
	if axis==2: ii,jj = 0,1

	outputSpectrum={}
	outputSpectrum['Axis']=[[],[]]
	outputSpectrum['AxisLabel']=[[],[]]
	outputSpectrum['AxisUnits']=[[],[]]

	outputSpectrum['Metadata']=spectrum['Metadata']


	outputSpectrum['data']=image


	outputSpectrum['Axis'][0]=spectrum['Axis'][ii]
	outputSpectrum['Axis'][1]=spectrum['Axis'][jj]
	outputSpectrum['AxisLabel'][0]=spectrum['AxisLabel'][ii]
	outputSpectrum['AxisLabel'][1]=spectrum['AxisLabel'][jj]
	outputSpectrum['AxisUnits'][0]=spectrum['AxisUnits'][ii]
	outputSpectrum['AxisUnits'][1]=spectrum['AxisUnits'][jj]		

	return outputSpectrum

def secondDerivativeExplorer(spectrum,cmap='terrain'):

	font = {'size'   : 14}
	matplotlib.rc('font', **font)


	def build_explorer_3panel(spectrum,whichAxis,smoothing,cRange):

		if whichAxis=='Energy':
			axis=0
		else:
			axis=1

		cmax=cRange
		cmin=-cRange
		fig,ax=matplotlib.pyplot.subplots(figsize=(12,5),ncols=2) 

		quickPlot(spectrum,axis=ax[0])
		ax[0].set_title("Raw image")
		
		tempSpectrum=copy.deepcopy(spectrum)
		tempSpectrum['data']=scipy.ndimage.uniform_filter1d(tempSpectrum['data'], smoothing, axis)
		
		quickPlot(tempSpectrum,axis=ax[1])
		ax[1].set_title("Smoothed image")
		matplotlib.pyplot.tight_layout()


		
		
		fig,axes=matplotlib.pyplot.subplots(figsize=(12,5),ncols=2) 
		ax=axes[0]
		tempSpectrum['data'] = np.diff(tempSpectrum['data'], n=1,axis=axis)
		quickPlot(tempSpectrum,axis=ax,cmax=cmax,cmin=cmin,cmap=cmap)
		ax.set_title('First derivative')
		ax=axes[1]
		tempSpectrum['data'] = np.diff(tempSpectrum['data'], n=1,axis=axis)
		quickPlot(tempSpectrum,axis=ax,cmax=cmax,cmin=cmin,cmap=cmap)
		ax.set_title('Second derivative')	
		matplotlib.pyplot.tight_layout()	
	
	#print(time.time()-t0)


	e=list(spectrum['Axis'][0])
	a=list(spectrum['Axis'][1])

	style = {'description_width': 'initial'}

	whichAxisToggle=ipywidgets.widgets.ToggleButtons(
	    options=['Energy', 'Angle'],
	    description='Which axis:',
	    disabled=False,
	)

	smoothingSlider=ipywidgets.widgets.IntSlider(
		value=int(round(len(e)/32)),
		min=1,
		max=50,
		step=1,
		description='Smoothing:',
		continuous_update=False,
		layout=ipywidgets.Layout(width='600px')
	)  

	colorSlider=ipywidgets.widgets.FloatSlider(
		value=10,
		min=0,
		max=50,
		step=0.5,
		description='Color range:',
		continuous_update=False,
		layout=ipywidgets.Layout(width='600px'),
		style=style
	)  
 

	w = ipywidgets.interactive(
		build_explorer_3panel,
		spectrum=ipywidgets.fixed(spectrum),
		whichAxis=whichAxisToggle,
		smoothing=smoothingSlider,
		cRange=colorSlider,
	)
   
	# prevent flicker as the cell size goes to zero when redrawing
	output = w.children[-1]
	output.layout.height = '900px'

	return w 


def explorer(spectrum):

	#matplotlib.pyplot.ioff()
	font = {'size'   : 14}
	matplotlib.rc('font', **font)

	def generic(spectrum):

		# You should be initializing the panels once on start, then the call function just updates the figure. 
		# This way plt.subplots only gets called once.


		def explorer_Slice(spectrum,whichAxis,cmin,cmax,xValue,yValue,zValue,xIntegration,yIntegration,zIntegration,cmap):
			
			t0=time.time()

			ti=time.time()
			integration = [xIntegration,yIntegration,zIntegration]
			value = [xValue,yValue,zValue]
			axes = [list(spectrum['Axis'][0]),list(spectrum['Axis'][1]),list(spectrum['Axis'][2])]
			#print("t1 {:.4f}".format(time.time()-ti))



			ti=time.time()
			fig,ax=matplotlib.pyplot.subplots(figsize=(5,8)) #Takes nearly half the total time
			#print("t2 {:.4f}".format(time.time()-ti))


			ti=time.time()
			spectrumSlice=getSlice(spectrum=spectrum,axis=whichAxis,axisValue=value[whichAxis],sliceIntegration=integration[whichAxis],beQuiet=True,normalized=True)
			#print("t3 {:.4f}".format(time.time()-ti))


			#spectrumSlice=getSlice(spectrum=spectrum,axis=0,axisValue=Ek,sliceIntegration=sliceIntegration,normalized=True,beQuiet=True)
			quickPlot(spectrumSlice,axis=ax,cmap=cmap,cmin=cmin,cmax=cmax)
			#print("t4 {:.4f}".format(time.time()-ti))

			# Draw dotted lines to show where the cuts are being taken/integrated

			ti=time.time()
			startVal,endVal=[],[]
			for ii,a in enumerate(axes):
				startFrameIndex = list(a).index(min(a, key=lambda x:abs(x-value[ii]-(integration[ii]/2))))
				endFrameIndex = list(a).index(min(a, key=lambda x:abs(x-value[ii]+(integration[ii]/2))))
				startVal.append(a[startFrameIndex])
				endVal.append(a[endFrameIndex])

			if whichAxis==0:
				ax.set_title('Constant '+spectrum['AxisLabel'][0],color='tab:blue')
				ax.plot([axes[2][0],axes[2][-1]],[startVal[1], startVal[1]], '--',color='tab:green')
				ax.plot([axes[2][0],axes[2][-1]],[endVal[1], endVal[1]], '--',color='tab:green')
				ax.plot([startVal[2], startVal[2]],[axes[1][0],axes[1][-1]], '--',color='tab:orange')
				ax.plot([endVal[2], endVal[2]],[axes[1][0],axes[1][-1]], '--',color='tab:orange')

			if whichAxis==1:
				ax.set_title('Constant '+spectrum['AxisLabel'][1],color='tab:green')
				ax.plot([axes[2][0],axes[2][-1]],[startVal[0], startVal[0]], '--',color='tab:blue')   
				ax.plot([axes[2][0],axes[2][-1]],[endVal[0], endVal[0]], '--',color='tab:blue')   
				ax.plot([startVal[2], startVal[2]],[axes[0][0],axes[0][-1]], '--',color='tab:orange')
				ax.plot([endVal[2], endVal[2]],[axes[0][0],axes[0][-1]], '--',color='tab:orange')


			if whichAxis==2:
				ax.set_title('Constant '+spectrum['AxisLabel'][2],color='tab:orange')
				ax.plot([axes[1][0],axes[1][-1]],[startVal[0], startVal[0]], '--',color='tab:blue')   
				ax.plot([axes[1][0],axes[1][-1]],[endVal[0], endVal[0]], '--',color='tab:blue') 
				ax.plot([startVal[1], startVal[1]],[axes[0][0],axes[0][-1]], '--',color='tab:green')
				ax.plot([endVal[1], endVal[1]],[axes[0][0],axes[0][-1]], '--',color='tab:green') 
			
			#print("t5 {:.4f}".format(time.time()-ti))
			
			ti=time.time()
			fig.canvas.draw()
			#print("t6 {:.4f}".format(time.time()-ti))

			#print("Total: {:.4f} (approx {:.1f} FPS)".format(time.time()-t0,1/(3*(time.time()-t0))))



    
		box_layout = ipywidgets.widgets.Layout(
			border='dashed 1px gray',
			margin='0px 10px 10px 0px',
			padding='5px 5px 5px 5px',
			width='930px')

		#-------- Colorscale panel
		colorMapSelector = ipywidgets.widgets.Dropdown(
		options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr','terrain'],
		value='terrain',
		description='Colormap:',
		)
		colorscale_panel = ipywidgets.widgets.VBox([colorMapSelector],layout=box_layout)

		box_layout = ipywidgets.widgets.Layout(border='dashed 1px gray',margin='0px 10px 10px 0px',padding='5px 5px 5px 5px',width='310px')


		style = {'description_width': 'initial'}

		panel=[{},{},{}]
		fig= []
		axes=[]

		for axis in [0,1,2]:

			ax=list(spectrum['Axis'][axis])
			ax_midpoint = ax[int(len(ax)/2)]
			ax_step = abs(ax[1]-ax[0])	

			panel[axis]['val']=ipywidgets.widgets.SelectionSlider(
									options=[("{:.3f}".format(i),i) for i in ax],
									value=ax_midpoint,
									description='{}'.format(spectrum['AxisLabel'][axis]),
									continuous_update=False,
									layout=ipywidgets.Layout(width='300px'),
									style=style)

			panel[axis]['cmin']=ipywidgets.widgets.FloatSlider(
								value=np.min(spectrum['data']),
								min=np.min(spectrum['data']),
								max=np.max(spectrum['data'])*2,
								step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/400,
								description='ColorMin:',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px'),
								style=style)	

			panel[axis]['cmax']=ipywidgets.widgets.FloatSlider(
								value=np.max(spectrum['data'])*1,
								min=np.min(spectrum['data']),
								max=np.max(spectrum['data'])*2,
								step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/400,
								description='ColorMax:',
								continuous_update=False,
								layout=ipywidgets.Layout(width='300px'),
								style=style)
			panel[axis]['integration']=ipywidgets.widgets.FloatSlider(
										value=0,
										min=0,
										max=500*ax_step,
										step=2*ax_step,
										description='Integration ({})'.format(spectrum['AxisUnits'][axis]),
										layout=ipywidgets.Layout(width='300px',description_width='100px'),
										continuous_update=False,
			


										style=style)	
		for axis in [0,1,2]:

			#f,a=matplotlib.pyplot.subplots(figsize=(4,4))
			#fig.append(f)
			#axes.append(a)
			panel[axis]['output']=ipywidgets.widgets.interactive_output(explorer_Slice,{
									'spectrum':ipywidgets.fixed(spectrum),
									'whichAxis':ipywidgets.fixed(axis),
									'cmin':panel[axis]['cmin'],
									'cmax':panel[axis]['cmax'],
									'xValue':panel[0]['val'],
									'yValue':panel[1]['val'],
									'zValue':panel[2]['val'],
									'xIntegration':panel[0]['integration'],
									'yIntegration':panel[1]['integration'],
									'zIntegration':panel[2]['integration'],
									'cmap':colorMapSelector
									})
			panel[axis]['widget'] = ipywidgets.widgets.VBox([panel[axis]['output'],panel[axis]['val'],panel[axis]['cmin'],panel[axis]['cmax'],panel[axis]['integration']],layout=box_layout)
			#panel[axis]['widget'].children[0].layout.height = '450px'

			panel[axis]['widget'].children[0].layout.height = '450px'
		outputPanel = ipywidgets.widgets.HBox([panel[0]['widget'],panel[1]['widget'],panel[2]['widget']],layout=ipywidgets.Layout(width='1000px'))
		metaPanel = ipywidgets.widgets.VBox([colorscale_panel,outputPanel],layout=ipywidgets.Layout(width='1000px'))

		return metaPanel

	def Manipulator_2D_explorer(spectrum):
		font = {'size'   : 14}
		matplotlib.rc('font', **font)

		def build_explorer_panel(spectrum,majorVal,minorVal,signalenergy,signalangle,averaging,mapcrange,framecrange,cmap):

			cmin,cmax=mapcrange[0],mapcrange[1]
			framecmin,framecmax=framecrange[0],framecrange[1]

			majorAxis = list(spectrum['majorAxis'])
			majorAxisStep=abs(majorAxis[1]-majorAxis[0])
			minorAxis = list(spectrum['minorAxis'])
			minorAxisStep=abs(minorAxis[1]-minorAxis[0])
			if minorAxis[0]>minorAxis[-1]: minorAxisMin,minorAxisMax=minorAxis[-1],minorAxis[0]
			else: minorAxisMin,minorAxisMax=minorAxis[0],minorAxis[-1]

			if majorAxis[0]>majorAxis[-1]: majorAxisMin,majorAxisMax=majorAxis[-1],majorAxis[0]
			else: majorAxisMin,majorAxisMax=majorAxis[0],majorAxis[-1]


			fig,axis=matplotlib.pyplot.subplots(figsize=(15,7),ncols=2) 

			#------ Plot a single detector frame
			ax=axis[1]	
			
			x=list(spectrum['Axis'][0])
			y=list(spectrum['Axis'][1])

			majorIndex=majorAxis.index(majorVal)
			minorIndex=minorAxis.index(minorVal)

			ax.imshow(spectrum['data'][:,:,minorIndex,majorIndex],aspect='auto',cmap='gray_r',extent=[y[0],y[-1],x[-1],x[0]],clim=[framecmin,framecmax])
			ax.invert_yaxis()	
			ax.set_xlabel("{} ({})".format(spectrum['AxisLabel'][1],spectrum['AxisUnits'][1])) 
			ax.set_ylabel("{} ({})".format(spectrum['AxisLabel'][0],spectrum['AxisUnits'][0])) 
			ax.set_title("Detector frame")

			#ROI=matplotlib.patches.Rectangle((ROIx-ROIxSize/2,ROIy-ROIySize/2), width=ROIxSize, height=ROIySize, angle=0,linestyle='-',color='tab:red',fill=False,lw=2)
			#ax.add_patch(ROI)  
			ax.axvline(x=signalangle,color='tab:red') 
			ax.axhline(y=signalenergy,color='tab:red') 
			averaging_y=abs(x[averaging]-x[0])
			averaging_x=abs(y[averaging]-y[0])

			ROI=matplotlib.patches.Rectangle((signalangle-averaging_x,signalenergy-averaging_y), height=averaging_y*2, width=averaging_x*2, angle=0,linestyle='-',color='tab:red',fill=False)
			ax.add_patch(ROI)   


			signalenergyIndex=x.index(signalenergy)
			signalangleIndex=y.index(signalangle)

			
			#------ Plot the map
			ax=axis[0]

			image = np.zeros([Shape(spectrum['data'])[2],Shape(spectrum['data'])[3]])
			for ii in range(len(majorAxis)):
				for jj in range(len(minorAxis)):
					signal = np.sum(np.asarray(spectrum['data'])[signalenergyIndex-averaging:signalenergyIndex+averaging,signalangleIndex-averaging:signalangleIndex+averaging,jj,ii])
					image[jj,ii]=signal

			if np.max(image)>0:
				image=image/np.max(image)

			image_flipped=np.flip(image,axis=1)
			if majorAxis[0]>majorAxis[1]: image_flipped=np.flip(image_flipped,axis=1)

			if minorAxis[0]>minorAxis[1]: image_flipped=np.flip(image_flipped,axis=0)
			im=ax.imshow(image_flipped.T,aspect='equal',cmap=cmap,extent=[minorAxisMin-(minorAxisStep/2),minorAxisMax+(minorAxisStep/2),majorAxisMin-(majorAxisStep/2),majorAxisMax+(majorAxisStep/2)],clim=[cmin,cmax])
			fig.colorbar(im,ax=ax)


			# Draw horizontal and vertical crosshairs

			ax.axvline(x=minorVal,ls='--')
			ax.axhline(y=majorVal,ls='--')
			ROI=matplotlib.patches.Rectangle((minorVal-(minorAxisStep/2),majorVal-(majorAxisStep/2)), height=minorAxisStep, width=majorAxisStep,linestyle='-',color='tab:red',fill=False,lw=2)
			ax.add_patch(ROI)   
			#ax.plot([majorVal,majorVal],[minorAxisMin,minorAxisMax])
			#ax.plot([majorAxisMin,majorAxisMax],[minorVal,minorVal])
			ax.set_ylabel("{} ({})".format(spectrum['majorAxisLabel'],spectrum['AxisUnits'][2]))
			ax.set_xlabel("{} ({})".format(spectrum['minorAxisLabel'],spectrum['AxisUnits'][3]))
			ax.ticklabel_format(useOffset=False)
			matplotlib.pyplot.tight_layout()
			ax.set_title("Intensity")
			


		majorAxis = list(spectrum['majorAxis'])
		minorAxis = list(spectrum['minorAxis'])

		style = {'description_width': 'initial'}


		majorSlider=ipywidgets.widgets.SelectionSlider(
			options=[("{:.3f}".format(i),i) for i in majorAxis],
			description=spectrum['majorAxisLabel'],
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
			)

		minorSlider=ipywidgets.widgets.SelectionSlider(
			options=[("{:.3f}".format(i),i) for i in minorAxis],
			description=spectrum['minorAxisLabel'],
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
			)



		ax=list(spectrum['Axis'][1])
		ax_midpoint = ax[int(len(ax)/2)]

		signalangleSlider=ipywidgets.widgets.SelectionSlider(options=[("{:.3f}".format(i),i) for i in ax],value=ax_midpoint,description="ROI angle",continuous_update=False,layout=ipywidgets.Layout(width='600px'),style=style)

		ax=list(spectrum['Axis'][0])

		signalenergySlider=ipywidgets.widgets.SelectionSlider(options=[("{:.3f}".format(i),i) for i in ax],value=ax[int(len(ax)*7/9)],description="ROI energy",continuous_update=False,layout=ipywidgets.Layout(width='600px'),style=style)
		averagingSlider=ipywidgets.widgets.SelectionSlider(options=[i for i in range(100)],value=30,description="ROI Integration",continuous_update=False,layout=ipywidgets.Layout(width='600px'),style=style)

		mapcolorSlider=ipywidgets.widgets.FloatRangeSlider(value=[0,2],max=2,step=2/500,description='Map colorscale',continuous_update=False,layout=ipywidgets.Layout(width='600px'),style=style)
		maxVal = np.max(spectrum['data'])
		framecolorSlider=ipywidgets.widgets.FloatRangeSlider(value=[0,maxVal/2],max=maxVal*1.3,step=maxVal*1.3/500,description='Frame colorscale',continuous_update=False,layout=ipywidgets.Layout(width='600px'),style=style)
		
		colorMapSelector = ipywidgets.widgets.Dropdown(options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],value='cividis',description='Colormap:',)


		w = ipywidgets.interactive(
			build_explorer_panel,
			spectrum=ipywidgets.fixed(spectrum),
			majorVal=majorSlider,
			minorVal=minorSlider,

			signalenergy=signalenergySlider,
			signalangle=signalangleSlider,
			averaging=averagingSlider,
			mapcrange=mapcolorSlider,
			framecrange=framecolorSlider,
			cmap = colorMapSelector,
		)
	   
		# prevent flicker as the cell size goes to zero when redrawing
		output = w.children[-1]
		output.layout.height = '700px'

		return w 

	def generic2D(spectrum,hv=0):
		try:
			if spectrum.endswith(".ibw") or spectrum.endswith(".txt"): spectrum=loadSpectrum(spectrum,beQuiet=True)
		except AttributeError: pass
		#--------------------------------
		validMeasurementTypes = ['2D image',
		'energy-deflection image',
		'hv-energy image',
		'angle-hv image',
		'energy-k image',
		'hv-k image',
		'deflector angle-angle image',
		'manipulator angle-angle image',
		'k-k image']

		def buildDisplay(spectrum,cmin,cmax,cmap):
			fig,ax=matplotlib.pyplot.subplots(figsize=(8,5))
			quickPlot(spectrum=spectrum,cmin=cmin,cmax=cmax,cmap=cmap,axis=ax)
			matplotlib.pyplot.show()

		style = {'description_width': 'initial'}
		box_layout = ipywidgets.widgets.Layout(
			border='dashed 1px gray',
			margin='0px 10px 10px 0px',
			padding='5px 5px 5px 5px',
			width='800px')

		colorMinSlider=ipywidgets.widgets.FloatSlider(
			value=np.min(spectrum['data']),
			min=np.min(spectrum['data']),
			max=np.max(spectrum['data'])*2,
			step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
			description='ColorMin:',
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
		)	
		colorMaxSlider=ipywidgets.widgets.FloatSlider(
			value=np.max(spectrum['data'])*1,
			min=np.min(spectrum['data']),
			max=np.max(spectrum['data'])*2,
			step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
			description='ColorMax:',
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
		)
		colorMapSelector = ipywidgets.widgets.Dropdown(
			options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],
			value='bone_r',
			description='Colormap:',
		)

		

		colorscale_panel = ipywidgets.widgets.VBox(
			[colorMinSlider,colorMaxSlider,colorMapSelector],
			layout=box_layout)

		#controlPanel = ipywidgets.widgets.HBox([colorscale_panel])


		out = ipywidgets.widgets.interactive_output(buildDisplay,{
			'spectrum':ipywidgets.fixed(spectrum),
			'cmin':colorMinSlider,
			'cmax':colorMaxSlider,
			'cmap':colorMapSelector,
			})

		metaPanel = ipywidgets.widgets.VBox(
			[out,colorscale_panel],
			layout=ipywidgets.Layout(width='800px')
			)

		#output = metaPanel.children[-1]
		#output.layout.height = '200px'

		return metaPanel



	def generic2D(spectrum,hv=0):
		try:
			if spectrum.endswith(".ibw") or spectrum.endswith(".txt"): spectrum=loadSpectrum(spectrum,beQuiet=True)
		except AttributeError: pass
		#--------------------------------
		validMeasurementTypes = ['2D image',
		'energy-deflection image',
		'hv-energy image',
		'angle-hv image',
		'energy-k image',
		'hv-k image',
		'deflector angle-angle image',
		'manipulator angle-angle image',
		'k-k image']

		def buildDisplay(spectrum,cmin,cmax,cmap):
			fig,ax=matplotlib.pyplot.subplots(figsize=(8,5))
			quickPlot(spectrum=spectrum,cmin=cmin,cmax=cmax,cmap=cmap,axis=ax)
			matplotlib.pyplot.show()

		style = {'description_width': 'initial'}
		box_layout = ipywidgets.widgets.Layout(
			border='dashed 1px gray',
			margin='0px 10px 10px 0px',
			padding='5px 5px 5px 5px',
			width='800px')

		colorMinSlider=ipywidgets.widgets.FloatSlider(
			value=np.min(spectrum['data']),
			min=np.min(spectrum['data']),
			max=np.max(spectrum['data'])*2,
			step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
			description='ColorMin:',
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
		)	
		colorMaxSlider=ipywidgets.widgets.FloatSlider(
			value=np.max(spectrum['data'])*1,
			min=np.min(spectrum['data']),
			max=np.max(spectrum['data'])*2,
			step=(np.max(spectrum['data'])*2-np.min(spectrum['data']))/200,
			description='ColorMax:',
			continuous_update=False,
			layout=ipywidgets.Layout(width='600px'),
			style=style
		)
		colorMapSelector = ipywidgets.widgets.Dropdown(
			options=['bone_r', 'inferno', 'viridis','plasma', 'cividis','gray','OrRd','PuBuGn','coolwarm','bwr'],
			value='bone_r',
			description='Colormap:',
		)

		

		colorscale_panel = ipywidgets.widgets.VBox(
			[colorMinSlider,colorMaxSlider,colorMapSelector],
			layout=box_layout)

		#controlPanel = ipywidgets.widgets.HBox([colorscale_panel])


		out = ipywidgets.widgets.interactive_output(buildDisplay,{
			'spectrum':ipywidgets.fixed(spectrum),
			'cmin':colorMinSlider,
			'cmax':colorMaxSlider,
			'cmap':colorMapSelector,
			})

		metaPanel = ipywidgets.widgets.VBox(
			[out,colorscale_panel],
			layout=ipywidgets.Layout(width='800px')
			)

		#output = metaPanel.children[-1]
		#output.layout.height = '200px'

		return metaPanel

	

	if Shape(spectrum['data'])==3:
		try:
			return generic(spectrum)
		except: 
			return generic(spectrum)


	elif Shape(spectrum['data'])==4:
		return Manipulator_2D_explorer(spectrum)
	#
	elif Shape(spectrum['data'])==2:
		return generic2D(spectrum)	

	else:
		print("explorer currently only supports datasets with dimension 2,3 or 4")

def indexOfClosestValue(axis,value):
	axis=list(axis)
	return axis.index(min(axis, key=lambda x:abs(x-value)))




def kwarp(spectrum,Eb_offset=ANALYZER_WORKFUNCTION, polar_offset=0,tilt_offset=0,hv=0,resolutionDivider=1,corrected_hvAxis=[],beQuiet=False):

	eV_per_J = 1.602176e-19
	hbar__Js = 1.054571e-34
	electron_mass__kg = 9.109e-31
	angstroms_per_meter=1e-10
	prefactor = (math.sqrt(2*electron_mass__kg*eV_per_J)/(hbar__Js))*angstroms_per_meter # = 0.51234

	#-------------------------------------------------------------------------------------------------------------------------------------------------
	def wholeMatrix_hvscan_warp(spectrum,tilt_offset,Eb_offset,corrected_hvAxis,resolutionDivider,beQuiet):
		import time
		import random

		t0=time.time()

		tilt_offset_rad = math.radians(tilt_offset)

		#-------------------------- Properties of source matrix
		sourceMatrix= spectrum['data']

		source_energyAxis = spectrum['Axis'][0]
		source_energyAxis_corrected = source_energyAxis - Eb_offset
		source_energyAxis_step = abs(source_energyAxis[1]-source_energyAxis[0])

		source_angleAxis = spectrum['Axis'][1]
		source_angleAxis_step = abs(source_angleAxis[1]-source_angleAxis[0])

		source_hvAxis = spectrum['Axis'][2]

		if source_hvAxis[0]>source_hvAxis[-1]: # Handle the case where photon energy was swept down rather than up:
			source_hvAxis = [ii for ii in reversed(spectrum['Axis'][2])]
			sourceMatrix = np.flip(sourceMatrix,2)		
		#--------------------------


		#-------------------------- Properties of output (destination) matrix	
		# Find the dimensions of an output matrix that will fit the entire kwarped dataset without compromising resolution 


		# First we find the max and min k values, by just calculating for each hv frame what the k limits and minimum k stepsize is on each frame
		# We'll then take the min and max from that list to determine the boundaries and number of points in the output matrix.
		
		kLimits=[]
		kSteps = []

		for index,hv in enumerate(source_hvAxis):

			if len(corrected_hvAxis)==0: #Normal case
				Ek_max = hv-ANALYZER_WORKFUNCTION-min(source_energyAxis_corrected)
				Ek_min = hv-ANALYZER_WORKFUNCTION-max(source_energyAxis_corrected)

			else: #Special case if there is a corrected hv axis - the kinetic energy range for each frame will be different
				local_source_energyAxis_corrected = source_energyAxis_corrected - (hv-corrected_hvAxis[index])
				Ek_max = corrected_hvAxis[index]-ANALYZER_WORKFUNCTION-min(local_source_energyAxis_corrected)
				Ek_min = corrected_hvAxis[index]-ANALYZER_WORKFUNCTION-max(local_source_energyAxis_corrected)

			# For this photon energy we can now calculate the max and min k values:
			kLimits.append(angle_to_ky_manipulator(alpha=source_angleAxis[0],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_max))
			kLimits.append(angle_to_ky_manipulator(alpha=source_angleAxis[-1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_max))

			# And the max and min k stepsizes:
			kSteps.append(abs(angle_to_ky_manipulator(alpha=source_angleAxis[0],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)-angle_to_ky_manipulator(alpha=source_angleAxis[1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)))
			kSteps.append(abs(angle_to_ky_manipulator(alpha=source_angleAxis[-1],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)-angle_to_ky_manipulator(alpha=source_angleAxis[-2],polar_offset=0,tilt_offset=tilt_offset,Ek=Ek_min)))

		kMax,kMin = max(kLimits),min(kLimits)
		kStepMax,kStepMin = max(kSteps),min(kSteps)

		# Downscale according to the divider that got passed in
		if resolutionDivider!=1 and beQuiet==False: print("Scaling k resolution by {}x, kStep now {:.4f} compared to minimum possible {:.4f}".format(resolutionDivider,kStepMax*resolutionDivider,kStepMin))
		
		num_kSteps = int((kMax-kMin)/(kStepMax*resolutionDivider))
		outputMatrix_kAxis = np.linspace(kMin,kMax,num_kSteps)


		# Now do the same exercise for the energy scale

		if len(corrected_hvAxis)==0:
			eMin = min(source_energyAxis_corrected)
			eMax = max(source_energyAxis_corrected)
		else:
			hv_delta = (max(abs(source_hvAxis-corrected_hvAxis)))
			eMin = min(source_energyAxis_corrected)
			eMax = max(source_energyAxis_corrected)
			if beQuiet==False:
				print("Largest hv correction to consider is {}. The binding energy scale of the output will thus be modified from {}--{} to {}--{}".format(hv_delta,eMin,eMax,eMin-hv_delta,eMax+hv_delta))
			eMin-=hv_delta
			eMax+=hv_delta

		num_eSteps = int((eMax-eMin)/(source_energyAxis_step*resolutionDivider))
		outputMatrix_eAxis = np.linspace(eMax,eMin,num_eSteps)
	
		# Initialize the output (kwarped) matrix
		outputMatrixSize = (outputMatrix_eAxis.size,outputMatrix_kAxis.size,source_hvAxis.size)
		outputMatrix=np.zeros(outputMatrixSize)
		#--------------------------


		#-------------------------- Perform the reverse mapping (look up source pixel from output pixel)

		
		# When we do 'all at once' calculations with np, there are going be to unphysical regions where we end up taking a sqrt of a negative number.
		# Rather than mask out all the offending regions, we're just going to let np try, sometimes produce invalid output, and deal with
		# this by the 'try/except' clauses. Because we already know that this is going to be going on, temporarily disable output warnings about it.

		for hv_index,photonEnergy in enumerate(source_hvAxis): #For each photon energy
	
			printProgressBar(hv_index, len(source_hvAxis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)

			im = sourceMatrix[:,:,hv_index] #Extract the energy-angle image, it will be [energy,angle]

			if len(corrected_hvAxis)==0: 
				source_Ek_axis = photonEnergy-ANALYZER_WORKFUNCTION-source_energyAxis_corrected
			else:
				source_Ek_axis= -source_energyAxis_corrected-ANALYZER_WORKFUNCTION + corrected_hvAxis[hv_index]

			output_Ek_axis = photonEnergy-ANALYZER_WORKFUNCTION-outputMatrix_eAxis

			# prepare for the the interpolation

			spl = scipy.interpolate.RectBivariateSpline(source_Ek_axis,source_angleAxis, im,kx=1,ky=1)



			# Pre-compute some things outside of the loop for speed
			C_axis = prefactor*np.sqrt(source_Ek_axis) 
			C2_axis = C_axis**2
			k2_axis = outputMatrix_kAxis**2

			source_angleAxis_min=min(source_angleAxis)
			source_angleAxis_max=max(source_angleAxis)

			for output_energyPixel,output_Ek in enumerate(output_Ek_axis): 

				if output_Ek>min(source_Ek_axis) and output_Ek<max(source_Ek_axis):
					sourceEnergy__Pixel=indexOfClosestValue(list(source_Ek_axis),output_Ek)

					C = C_axis[sourceEnergy__Pixel]
					C2 = C2_axis[sourceEnergy__Pixel]
					E = np.sqrt((C2-k2_axis))
					
					# Based on kparr = 0.512*sqrt(Ek)*sin(alpha+tilt), except we've precomputed 0.512*sqrt(Ek)
					source_angle_degrees = np.degrees(np.arcsin(outputMatrix_kAxis/C)-np.radians(tilt_offset)) #Contains all angle pixels at this energy value and this hv
					
					source_angle_degrees = [float('NaN') if (ii>source_angleAxis_max or ii<source_angleAxis_min) else ii for ii in source_angle_degrees]
					outputMatrix[output_energyPixel,:,hv_index]=np.nan_to_num(spl(output_Ek,source_angle_degrees,grid=False))



		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['data']=outputMatrix
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		if len(corrected_hvAxis)==0:
			outputSpectrum['Axis'][2]=list(source_hvAxis)
		else:
			outputSpectrum['Axis'][2]=list(corrected_hvAxis)
		outputSpectrum['AxisLabel'][2]="Photon energy" 
		outputSpectrum['AxisUnits'][2]='eV'

		outputSpectrum['Axis'][0]=list(outputMatrix_eAxis)
		outputSpectrum['AxisLabel'][0]="Binding energy"  
		outputSpectrum['AxisUnits'][0]='eV'

		outputSpectrum['Axis'][1]=list(outputMatrix_kAxis)
		outputSpectrum['AxisLabel'][1]="kY"
		outputSpectrum['AxisUnits'][1]='$\AA^{-1}$'



		if beQuiet==False: print("Time taken: {:.2f} seconds".format(time.time()-t0))
		return outputSpectrum
			
	#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def wholeMatrix_kwarp(spectrum,polar_offset,tilt_offset,hv,resolutionDivider):
		import time
		#print("wholeMatrix_kwarp")

		resolutionDivider=resolutionDivider

		t0=time.time()

		# ----- Input properties:

		x = spectrum['Axis'][2] # Typically angle 2 (deflector, polar)
		y = spectrum['Axis'][1] # Typically angle 1 (analyzer)
		e = spectrum['Axis'][0] # Typically energy
		e = np.array(list(reversed(e)))
		data = spectrum['data']

		# If the deflection or polar goes backwards, flip both the data matrix and the axis values
		# I don't think this is possible with deflector scans, but it is with polar maps

		#if x[0]>x[-1]:
		#	x = [ii for ii in reversed(spectrum['Axis'][2])]
		#	data = np.flip(data,2)

		#print("lenx,leny=",len(x),len(y))
		#print("shape data",np.shape(spectrum['data']))

		Ek_max = max(e)


		# ----- Output properties:

		outputMatrixSize = tuple(int(ii/resolutionDivider) for ii in data.shape)
		outputMatrix=np.zeros(outputMatrixSize)

	
		#print("Output matrix has shape:",outputMatrix.shape)

		#x_first, x_last = x[0]-polar_offset,x[-1]-polar_offset
		x = [ii - polar_offset for ii in x]
		#print("x_first,x_last = {:.3f},{:.3f}".format(x_first,x_last))
		x_k_first=angle_to_kx_manipulator(alpha=0,polar_offset = x[0], Ek = Ek_max)
		x_k_last=angle_to_kx_manipulator(alpha=0,polar_offset = x[-1], Ek = Ek_max)
		#print("k_first,k_last= {:.3f},{:.3f}".format(x_k_first,x_k_last))

		y_k_max=angle_to_ky_manipulator(alpha=np.max(y),polar_offset = min(np.abs(x)),tilt_offset= tilt_offset,Ek = Ek_max)
		y_k_min=angle_to_ky_manipulator(alpha=np.min(y),polar_offset = max(np.abs(x)),tilt_offset= tilt_offset,Ek = Ek_max)

		x_k_step=((x_k_last-x_k_first)/(outputMatrix.shape[2]-1))
		y_k_step=((y_k_max-y_k_min)/(outputMatrix.shape[1]-1))
		e_step = ((e[-1]-e[0])/(outputMatrix.shape[0]-1))

		x_kAxis = [x_k_first+(index*x_k_step) for index in range(outputMatrix.shape[2])]
		x_kAxis=np.array(x_kAxis)
		#print("x_kAxis spans {:.3f} through {:.3f}, step {:.3f}".format(x_kAxis[0],x_kAxis[-1],x_k_step))
		y_kAxis = [y_k_min+(index*y_k_step) for index in range(outputMatrix.shape[1])]
		y_kAxis=np.array(y_kAxis)
		#print("y_kAxis spans {:.3f} through {:.3f}, step {:.3f}".format(y_kAxis[0],y_kAxis[-1],y_k_step))
		#print(len(x_kAxis),len(y_kAxis))
		Ek_axis = [e[0]+(index*e_step) for index in range(outputMatrix.shape[0])]
		#print("Ek_axis spans {:.3f} through {:.3f}, step {:.3f}".format(Ek_axis[0],Ek_axis[-1],e_step))

		x_step = x[1]-x[0]
		y_step = y[1]-y[0]

		#x_angle = k_to_polar_manipulator(kx,ky,polar_offset,tilt_offset,Ek)
		#y_angle = k_to_alpha_manipulator(kx,ky,tilt_offset,Ek)

		tilt_rad = math.radians(tilt_offset)

		for index,Ek in enumerate(Ek_axis):

			if beQuiet==False: printProgressBar(index, len(Ek_axis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
				
			#print("Extracting a constant energy slice:")
			inputImage = data[int(index*resolutionDivider),:,:]

			#inputImage = data[:,:,int(index*resolutionDivider)]
			#inputImage is a constant energy slice
			#print("size is:",np.shape(inputImage.T))

			spl = scipy.interpolate.RectBivariateSpline(y,x, inputImage,kx=1,ky=1)
				
			#print(Ek)
			try: 
				C = 0.512316*math.sqrt(Ek) # Experiment with making this a parallel np operation outside of the loop (i.e defining a new array)

				for jj,kx in enumerate(x_kAxis):
					E = np.sqrt(((C**2)-(kx**2)-(y_kAxis**2)))
					#print(Ek,kx,y_kAxis[0],E[0])
					alpha_rad = (np.arcsin((np.sin(tilt_rad)*E - np.cos(tilt_rad)*y_kAxis)/C )) 
					y_angle = np.degrees(alpha_rad)
					#print(tilt_rad,y_kAxis[0])
					#print(kx,y_angle[0])
					#break
					polar_rad = (np.arctan((kx) / (np.sin(tilt_rad)*y_kAxis + np.cos(tilt_rad)*E )))
					x_angle = np.degrees(polar_rad)

					#outputMatrix[:,index,jj]=spl(x_angle,y_angle,grid=False)
					outputMatrix[index,:,jj]=spl(y_angle,x_angle,grid=False)


			except ValueError: 
				print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")
				outputMatrix[:,index,:]=0
		


		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputMatrix2 = []
		for i in range(len(outputMatrix)):
			col2 = []
			for j in range(len(outputMatrix[0])):
				col1 = []
				for k in range(len(outputMatrix[0][0])):
					col1.append(outputMatrix[len(outputMatrix)-i-1][j][k])
				col2.append(np.array(col1))
			outputMatrix2.append(np.array(col2))
		outputSpectrum['data']=np.array(outputMatrix2)
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		outputSpectrum['Axis'][2]=x_kAxis
		outputSpectrum['AxisUnits'][2]='$\AA^{-1}$'
		outputSpectrum['AxisLabel'][2]="k_X" 

		if hv!=0:
			outputSpectrum['Axis'][0]=[hv -ii - ANALYZER_WORKFUNCTION for ii in Ek_axis]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"  
		else:
			outputSpectrum['Axis'][0]=Ek_axis
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"			

		outputSpectrum['Axis'][1]=y_kAxis
		outputSpectrum['AxisUnits'][1]='$\AA^{-1}$'
		outputSpectrum['AxisLabel'][1]="k_Y"  

		if beQuiet == False: print("time taken:",time.time()-t0)
		return outputSpectrum

	def wholeMatrix_kwarp_deflector(spectrum,polar_offset,tilt_offset,hv,resolutionDivider):
		import time
		#print("wholeMatrix_kwarp_deflector")

		resolutionDivider=resolutionDivider

		t0=time.time()

		# ----- Input properties:

		x = spectrum['Axis'][2] # Typically angle 2 (deflector, polar). Will be mapped to kx
		y = spectrum['Axis'][1] # Typically angle 1 (analyzer). Will be mapped to ky
		e = spectrum['Axis'][0] # Typically energy
		e = list(reversed(e))
		#print("anticipating x=angle2,y=angle1,e=energy")
		#print("x,y,e lengths=",len(x),len(y),len(e))
		#print("x,y,e first/last elems:",x[0],x[-1],y[0],y[-1],e[0],e[-1])

		data = spectrum['data']
		#print("Input matrix has shape:",spectrum['data'].shape)	
		#print("Expected format is (energy,angle1,angle2)")
		# If the deflection or polar goes backwards, flip both the data matrix and the axis values
		# I don't think this is possible with deflector scans, but it is with polar maps

		#if x[0]>x[-1]:
		#	x = [ii for ii in reversed(spectrum['Axis'][2])]
		#	data = np.flip(data,2)

		Ek_max = max(e)


		# ----- Output properties:

		outputMatrixSize = tuple(int(ii/resolutionDivider) for ii in data.shape)
		outputMatrix=np.zeros(outputMatrixSize)

	
		#print("Output matrix has shape:",outputMatrix.shape)

		x_k_first=angle_to_kx_DA30(alpha=0,beta= x[0],polar_offset = polar_offset,Ek = Ek_max)
		x_k_last=angle_to_kx_DA30(alpha=0,beta= x[-1],polar_offset = polar_offset,Ek = Ek_max)

		y_k_max=angle_to_ky_DA30(alpha=np.max(y),beta=0,polar_offset = polar_offset,tilt_offset= tilt_offset,Ek = Ek_max)
		y_k_min=angle_to_ky_DA30(alpha=np.min(y),beta=0,polar_offset = polar_offset,tilt_offset= tilt_offset,Ek = Ek_max)

		x_k_step=((x_k_last-x_k_first)/(outputMatrix.shape[2]-1))
		y_k_step=((y_k_max-y_k_min)/(outputMatrix.shape[1]-1))

		e_step = ((e[-1]-e[0])/(outputMatrix.shape[0]-1))

		x_kAxis = [x_k_first+(index*x_k_step) for index in range(outputMatrix.shape[2])]
		x_kAxis=np.array(x_kAxis)
		#print("x_kAxis spans {:.3f} through {:.3f}, step {:.3f}. len{}".format(x_kAxis[0],x_kAxis[-1],x_k_step,len(x_kAxis)))
		y_kAxis = [y_k_min+(index*y_k_step) for index in range(outputMatrix.shape[1])]
		y_kAxis=np.array(y_kAxis)
		#print("y_kAxis spans {:.3f} through {:.3f}, step {:.3f}".format(y_kAxis[0],y_kAxis[-1],y_k_step))
		#print(len(x_kAxis),len(y_kAxis))
		Ek_axis = [e[0]+(index*e_step) for index in range(outputMatrix.shape[0])]
		#print("Ek_axis spans {:.3f} through {:.3f}, step {:.3f}".format(Ek_axis[0],Ek_axis[-1],e_step))

		x_step = x[1]-x[0]
		y_step = y[1]-y[0]

		polar_rad = math.radians(polar_offset)
		tilt_rad = math.radians(tilt_offset)
		st=math.sin(tilt_rad)
		ct=math.cos(tilt_rad)
		sp=math.sin(polar_rad)
		cp=math.cos(polar_rad)

		t12 = ct
		t13 = -st
		t21 = -cp
		t22 = sp*st
		t23 = sp*ct
		t31 = sp
		t32 = cp*st
		t33 = cp*ct	

		# Step through every constant energy slice and perform the warping 'all at once' on each slice
		for index,Ek in enumerate(Ek_axis):

			if beQuiet==False: printProgressBar(index, len(Ek_axis)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
			
			#print("Extracting a constant energy slice:")
			inputImage = data[int(index*resolutionDivider),:,:]
			#inputImage = data[:,:,int(index*resolutionDivider)]
			#inputImage is a constant energy slice
			#print("size is:",np.shape(inputImage))
			#print(len(x),len(y))

			# Fast method of doing 2D interpolation from the source energy slice

			spl = scipy.interpolate.RectBivariateSpline(y,x, inputImage,kx=1,ky=1)
			
			#print("Ek = ",Ek)
			C = 0.512316*math.sqrt(Ek)

			for jj,kx in enumerate(x_kAxis):
				E = np.sqrt((C**2-kx**2-y_kAxis**2))
				zz = np.sqrt(C**2 - (t31*kx + t32*y_kAxis + t33*E)**2)
				precalc1 = -np.arccos((t31*kx + t32*y_kAxis + t33*E)/C)/zz
				beta_rad = precalc1  * (t21*kx + t22*y_kAxis + t23*E)
				x_angle= np.degrees(beta_rad)
				alpha_rad = precalc1 * (t12*y_kAxis + t13*E)
				y_angle= -np.degrees(alpha_rad) # Notice that I flipped the sign!	

				temp = spl(y_angle,x_angle,grid=False)
				#print(len(temp))
				outputMatrix[index,:,jj]=temp
			



		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputMatrix2 = []
		for i in range(len(outputMatrix)):
			col2 = []
			for j in range(len(outputMatrix[0])):
				col1 = []
				for k in range(len(outputMatrix[0][0])):
					col1.append(outputMatrix[len(outputMatrix)-i-1][len(outputMatrix[0])-j-1][len(outputMatrix[0][0])-k-1])
				col2.append(np.array(col1))
			outputMatrix2.append(np.array(col2))
		outputSpectrum['data']=outputMatrix2
		outputSpectrum['Axis']=[[],[],[]]
		outputSpectrum['AxisLabel']=["","",""]
		outputSpectrum['AxisUnits']=["","",""]

		outputSpectrum['Axis'][2]=x_kAxis
		outputSpectrum['AxisUnits'][2]='$\AA^{-1}$'
		outputSpectrum['AxisLabel'][2]="k_X" 

		if hv!=0:
			outputSpectrum['Axis'][0]=[hv - ii - ANALYZER_WORKFUNCTION for ii in Ek_axis]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"
		else:
			outputSpectrum['Axis'][0]=Ek_axis
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"			

		outputSpectrum['Axis'][1]=y_kAxis
		outputSpectrum['AxisUnits'][1]='$\AA^{-1}$'
		outputSpectrum['AxisLabel'][1]="k_Y"  

		if beQuiet == False: print("time taken:",time.time()-t0)
		return outputSpectrum

	def energy_angle_kwarp(spectrum,polar_offset=0,tilt_offset=0,resolutionDivider=1,beQuiet=False):
		#print("energy_angle_kwarp")

		def linearInterpolation(row,column,image):

			c0 = math.floor(column)
			c1 = math.ceil(column)   
			c0_weight=c1-column
			c1_weight=column-c0
			
			interpolatedPixel=0
			if c0<image.shape[1]:	interpolatedPixel+=image[row][c0]*c0_weight
			if c1<image.shape[1]:	interpolatedPixel+=image[row][c1]*c1_weight

			return interpolatedPixel

		e=spectrum['Axis'][0]
		a=spectrum['Axis'][1]
		im=spectrum['data']#.T
		#e = list(reversed(e))

		source_numPixels = len(a)
		e_midpoint = e[0]+((e[-1]-e[0])/2)
		a_step = a[1]-a[0]
		# -------------------------------------
		# Initialize the destination image
			
		dest_numPixels = math.ceil(source_numPixels/resolutionDivider)
		destImage = np.zeros([len(e),dest_numPixels])
		
		# ------------------------------------------------
		# Calculate the k axis scale of the dest image
		if polar_offset==0: kx=0
		else: kx = angle_to_kx_manipulator(alpha=0,polar_offset=polar_offset,Ek=e_midpoint)

		ky_1 = angle_to_ky_manipulator(alpha=a[0],polar_offset=polar_offset,tilt_offset=tilt_offset,Ek=e_midpoint)
		ky_2 = angle_to_ky_manipulator(alpha=a[-1],polar_offset=polar_offset,tilt_offset=tilt_offset,Ek=e_midpoint)
		
		destImage_kAxis = np.linspace(ky_1,ky_2,dest_numPixels)
		dk = destImage_kAxis[1]-destImage_kAxis[0]  

		# ------------------------------------------------
		# Extract the destination image out of the source image
		
		minXAngle = 90
		maxXAngle = -90

		# This is split into two cases for speed reasons - the simple case is nearly 50% faster
		if polar_offset==0:

			precalc1 = 360/(2*math.pi)

			for energy_pixel,Ek in enumerate(e):

				precalc2 = (0.512316*math.sqrt(Ek))

				for jj,k in enumerate(destImage_kAxis):
					
					angle = precalc1*(math.asin(k/precalc2))
					#angle = k_to_alpha_manipulator(kx=0,ky=k,tilt_offset=tilt_offset,Ek=Ek)
					sourceAnglePixel = (angle - tilt_offset - a[0])/a_step
					destImage[energy_pixel,jj] = float(linearInterpolation(row=energy_pixel,column=sourceAnglePixel,image=im))

		else:	   
			for energy_pixel,Ek in enumerate(e):

				for jj,k in enumerate(destImage_kAxis):
					if beQuiet==False:
						# This calculation is not used for interpolation, just to keep track of how bad this approximation is
						x_angle = k_to_polar_manipulator(kx=kx,ky=k,polar_offset=0,tilt_offset=tilt_offset,Ek=Ek)
						if x_angle<minXAngle: minXAngle = x_angle
						if x_angle>maxXAngle: maxXAngle = x_angle
						
					y_angle = k_to_alpha_manipulator(kx=kx,ky=k,tilt_offset=tilt_offset,Ek=Ek)
					
					# Find the pixel coordinate corresponding to this angle
					sourceAnglePixel = (y_angle-a[0])/a_step
					
					destImage[energy_pixel,jj] = linearInterpolation(row=energy_pixel,column=sourceAnglePixel,image=im)
			
			if beQuiet==False:
				if(abs(minXAngle-maxXAngle)>0.02):
					print("\nYou acquired this image at a polar angle of {:.3f}".format(polar_offset))
					print("This kwarp is an approximation. An error-free kwarp would require a polar map spanning {:.2f}deg to {:.2f}deg".format(minXAngle,maxXAngle))





		outputSpectrum={}
		outputSpectrum['Metadata']={}
		outputSpectrum['Axis']=[[],[]]
		outputSpectrum['AxisLabel']=["",""]
		outputSpectrum['AxisUnits']=["",""]

		outputSpectrum['Metadata']=spectrum['Metadata'].copy()
		destImage2 = []
		for i in range(len(destImage)):
			col = []
			for j in range(len(destImage[0])):
				col.append(destImage[len(destImage)-i-1][j])
			destImage2.append(np.array(col))
		destImage2 = np.array(destImage2)
		outputSpectrum['data']=destImage
		outputSpectrum['Axis'][1]=destImage_kAxis
		outputSpectrum['AxisLabel'][1]="k$_{\parallel}$"
		outputSpectrum['AxisUnits'][1]="$\AA^{-1}$"
		if hv!=0:
			outputSpectrum['Axis'][0]=[hv - ii - ANALYZER_WORKFUNCTION for ii in e]
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Binding energy"
		else:
			outputSpectrum['Axis'][0]=e
			outputSpectrum['AxisUnits'][0]="eV"
			outputSpectrum['AxisLabel'][0]="Kinetic energy"

		return outputSpectrum

	if Shape(spectrum['data'])==2 and spectrum['AxisUnits'][1]=="$\\degree$":
		return energy_angle_kwarp(spectrum,polar_offset,tilt_offset,resolutionDivider,beQuiet)

	#elif Shape(spectrum['data'])==3 and spectrum['AxisUnits'][2]=="eV":
	#	return wholeMatrix_hvscan_warp(spectrum,tilt_offset=tilt_offset,Eb_offset=Eb_offset,resolutionDivider=resolutionDivider,corrected_hvAxis=corrected_hvAxis,beQuiet=beQuiet)
	
	elif Shape(spectrum['data'])==3 and spectrum['AxisLabel'][2]=="Deflector angle":
		return wholeMatrix_kwarp_deflector(spectrum,polar_offset,tilt_offset,hv=hv,resolutionDivider=resolutionDivider)
	
	elif Shape(spectrum['data'])==3 and spectrum['AxisUnits'][2]=="$\\degree$":
		return wholeMatrix_kwarp(spectrum,polar_offset,tilt_offset,hv=hv,resolutionDivider=resolutionDivider)
		
	else:
		print("I don't know how to k-warp this type of spectrum")
def angle_to_kx_DA30(alpha,beta,polar_offset,Ek):

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")


	alpha_rad = -math.radians(alpha) # Notice that I flipped the sign!
	beta_rad = math.radians(beta)
	polar_rad = math.radians(polar_offset) 

	D = math.sqrt(alpha_rad**2 + beta_rad**2)
		
	# Be careful, we can't use np.sinc since it is the engineering form sin(pi*x)/(pi*x)
	if D==0: 	sincD = 1 
	else: 		sincD = math.sin(D)/D

	kx = C * (beta_rad*math.cos(polar_rad)*sincD + math.sin(polar_rad)*math.cos(D))

	return kx

def angle_to_kx_manipulator(alpha,polar_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = -math.radians(alpha) # Notice that I flipped the sign!
	polar_rad = math.radians(polar_offset) 
  
	kx = C*math.sin(polar_rad)*math.cos(alpha_rad)

	return kx

def angle_to_ky_DA30(alpha,beta,polar_offset,tilt_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = -math.radians(alpha) # Notice that I flipped the sign!
	beta_rad = math.radians(beta)
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	D = math.sqrt(alpha_rad**2 + beta_rad**2)

	if D==0: 	sincD = 1
	else: 		sincD = math.sin(D)/D
			
	ky = C * (sincD*(-alpha_rad*math.cos(tilt_rad)-beta_rad*math.sin(tilt_rad)*math.sin(polar_rad)) + math.cos(D)*math.sin(tilt_rad)*math.cos(polar_rad))

	return ky

def angle_to_ky_manipulator(alpha,polar_offset,tilt_offset,Ek):
	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	alpha_rad = -math.radians(alpha) # Notice that I flipped the sign!
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	ky = C * (math.cos(alpha_rad)*math.sin(tilt_rad)*math.cos(polar_rad) - math.cos(tilt_rad)*math.sin(alpha_rad))

	return ky

def k_to_alpha_DA30(kx,ky,polar_offset,tilt_offset,Ek):
	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.NaN

	E = math.sqrt(((C**2)-(kx**2)-(ky**2)))

	st=math.sin(tilt_rad)
	ct=math.cos(tilt_rad)
	sp=math.sin(polar_rad)
	cp=math.cos(polar_rad)

	t12 = ct
	t13 = -st
	t31 = sp
	t32 = cp*st
	t33 = cp*ct

	zz = math.sqrt(C**2 - (t31*kx + t32*ky + t33*E)**2)

	if  zz == 0:	alpha_rad=0
	else:			alpha_rad = -math.acos( (t31*kx + t32*ky + t33*E)/C) * (t12*ky + t13*E) / zz

	# I deliberately flip the sign of all ky terms
		
	return -math.degrees(alpha_rad) # Notice that I flipped the sign!

def k_to_alpha_manipulator(kx,ky,tilt_offset,Ek):

	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.NaN

	E = math.sqrt(((C**2)-(kx**2)-(ky**2)))

	
	alpha_rad = (math.asin((math.sin(tilt_rad)*E - math.cos(tilt_rad)*ky)/C )) 

	return -math.degrees(alpha_rad) # Notice that I flipped the sign!

def k_to_beta_DA30(kx,ky,polar_offset,tilt_offset,Ek):

	polar_rad = math.radians(polar_offset)
	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.NaN

	E = math.sqrt((C**2-kx**2-ky**2))

	st=math.sin(tilt_rad)
	ct=math.cos(tilt_rad)
	sp=math.sin(polar_rad)
	cp=math.cos(polar_rad)
		
	t21 = -cp
	t22 = sp*st
	t23 = sp*ct
	t31 = sp
	t32 = cp*st
	t33 = cp*ct

	zz = math.sqrt(C**2 - (t31*kx + t32*ky + t33*E)**2)

	if zz==0:	beta_rad= 0
	else:		beta_rad = -math.acos((t31*kx + t32*ky + t33*E)/C)  * (t21*kx + t22*ky + t23*E) /zz
		

	return math.degrees(beta_rad)


def k_to_polar_manipulator(kx,ky,polar_offset,tilt_offset,Ek):

	tilt_rad = math.radians(tilt_offset)

	try: C = 0.512316*math.sqrt(Ek)
	except ValueError: print("! WARNING! An unphysical negative Ek was encountered in the input spectrum")

	if (C**2-kx**2-ky**2)<0:
		#print("Impossibly large kx/ky components for this kinetic energy ({:.2f},{:.2f})".format(kx,ky))
		return np.NaN
		

	E = math.sqrt((C**2-kx**2-ky**2))

	polar =  (math.atan((kx) / (math.sin(tilt_rad)*ky + math.cos(tilt_rad)*E )))

	return math.degrees(polar)+polar_offset

def Parameters(rr,Lens,ph,busca_n_linha,prin):
    rr = round(rr,3)
    index_lens = busca_n_linha(Lens,ph)[0]+2
    ph_len = []
    for i in range(index_lens,len(ph)):
        if len(ph[i]) >0:
            if ph[i][0] != '#':
                ph_len.append(ph[i])
            else:
                    break
    parameter = []; parameter_values = []
    for i in range(len(ph_len)):
        if len(ph_len[i]) == 1:
            marker = 0; marker2 = False
            if marker2 == False:
                for car in ph_len[i][0]:
                    if car == '@':
                        marker+=1
                        marker2 = True
                        break
                    else:
                        marker+=1 
            ratio = float(ph_len[i][0][marker:-1])
            aInner = int(ph_len[i+1][2])
            d1 = ph_len[i+2]
            Da1 = np.array([d1[2],d1[3],d1[4]],dtype = float)
            d3 = ph_len[i+3]
            Da3 = np.array([d3[2],d3[3],d3[4]],dtype = float)
            d5 = ph_len[i+4]
            Da5 = np.array([d5[2],d5[3],d5[4]],dtype = float)
            d7 = ph_len[i+5]
            Da7 = np.array([d7[2],d7[3],d7[4]],dtype = float)
            parameter.append([ratio,aInner])
            parameter_values.append([Da1,Da3,Da5,Da7])

    for r in range(len(parameter)):
        ratio = parameter[r][0]
        if rr == ratio:
            dr = 0; index = r
        else:
            if r == 0:
                dr = abs(rr - ratio)
                index = 0
            else:
                dr_new = abs(rr - ratio)
                if dr_new < dr:
                    dr = dr_new
                    index = r
    if dr == 0:
        if prin == True:
            print('Ratio = %s and aInner = %s deg\n' %(parameter[index][0],parameter[index][1]))
            print('Da1 = %s, %s, %s mm_z/deg^1 \n' %(parameter_values[index][0][0],parameter_values[index][0][1],parameter_values[index][0][2]))
            print('Da3 = %s, %s, %s mm_z/deg^3 \n' %(parameter_values[index][1][0],parameter_values[index][1][1],parameter_values[index][1][2]))
            print('Da5 = %s, %s, %s mm_z/deg^5 \n' %(parameter_values[index][2][0],parameter_values[index][2][1],parameter_values[index][2][2]))
            print('Da7 = %s, %s, %s mm_z/deg^7 \n' %(parameter_values[index][3][0],parameter_values[index][3][1],parameter_values[index][3][2]))
        return [parameter[index],parameter_values[index]]
    else:
        parameter[index].append(round(dr,3))
        if prin == True:
            print('Ratio = %s, aInner = %s deg and diferrence for the nearest ratio %s \n' %(rr,parameter[index][1], parameter[index][2]))
            print('Da1 = %s, %s, %s mm_z/deg^1 \n' %(parameter_values[index][0][0],parameter_values[index][0][1],parameter_values[index][0][2]))
            print('Da3 = %s, %s, %s mm_z/deg^3 \n' %(parameter_values[index][1][0],parameter_values[index][1][1],parameter_values[index][1][2]))
            print('Da5 = %s, %s, %s mm_z/deg^5 \n' %(parameter_values[index][2][0],parameter_values[index][2][1],parameter_values[index][2][2]))
            print('Da7 = %s, %s, %s mm_z/deg^7 \n' %(parameter_values[index][3][0],parameter_values[index][3][1],parameter_values[index][3][2]))
        return [parameter[index],parameter_values[index]]

def warping(e,a,D,Ekccd,Ep):
    x0 = Ekccd -0.05*Ep
    x1 = Ekccd
    x2 = Ekccd +0.05*Ep


    D_e = []
    for i in range(len(D)):
        y = D[i]
        a2 = ( (y[2]-y[0])*(x1 - x0) + (y[1]-y[0])*(x0 - x2) ) / ( (pow(x2,2) - pow(x0,2))*(x1 - x0) + (pow(x1,2) - pow(x0,2))*(x0 - x2) )
        a1 = ( (y[1]-y[0])  - a2*(pow(x1,2)-pow(x0,2)) ) / (  x1-x0  )
        a0 = y[0] - a1*x0 - a2*pow(x0,2)
        Den = a0 + a1*e + a2*pow(e,2)
        D_e.append(Den)

    z = D_e[0]*a + D_e[1]*pow(a,3) + D_e[2]*pow(a,5) +D_e[3]*pow(a,7) #mm
    
    return z
