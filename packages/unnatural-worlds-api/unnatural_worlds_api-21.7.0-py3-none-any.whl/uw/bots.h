# 1 "../../c/uwapi/uwapi/bots.h"
# 1 "<built-in>" 1
# 1 "<built-in>" 3
# 385 "<built-in>" 3
# 1 "<command line>" 1
# 1 "<built-in>" 2
# 1 "../../c/uwapi/uwapi/bots.h" 2



# 1 "../../c/uwapi/uwapi/common.h" 1



# 1 "headers/stdbool.h" 1
# 5 "../../c/uwapi/uwapi/common.h" 2
# 1 "headers/stdint.h" 1
# 6 "../../c/uwapi/uwapi/common.h" 2

typedef uint8_t uint8;
typedef int8_t sint8;
typedef uint16_t uint16;
typedef int16_t sint16;
typedef uint32_t uint32;
typedef int32_t sint32;
typedef uint64_t uint64;
typedef int64_t sint64;
# 25 "../../c/uwapi/uwapi/common.h"
 static const uint32 UW_GameTicksPerSecond = 20;

 typedef struct UwIds
 {
  const uint32 *ids;
  uint32 count;
 } UwIds;



 typedef enum UwPrototypeTypeEnum
 {
  UwPrototypeTypeEnum_None = 0,
  UwPrototypeTypeEnum_Resource = 1,
  UwPrototypeTypeEnum_Recipe = 2,
  UwPrototypeTypeEnum_Construction = 3,
  UwPrototypeTypeEnum_Unit = 4,
 } UwPrototypeTypeEnum;
               void uwAllPrototypes(UwIds *data);
               UwPrototypeTypeEnum uwPrototypeType(uint32 prototypeId);
               const char *uwPrototypeJson(uint32 prototypeId);
               const char *uwDefinitionsJson(void);



 typedef struct UwMapInfo
 {
  const char *name;
  const char *guid;
  const char *path;
  uint32 maxPlayers;
 } UwMapInfo;
               bool uwMapInfo(UwMapInfo *data);



               uint32 uwTilesCount(void);
 typedef struct UwTile
 {
  float position[3];
  float up[3];
  const uint32 *neighborsIndices;
  uint32 neighborsCount;
  uint8 terrain;
  bool border;
 } UwTile;
               void uwTile(uint32 index, UwTile *data);



 typedef enum UwOverviewFlags
 {
  UwOverviewFlags_None = 0,
  UwOverviewFlags_Resource = 1 << 0,
  UwOverviewFlags_Construction = 1 << 1,
  UwOverviewFlags_MobileUnit = 1 << 2,
  UwOverviewFlags_StaticUnit = 1 << 3,
  UwOverviewFlags_Unit = UwOverviewFlags_MobileUnit | UwOverviewFlags_StaticUnit,
 } UwOverviewFlags;
               UwOverviewFlags uwOverviewFlags(uint32 position);
               void uwOverviewIds(uint32 position, UwIds *data);
 typedef struct UwOverviewExtract
 {
  const UwOverviewFlags *flags;
  uint32 count;
 } UwOverviewExtract;
               void uwOverviewExtract(UwOverviewExtract *data);



               void uwAreaRange(float x, float y, float z, float radius, UwIds *data);
               void uwAreaConnected(uint32 position, float radius, UwIds *data);
               void uwAreaNeighborhood(uint32 position, float radius, UwIds *data);
               void uwAreaExtended(uint32 position, float radius, UwIds *data);

               bool uwTestVisible(float x1, float y1, float z1, float x2, float y2, float z2);
               bool uwTestShooting(uint32 shooterPosition, uint32 shooterProto, uint32 targetPosition, uint32 targetProto);
               float uwDistanceLine(float x1, float y1, float z1, float x2, float y2, float z2);
               float uwDistanceEstimate(uint32 a, uint32 b);
               float uwYaw(uint32 position, uint32 towards);



 typedef struct UwEntity UwEntity;
               UwEntity *uwEntityPointer(uint32 id);
               uint32 uwEntityId(UwEntity *entity);
               void uwAllEntities(UwIds *data);



 typedef struct UwProtoComponent
 {
  uint32 proto;
 } UwProtoComponent;
               bool uwFetchProtoComponent(UwEntity *entity, UwProtoComponent *data);

 typedef struct UwOwnerComponent
 {
  uint32 force;
 } UwOwnerComponent;
               bool uwFetchOwnerComponent(UwEntity *entity, UwOwnerComponent *data);

 typedef struct UwControllerComponent
 {
  uint32 player;
  uint32 timestamp;
 } UwControllerComponent;
               bool uwFetchControllerComponent(UwEntity *entity, UwControllerComponent *data);

 typedef struct UwPositionComponent
 {
  uint32 position;
  float yaw;
 } UwPositionComponent;
               bool uwFetchPositionComponent(UwEntity *entity, UwPositionComponent *data);

 typedef enum UwUnitStateFlags
 {
  UwUnitStateFlags_None = 0,
  UwUnitStateFlags_Shooting = 1 << 0,
  UwUnitStateFlags_Processing = 1 << 1,
  UwUnitStateFlags_Rebuilding = 1 << 2,
 } UwUnitStateFlags;
 typedef struct UwUnitComponent
 {
  UwUnitStateFlags state;
  uint32 killCount;
 } UwUnitComponent;
               bool uwFetchUnitComponent(UwEntity *entity, UwUnitComponent *data);

 typedef struct UwLifeComponent
 {
  sint32 life;
 } UwLifeComponent;
               bool uwFetchLifeComponent(UwEntity *entity, UwLifeComponent *data);

 typedef struct UwMoveComponent
 {
  uint32 posStart;
  uint32 posEnd;
  uint32 tickStart;
  uint32 tickEnd;
  float yawStart;
  float yawEnd;
 } UwMoveComponent;
               bool uwFetchMoveComponent(UwEntity *entity, UwMoveComponent *data);

 typedef struct UwAimComponent
 {
  uint32 target;
 } UwAimComponent;
               bool uwFetchAimComponent(UwEntity *entity, UwAimComponent *data);

 typedef struct UwRecipeComponent
 {
  uint32 recipe;
 } UwRecipeComponent;
               bool uwFetchRecipeComponent(UwEntity *entity, UwRecipeComponent *data);

 typedef struct UwUpdateTimestampComponent
 {
  uint32 timestamp;
 } UwUpdateTimestampComponent;
               bool uwFetchUpdateTimestampComponent(UwEntity *entity, UwUpdateTimestampComponent *data);

 typedef struct UwRecipeStatisticsComponent
 {
  uint32 timestamps[3];
  uint32 completed;
 } UwRecipeStatisticsComponent;
               bool uwFetchRecipeStatisticsComponent(UwEntity *entity, UwRecipeStatisticsComponent *data);

 typedef enum UwPriorityEnum
 {
  UwPriorityEnum_Disabled = 0,
  UwPriorityEnum_Normal = 1,
  UwPriorityEnum_High = 2,
 } UwPriorityEnum;
 typedef struct UwPriorityComponent
 {
  UwPriorityEnum priority;
 } UwPriorityComponent;
               bool uwFetchPriorityComponent(UwEntity *entity, UwPriorityComponent *data);

 typedef struct UwAmountComponent
 {
  uint32 amount;
 } UwAmountComponent;
               bool uwFetchAmountComponent(UwEntity *entity, UwAmountComponent *data);

 typedef struct UwAttachmentComponent
 {
  uint32 target;
 } UwAttachmentComponent;
               bool uwFetchAttachmentComponent(UwEntity *entity, UwAttachmentComponent *data);

 typedef enum UwPlayerStateFlags
 {
  UwPlayerStateFlags_None = 0,
  UwPlayerStateFlags_Loaded = 1 << 0,
  UwPlayerStateFlags_Pause = 1 << 1,
  UwPlayerStateFlags_Disconnected = 1 << 2,
  UwPlayerStateFlags_Admin = 1 << 3,
 } UwPlayerStateFlags;
 typedef enum UwPlayerConnectionClassEnum
 {
  UwPlayerConnectionClassEnum_None = 0,
  UwPlayerConnectionClassEnum_Computer = 1,
  UwPlayerConnectionClassEnum_VirtualReality = 2,
  UwPlayerConnectionClassEnum_Robot = 3,
  UwPlayerConnectionClassEnum_UwApi = 4,
 } UwPlayerConnectionClassEnum;
 typedef struct UwPlayerComponent
 {
  char name[28];
  uint32 nameLength;
  uint64 steamUserId;
  uint32 force;
  float progress;
  uint32 ping;
  UwPlayerStateFlags state;
  UwPlayerConnectionClassEnum playerConnectionClass;
 } UwPlayerComponent;
               bool uwFetchPlayerComponent(UwEntity *entity, UwPlayerComponent *data);

 typedef enum UwForceStateFlags
 {
  UwForceStateFlags_None = 0,
  UwForceStateFlags_Winner = 1 << 0,
  UwForceStateFlags_Defeated = 1 << 1,
  UwForceStateFlags_Disconnected = 1 << 2,
 } UwForceStateFlags;
 typedef struct UwForceComponent
 {
  float color[3];
  uint64 score;
  uint32 killCount;
  uint32 lossCount;
  uint32 finishTimestamp;
  uint32 team;
  UwForceStateFlags state;
 } UwForceComponent;
               bool uwFetchForceComponent(UwEntity *entity, UwForceComponent *data);

 typedef struct UwForceDetailsComponent
 {
  uint64 killValue;
  uint64 lossValue;
  uint32 startingPosition;
 } UwForceDetailsComponent;
               bool uwFetchForceDetailsComponent(UwEntity *entity, UwForceDetailsComponent *data);

 typedef enum UwForeignPolicyEnum
 {
  UwForeignPolicyEnum_None = 0,
  UwForeignPolicyEnum_Self = 1,
  UwForeignPolicyEnum_Ally = 2,
  UwForeignPolicyEnum_Neutral = 3,
  UwForeignPolicyEnum_Enemy = 4,
 } UwForeignPolicyEnum;
 typedef struct UwForeignPolicyComponent
 {
  uint32 forces[2];
  UwForeignPolicyEnum policy;
 } UwForeignPolicyComponent;
               bool uwFetchForeignPolicyComponent(UwEntity *entity, UwForeignPolicyComponent *data);

 typedef struct UwDiplomacyProposalComponent
 {
  uint32 offeror;
  uint32 offeree;
  UwForeignPolicyEnum proposal;
 } UwDiplomacyProposalComponent;
               bool uwFetchDiplomacyProposalComponent(UwEntity *entity, UwDiplomacyProposalComponent *data);
