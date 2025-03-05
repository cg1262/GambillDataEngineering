###################################################
    ## CALCULATE TOTAL HOURS (MARKER/MEASURE 'M2') BY FILE TYPE (## M2 = Cumulative Engine Hours in agg sheet, Total Hours in Measures sheet, M2, SR )
###################################################
def calculateTotalHours(oneSecDF,icdFileType):    
  ttlHours = 0
  
  ############################  SR - NON IDAHO (USE A CALC) ##Hours over a single flight##
  if icdFileType.startswith('2033'):
      
    ttlHours = oneSecDF.filter((oneSecDF['`142.00`'] > 500) & (oneSecDF['`121.00`'] > 26) ).count()  ## count number of seconds criteria met.
   
  ############################ SR - IDAHO (USE 110.00) ##Cumulative Hours over the life of an aircraft## GARMIN HOBBS Time
  elif icdFileType.startswith('3552'):    
    #ttlHours = oneSecDF.agg({"`110.00`":"max"}).first()[0] ##get max of label 110.00 
    ttlHours = oneSecDF.filter((oneSecDF['`142.00`'] > 500) & (oneSecDF['`121.00`'] > 26) ).count()  ## count number of seconds criteria met.

  ##added by Nihilent for SF50##
  ############################ SF - REV D, E (USE 171.00) ##Cumulative Hours over the life of the engine##
  elif icdFileType.startswith('2034D') or icdFileType.startswith('2034E') :    
    ttlHours = oneSecDF.agg({"`171.00`":"max"}).first()[0] ##get max of label 171.00 

  ##added by Nihilent for SF50##
  ############################ SF - REV F (USE 110.00) ##Cumulative Hours over the life of the engine##
  elif icdFileType.startswith('2034F'): 
    ttlHours = oneSecDF.agg({"`110.00`":"max"}).first()[0] ##get max of label 110.00
  return ttlHours

###################################################
    ## CALCULATE FLIGHT HOURS (MARKER/MEASURE 'M10') BY FILE TYPE ( ## M10 = Flight Hours in agg sheet, Flight Time in Measures sheet, M10)
###################################################
def calculateFlightHours(oneSecDF,icdFileType, airGroundStatusLabel):
  flightHrs = 0
  
  ############################  SR - NON IDAHO (USE A CALC)
  #if icdFileType.startswith('2033'):
    ##added by Nihilent for SF50##     
  #  flightHrs = oneSecDF.filter((oneSecDF['`'+ airGroundStatusLabel + '`'] == 0)).count() #Hobbs Secs 
    
  ############################ SR - IDAHO (USE 110.01)
  if icdFileType.startswith('3552'):  
    flightHrs = oneSecDF.agg({"`110.01`":"max"}).first()[0] ##get max of label 110.01   GARMIN FLIGHT Time

  ############################ SF - REV D, E (USE A CALC) ----- for sf where we need to calc, count number of seconds aircraft is off ground based on air ground label
  #elif icdFileType.startswith('2034D') or icdFileType.startswith('2034E') : 
    ##added by Nihilent for SF50##           
  #  flightHrs = oneSecDF.filter((oneSecDF['`'+ airGroundStatusLabel + '`'] == 1)).count() #Hobbs Secs

  ############################ SF - REV F (USE 110.01)
  #elif icdFileType.startswith('2034F'):    
  elif icdFileType=='2034F':
    flightHrs = oneSecDF.agg({"`110.01`":"max"}).first()[0] ##get max of label 110.01  
    
  return flightHrs