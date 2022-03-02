"""
    profile_displacement.py
        -- profile the getdisplacement function
"""


from GPS_service import objdict
from time import time

# define input parameters
inputdict = {}
#non-required paras
inputdict['scale'] = None
inputdict['ref'] = None 
inputdict['ct'] = None 
inputdict['pt'] = None
inputdict['eon'] = False
inputdict['mon'] = False
inputdict['dwin1'] = None
inputdict['dwin2'] = None
inputdict['vabs'] = False
inputdict['analysisCenter'] = None

# required
# --lat 33 --lon -115 --width 2 --height 2 -t1 2010-04-07 -t2 2010-04-09 -c NGL -o displacement.kml
inputdict["lat"] = 33
inputdict["lon"] = -115
inputdict["width"] = 4
inputdict["height"] = 4
inputdict["epoch1"] = '2010-01-01'
inputdict["epoch2"] = '2011-01-01'
inputdict["output"] = "1_profile"

paras = objdict(inputdict)

def main():
    """call getdisplacement"""
    print(paras)
    start = time()
    from getDisplacement import getDisplacement
    getDisplacement(paras)
    end = time()
    print(f'It took {end - start} seconds!')

if __name__ == '__main__':

    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()