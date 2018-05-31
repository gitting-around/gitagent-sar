namespace java com.swarms.thrift
namespace csharp SwarmsGUI.Comm.Thrift
namespace cpp swarms

struct Position{
	1: double longitude,  // [degrees/minutes/seconds]
	2: double latitude,	 // [degrees/minutes/seconds]
	3: double altitude,	// [m]
	4: double depth,	// [m]
    5: i64 lastUpdate,
}

struct Orientation {
	1: double roll,
	2: double pitch,
	3: double yaw,
    4: i64 lastUpdate,
}

struct Region {
	1: list<Position> area,
}

struct Capability {
	1: string name,
}

enum VehicleType{
	ROV,
	AUV,
    USV,
	VESSEL,
}

enum EquipmentType {
	CAMERA,
	SONAR,
	PROPULSION,
	H2S,
	LIGHT,
	GPS,
	ACOUSTIC,
    USBL,
    WIFI
    ARM,
    ENERGY,
    SALINITY,
}

struct Equipment {
	1: EquipmentType type,
	2: i32 consumption,					//mW/h
	3: string name,
}

enum TaskRegionType {
	Point,
	Column,
	Area,
}

struct Task {
	1: i32 taskTypeId,	// from excel file provided by Johann
	2: string description,
	3: TaskRegionType regionType
	4: list<EquipmentType> requiredTypes,
	5: double maxSpeed,  // [m/s]
}

enum TaskStatus {
	NotStarted,
	Running,
	Finished,
	Stopped,
}

struct Vehicle {
	1: i32 id,
	2: string name,
	3: Position location,
	4: Orientation orientation,
	5: double speed,     // [m/s] The speed at which the consumption is provided
	6: double currentSpeed,	// [m/s]					//Current speed of the robot while performing an action
	7: VehicleType type,
	8: i32 maxBattery			//Max battery power (mW/h)
	9: double batteryStatus,						//The remaining power (mW/h) of the battery
 	10: i32 consumption,	//	[mW/h]					//Battery consumption of the vehicle for the given speed
	11: list<Equipment> equipments,
	12: bool onboardPlanner,
	13: i64 lastUpdate,
    14: double safetyDistance,
}

struct Action {
	1: Task relatedTask,
	2: i32 actionId,
	3: Region area,
	4: double speed, // [m/s]
	5: double altitude, // [m]
	6: double range,  // What is range?
	7: i32 timeLapse, // [s]
	8: Orientation bearing,
	9: i32 startTime, // relative to the mission timeline
	10: i32 endTime, // relative to the mission timeline
	11: TaskStatus status,
	12: i32 assignedVehicleId,
	13: i32 parentActionId, // Id of parent Action for sub-actions
}


struct Mission {
	1: i32 missionId,
	2: Region navigationArea,
	3: list<Region> forbiddenArea,
	4: list<Position> surfacePoints,
	5: list<Action> actions,
	6: list<Vehicle> vehicles,
}

struct H2S {
    1: i32 h2sId,
	2: double latitude,
	3: double longitude,
    4: double depth,
	5: double h2s,
    6: i64 time,
}

struct Landmark {
    1: i32 landmarkId,
	2: string name,
	3: double latitude,
	4: double longitude,
    5: string url,
    6: i64 time,
}

struct Pressure {
    1: i32 pressureId,
    2: double latitude,
	3: double longitude,
    4: double pressure,
    5: i64 time,
}

struct Temperature {
    1: i32 temperatureId,
    2: double latitude,
	3: double longitude,
    4: double depth,
    5: double temperature,
    6: i64 time,
}

struct Ph {
    1: i32 phId,
    2: double latitude,
	3: double longitude,
    4: double depth,
    5: double ph,
    6: i64 time,
}


struct TimedSpeed {
    1: double speed,
	2: i64 time,
}

struct Current {
    1: i32 currentId,
    2: double latitude,
	3: double longitude,
    4: double depth,
    5: double currentEast,
    6: double currentNorth,
    7: i64 time,
}


struct Event {
    1: i32 eventId,
    2: i32 vehicleId,
	3: i32 missionId,
    4: i32 type,
    5: string description,
    6: i64 time,
}

struct Salinity {
    1: i32 salinityId,
    2: i32 missionId,
    3: i32 vehicleId,
    4: Position position,
    5: double salinity,
    6: i64 time,
}


