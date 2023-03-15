from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

sessions = AudioUtilities.GetAllSessions()
            
def get_programs():
    program_lst = []
    for session in sessions:
        if session.Process:
            #print(session.Process.name())
            program_lst.append(session.Process.name())
    return program_lst
            
def get_volumes(apps):
    volume_lst = []
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if isinstance(apps, str):
            if session.Process and session.Process.name() == apps:
                print("volume of" ,apps,'is', volume.GetMasterVolume())
                
        else:
            for app in apps:
                if session.Process and session.Process.name() == app:
                    #print("volume of" ,app,'is', volume.GetMasterVolume())
                    volume_lst.append(volume.GetMasterVolume())
    return volume_lst
                    
def set_master_volume(apps,value):
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if isinstance(apps, str):
            if session.Process and session.Process.name() == apps:
                volume.SetMasterVolume(float(value), None)
        elif isinstance(apps, list):
            for app in apps:
                if session.Process and session.Process.name() == app:
                    volume.SetMasterVolume(value, None)
        else:
            print('apps not str or list')

def main():
    def pick_program(pos):
        user = input('pick a volume level 0.1-1.0')
        set_master_volume(programs[pos],user)
        
    programs = get_programs()
    vol = get_volumes(programs)
    counter = 0
    for program, vol in zip(programs, vol):
        print('the volume of', program,'is', vol,'enter', counter,'to select a program')
        counter += 1
        
    while True:
        try:
            user = int(input('select a program of enter Q to quit'))
        except:
            quit()
        
        if user >= len(programs):
            print('selection not in list try again or enter Q to quit')
            main()
        pick_program(user)
        
    
    
                  
if __name__ == "__main__":
    main()