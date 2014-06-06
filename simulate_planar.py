
import sys
import os
import time
import math
import copy

import load_errors
import planar_lattice
import perfect_matching


home = os.environ['HOME']


        
class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start


        



def squashMatching(size,error_type,matching):

   channel=0 if error_type=="X" else 1

   flip_array=[[1]*(2*size+1) for _ in range(2*size+1)]

   for [(pt,p0,p1),(qt,q0,q1)] in matching:


      flips = []
    
      if (p0 in [-1,size*2+1] and q0 in [-1,size*2+1]) or (p1 in [-1,size*2+1] and q1 in [-1,size*2+1]):
         flips+=[]

      else:

         s0=int(math.copysign(1,q0-p0))
         s1=int(math.copysign(1,q1-p1))
         
         range0=range(1,abs(q0-p0),2)
         range1=range(1,abs(q1-p1),2)         
         for x in range1:
            flips+=[[p0,p1+s1*x]]
         for y in range0:
            flips+=[[p0+s0*y,q1]]

         
      for flip in flips:
         flip_array[flip[0]][flip[1]]*=-1



   return flip_array

           

         
            

            
            
                    



###
###          RUN CODE 
###




testvec4=[0.926639, 0.006904, 0.003904, 0.003904, 0.000012, 0.000024,0.000012,
               0.000048, 0.000048, 0.001062, 0.042477, 0.006868, 0.003904,0.003904,
               0.000012, 0.000024, 0.000012, 0.000048, 0.000048, 0.000147]

testvec3=[0.96288, 0.003438, 0.00132, 0.00132, 0.000002, 0.000006,
               0.000002, 0.000018, 0.000018, 0.002292, 0.021877, 0.002552, 0.00132,
               0.00132, 0.000002, 0.000006, 0.000002, 0.000018, 0.000018, 0.002552]






def run2D(size=4,p=0.03,pLie=0,showArray=False):

   L=planar_lattice.PlanarLattice(size)

   L.applyRandomErrors(p,p)
   L.measureStars(pLie)
   L.measurePlaquettes(pLie)

   #L.showArray("errors","X")

   L.findAnyons()

   matchingX=perfect_matching.match_planar_2D(size,"plaquette",L.positions_anyons_P)
   matchingZ=perfect_matching.match_planar_2D(size,"star",L.positions_anyons_S)

   
   L.apply_matching("X",matchingX)
   L.apply_matching("Z",matchingZ)
   
   if showArray==True:
      L.showArrayText("errors","X")
      L.showArrayText("errors","Z")

   return L.measure_logical()






def run3Drandom(size=4,tSteps=5,p=0.05,pLie=0.00,timespace = [1,1],showTextArray=False):

   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)
   

   for i in range(tSteps):                     # loop over time      
                
      L.applyRandomErrors(p,p)
      L.measurePlaquettes(pLie)               
      L.measureStars(pLie)                    
      PL.addMeasurement(L)         # add the updated 2D lattice to 3D array


   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   if showTextArray==True: L.showArrayText("errors","X")
   
   PL.findAnyons()

   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace)


   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)
   
   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

   return L.measure_logical()
   








def run3D(size=4,tSteps=5,errorVec3 = testvec4, errorVec4=testvec4,timespace=[1,1],boundary_weight = 1,stabilizersNotComplete=0):


   t0 = time.time()
   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)

   for i in range(tSteps):                     # loop over time                                                       
        L.measureNoisyStabilizers("plaquette",errorVec3, errorVec4,stabilizersNotComplete)
        L.measureNoisyStabilizers("star",errorVec3,errorVec4,stabilizersNotComplete)                                
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)                        # this to the parity Lattice

   PL.findAnyons()

#   L.showArray("all",0)
   
   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)

   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)
 
   return L.measure_logical()