//Service for Semantic Queries.
//----------------------------------------------
// Notice that both functions in this service are blocking functions. There is no callback defined in the MmtService for sending the result. 
// This is because the Mmt needs the lists in order to populate the interface with valid data.
//----------------------------------------------
service SemanticQueryService
{
    //Get Functions
	list<Task>      getAllTasks             (),
    list<Task>      getAllActions           (),
    list<Vehicle>   getAllVehicles          (),				
    i32             getNewMissionID         (),
    list<i32>       getAllMissionIDs        (),
    i32             getOngoingMissionID     (),                             //Added in Version9. Should return a negative value if there is no mission in progress
    Vehicle         getVehicle              (1:i32 vid),
    list<Salinity>  getOntologySalinity     (1:i32 missionId),
    list<Landmark>  getOntologyLandmarks    (1:i32 missionId),
    list<Event>     getEvents               (1:i32 missionId, 2:i64 timeReference),

    //Query Functions
    TimedSpeed          querySpeed              (1:Vehicle v),
    Position            queryPosition           (1:Vehicle v),
    Orientation         queryOrientation        (1:Vehicle v),
    list<Ph>            queryAllPh              (1:i32 missionId),
    list<H2S>           queryAllH2S             (1:i32 missionId),
    list<double>        queryRefCoords          (1:i32 missionId),
    list<Salinity>      queryAllSalinity        (1:i32 missionId),
    list<Landmark>      queryAllLandmarks       (1:i32 missionId),
    list<Temperature>   queryAllTemperature     (1:i32 missionId),
    list<Vehicle>       queryMissionStateVector (1:i32 missionId, 2:i64 timeReference),
    Vehicle             queryVehicleStateVector (1:i32 missionId, 2:i32 vehicleId, 3:i64 timeReference),    
    list<Ph>            queryPh                 (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),
    list<H2S>           queryH2S                (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),
    list<Current>       queryCurrent            (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),
    list<Pressure>      queryPressure           (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),
    list<Salinity>      querySalinity           (1:i32 missionID, 2:double latitude, 3:double longitude, 4:double radius), 
    list<Landmark>      queryLandmarks          (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),
    list<Temperature>   queryTemperature        (1:i32 missionId, 2:double latitude, 3:double longitude, 4:double radius),

    //Store Functions    
    oneway void storeEvent          (1:i32 missionId, 2:i32 vehicleId, 3:i32 subtype, 4:string description, 5:i64 timeReference),
    oneway void storePressure       (1:i32 missionId,2:double latitude,3:double longitude,4:double pressure,5:i64 timeReference),
    oneway void storePh             (1:i32 missionId,2:double latitude,3:double longitude,4:double depth,5:double ph,6:i64 timeReference),
    oneway void storeH2S            (1:i32 missionId,2:double latitude,3:double longitude,4:double depth,5:double h2s,6:i64 timeReference),   
    oneway void storeLandmarks      (1:i32 missionId,2:double latitude,3:double longitude,4:string name,5:string url,6:i64 timeReference),
    oneway void storeTemperature    (1:i32 missionId,2:double latitude,3:double longitude,4:double depth,5:double temperature,6:i64 timeReference),
    oneway void storeCurrent        (1:i32 missionId,2:double latitude,3:double longitude,4:double depth,5:double currentEast,6:double currentNorth,7:i64 timeReference),
    oneway void storeSalinity       (1:i32 missionId, 2:i32 vehicleId, 3:double latitude, 4:double longitude, 5:double depth, 6:double altitude, 7:double salinity, 8:i64 timeReference),
    
    //The Mighty Everlasting PINGGGGGGG
    string ping(),
}


//Service for MTRR
//----------------------------------------------
// This service exposes a function that will be called when a plan is to be executed.
//----------------------------------------------
service MtrrService
{
	oneway void requestUpdateStatus     (),                     //Added in Verison 9
    oneway void sendPlan                (1: Mission plan),
    
    string abortMissionPlan             (1: i32 missionId),
    string abortVehiclePlan             (1: i32 vehicleId),
    string abortMissionPlanHard         (1: i32 missionId),     //Added in Version 9
    string abortVehiclePlanHard         (1: i32 vehicleId),     //Added in Version 9

    //The King of the network functions, the PIIINNNGGGGG
    string ping(),
}

//Service for Planners
//----------------------------------------------
// Note that this is a non-blocking oneway function. 
// When the planning is done and the plan is ready, then the Planner must call the sendPlan function exposed by MmtService
//----------------------------------------------
service PlannerService
{
	oneway void computePlan(1: Mission context),
    //Hehe, you though there would be another ping comment here? No, sorry! we run out of them
    string ping(),
}

//Service for Selection
//----------------------------------------------
// Note that this is a non-blocking oneway function. 
// When a plan is chosen, then the selected one should be sent to MMT by calling the sendSelection function exposed by MmtService
service SelectionService
{
	oneway void choosePlan(1: list<Mission> plans),
    //Every service needs a good Ping, I am just wondering: who has the Pong??
    string ping(),
}

//Service for MMT
//----------------------------------------------
service MmtService
{
	oneway void sendUpdatedStatusNotification   (),                                         //Added in Version 9, notifies the MMT that all status reports from vehicles is received and updated
    
    oneway void sendPlan                        (1: Mission plan),							//Called by Planners in response to a computePlan. Sends the plan to Mmt
	oneway void sendSelection                   (1:Mission plan),						    //Called by Selection module in reponse to choosePlan. Sends the selected plan to Mmt
	oneway void sendError                       (1:i32 errorId, 2:string errorMessage),	    //Called by all in case something goes wrong. 
	oneway void sendStatusReport                (1:Action current),				            //Called by MTRR whenever there is a new update for a mission.
    
    //No Pingy, No Party!
    string ping(),
}