# 5 "../../c/uwapi/uwapi/bots.h" 2








 static const uint32 UW_VERSION = 21;
               void uwInitialize(uint32 version);
               void uwDeinitialize(void);

 typedef void (*UwExceptionCallbackType)(const char *message);
               void uwSetExceptionCallback(UwExceptionCallbackType callback);

 typedef enum UwSeverityEnum
 {
  UwSeverityEnum_Note = 0,
  UwSeverityEnum_Hint = 1,
  UwSeverityEnum_Warning = 2,
  UwSeverityEnum_Info = 3,
  UwSeverityEnum_Error = 4,
  UwSeverityEnum_Critical = 5,
 } UwSeverityEnum;
 typedef struct UwLogCallback
 {
  const char *message;
  const char *component;
  UwSeverityEnum severity;
 } UwLogCallback;
 typedef void (*UwLogCallbackType)(const UwLogCallback *data);
               void uwSetLogCallback(UwLogCallbackType callback);
               void uwLog(UwSeverityEnum severity, const char *message);

 typedef struct UwAssistConfig
 {
  bool logistics;
  bool aiming;
  bool fighting;
  bool retaliations;
 } UwAssistConfig;
               void uwSetAssistConfig(const UwAssistConfig *config);

               void uwSetPlayerName(const char *name);
               void uwSetPlayerColor(float r, float g, float b);
               void uwSetConnectStartGui(bool enabled, const char *extraCmdParams);
               void uwSetConnectAsObserver(bool observer);

               bool uwConnectFindLan(uint64 timeoutMicroseconds);
               void uwConnectDirect(const char *address, uint16 port);
               void uwConnectLobbyId(uint64 lobbyId);
               void uwConnectNewServer(uint32 visibility, const char *name, const char *extraCmdParams);
               bool uwTryReconnect(void);
               void uwDisconnect(void);



 typedef enum UwConnectionStateEnum
 {
  UwConnectionStateEnum_None = 0,
  UwConnectionStateEnum_Connecting = 1,
  UwConnectionStateEnum_Connected = 2,
  UwConnectionStateEnum_Disconnecting = 3,
  UwConnectionStateEnum_Error = 4,
 } UwConnectionStateEnum;
 typedef void (*UwConnectionStateCallbackType)(UwConnectionStateEnum state);
               void uwSetConnectionStateCallback(UwConnectionStateCallbackType callback);
               UwConnectionStateEnum uwConnectionState(void);

 typedef enum UwGameStateEnum
 {
  UwGameStateEnum_None = 0,
  UwGameStateEnum_Session = 1,
  UwGameStateEnum_Preparation = 2,
  UwGameStateEnum_Game = 3,
  UwGameStateEnum_Finish = 4,
 } UwGameStateEnum;
 typedef void (*UwGameStateCallbackType)(UwGameStateEnum state);
               void uwSetGameStateCallback(UwGameStateCallbackType callback);
               UwGameStateEnum uwGameState(void);

 typedef enum UwMapStateEnum
 {
  UwMapStateEnum_None = 0,
  UwMapStateEnum_Downloading = 1,
  UwMapStateEnum_Loading = 2,
  UwMapStateEnum_Loaded = 3,
  UwMapStateEnum_Unloading = 4,
  UwMapStateEnum_Error = 5,
 } UwMapStateEnum;
 typedef void (*UwMapStateCallbackType)(UwMapStateEnum state);
               void uwSetMapStateCallback(UwMapStateCallbackType callback);
               UwMapStateEnum uwMapState(void);

 typedef void (*UwUpdateCallbackType)(uint32 tick, bool stepping);
               void uwSetUpdateCallback(UwUpdateCallbackType callback);



 typedef struct UwShootingUnit
 {
  uint32 position;
  uint32 force;
  uint32 prototype;
  uint32 id;
 } UwShootingUnit;
 typedef struct UwShootingData
 {
  UwShootingUnit shooter;
  UwShootingUnit target;
 } UwShootingData;
 typedef struct UwShootingArray
 {
  const UwShootingData *data;
  uint32 count;
 } UwShootingArray;
 typedef void (*UwShootingCallbackType)(const UwShootingArray *data);
               void uwSetShootingCallback(UwShootingCallbackType callback);



 typedef struct UwMyPlayer
 {
  uint32 playerEntityId;
  uint32 forceEntityId;
  bool primaryController;
  bool admin;
 } UwMyPlayer;
               bool uwMyPlayer(UwMyPlayer *data);



               void uwModifiedEntities(UwIds *data);



               bool uwTestConstructionPlacement(uint32 constructionPrototype, uint32 position);
               uint32 uwFindConstructionPlacement(uint32 constructionPrototype, uint32 position);



 typedef enum UwOrderTypeEnum
 {
  UwOrderTypeEnum_None = 0,
  UwOrderTypeEnum_Stop = 1,
  UwOrderTypeEnum_Guard = 2,
  UwOrderTypeEnum_Run = 3,
  UwOrderTypeEnum_Fight = 4,
  UwOrderTypeEnum_Load = 5,
  UwOrderTypeEnum_Unload = 6,
  UwOrderTypeEnum_SelfDestruct = 7,
 } UwOrderTypeEnum;
 typedef enum UwOrderPriorityFlags
 {
  UwOrderPriorityFlags_None = 0,
  UwOrderPriorityFlags_Assistant = 1 << 0,
  UwOrderPriorityFlags_User = 1 << 1,
  UwOrderPriorityFlags_Enqueue = 1 << 2,
  UwOrderPriorityFlags_Repeat = 1 << 3,
 } UwOrderPriorityFlags;
 typedef struct UwOrder
 {
  uint32 entity;
  uint32 position;
  UwOrderTypeEnum order;
  UwOrderPriorityFlags priority;
 } UwOrder;
               void uwOrder(uint32 unit, const UwOrder *data);
 typedef struct UwOrders
 {
  const UwOrder *orders;
  uint32 count;
 } UwOrders;
               void uwOrders(uint32 unit, UwOrders *data);



               void uwCommandPlaceConstruction(uint32 proto, uint32 position, float yaw);
               void uwCommandSetRecipe(uint32 unit, uint32 recipe);
               void uwCommandSetPriority(uint32 unit, UwPriorityEnum priority);
               void uwCommandLoad(uint32 unit, uint32 resourceType);
               void uwCommandUnload(uint32 unit);
               void uwCommandMove(uint32 unit, uint32 position, float yaw);
               void uwCommandAim(uint32 unit, uint32 target);
               void uwCommandRenounceControl(uint32 unit);
               void uwCommandSelfDestruct(uint32 unit);



               uint64 uwGetLobbyId(void);
               uint64 uwGetUserId(void);
               uint16 uwGetServerPort(void);
               void uwAdminKickPlayer(uint32 player);
               void uwAdminPlayerSetAdmin(uint32 player, bool admin);
               void uwAdminPlayerSetName(uint32 player, const char *name);
               void uwAdminPlayerJoinForce(uint32 player, uint32 force);
               void uwAdminForceJoinTeam(uint32 force, uint32 team);
               void uwAdminForceSetColor(uint32 force, float r, float g, float b);
               void uwAdminAddAi(void);
               void uwAdminStartGame(void);
               void uwAdminTerminateGame(void);
               void uwAdminSetGameSpeed(float speed);
               void uwAdminSetWeatherSpeed(float speed, float offset);
               void uwSendCameraSuggestion(uint32 position);
               void uwSendMapSelection(const char *path);
