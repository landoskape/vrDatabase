from sqlalchemy import Column, Integer, String, Boolean, Date, Float, Text, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class mice(Base):
    __tablename__ = 'mice'

    # an ID autogenerated by MySQL which uniquely identifies this session
    uid = Column(Integer, primary_key=True, autoincrement=True) 
    
    # the following three columns correspond to the standard Alyx format for managing mice and sessions
    mouseName = Column(String(9), nullable=False) # the mouse name (usually in NAMENUMBER, e.g. ATL001) format
    birthdate = Column(Date, nullable=False) # the date of the session 
    sex = Column(String(1), nullable=False) # the session ID
    virusDate = Column(Date, nullable=True)
    virusDescription = Column(Text, nullable=True)
    implantDate = Column(Date, nullable=True)
    implantDescription = Column(Text, nullable=True)
    logTime = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    

class sessions(Base):
    __tablename__ = 'sessions'

    # an ID autogenerated by MySQL which uniquely identifies this session
    uid = Column(Integer, primary_key=True, autoincrement=True) 
    
    # the following three columns correspond to the standard Alyx format for managing mice and sessions
    mouseName = Column(String(9), nullable=False) # the mouse name (usually in NAMENUMBER, e.g. ATL001) format
    date = Column(Date, nullable=False) # the date of the session 
    sessionID = Column(Integer, nullable=False) # the session ID
    
    # details about the experiments
    experimentType = Column("experimentType", String(100)) # textual description of experiment type
    experimentID = Column("experimentID", Integer, nullable=True) # an experiment ID -- which will correspond to experiment types in an "experiment" table
    behavior = Column(Boolean, nullable=False) # whether or not behavioral data was recorded
    imaging = Column(Boolean, nullable=False) # whether or not imaging was conducted
    faceCamera = Column(Boolean, nullable=False) # whether or not the faceCamera was used
    
    # details about behavior
    vrEnvironments = Column(Integer, nullable=True) # a bitand code for the vrEnvironments that were used (there will be a table for this)
    headPlateRotation = Column(Float, nullable=True) # the rotation in degrees of the head plate fork (should be measured manually, not by the read out of the holder!)
    
    # details about imaging properties (will ignore if "imaging" is set to False)
    numPlanes = Column(Integer, nullable=True) # the number of imaging planes
    planeSeparation = Column(Float, nullable=True) # the separation (in um) of imaging planes
    pockelsPercentage = Column(Float, nullable=True) # the percentage the pockels cell was set to
    objectiveRotation = Column(Float, nullable=True) # the rotation in degrees of the objective (should be measured manually, not by the read out of scanImage!)
    
    # processing details
    vrRegistration = Column(Boolean, nullable=False) # whether or not vrExperimentRegistration has been conducted
    s2p = Column(Boolean, nullable=True) # whether or not suite2p has been run
    s2pQC = Column(Boolean, nullable=True) # whether or not suite2p has been quality controlled
    redCellQC = Column(Boolean, nullable=True) # whether or not red cell quality control has been conducted
    sessionQC = Column(Boolean, nullable=False, default=True) # whether or not the session is good (starts as True, can set to False if necessary to avoid retrieving bad data)
    sessionScratchExplanation = Column(Text, nullable=True) # if session QC set to False, a textual explanation as to why it should be scratched
    
    # generic feature
    logTime = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


def returnBase():
    return Base


