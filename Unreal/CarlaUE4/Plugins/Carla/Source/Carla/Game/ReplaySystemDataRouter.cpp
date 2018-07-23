// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "Carla.h"
#include "CoreGlobals.h"
#include "ReplaySystemDataRouter.h"

#include "Agent/ReplayLoggerAgentComponent.h"
#include "Agent/VehicleAgentComponent.h"

#include "Vehicle/CarlaWheeledVehicle.h"

#include <fstream>
#include <ctime>

AReplaySystemDataRouter::AReplaySystemDataRouter(const FObjectInitializer& ObjectInitializer)
  : Super(ObjectInitializer)
{
  Init();
}

AReplaySystemDataRouter::AReplaySystemDataRouter()
{
  Init();
}

void AReplaySystemDataRouter::Init()
{
  PrimaryActorTick.bCanEverTick = true;
  PrimaryActorTick.bTickEvenWhenPaused = true;
  PrimaryActorTick.TickGroup = TG_PostPhysics;

  time_t rawtime;
  struct tm timeinfo = { 0 };

  time(&rawtime);
  localtime_s(&timeinfo, &rawtime);

  strftime(SimulationSaveFile, sizeof(SimulationSaveFile), "simulation_%d%m%Y_%H%M%S.dat", &timeinfo);
}

void AReplaySystemDataRouter::Tick(float DeltaTime)
{
  Super::Tick(DeltaTime);

  GameTimeStamp += DeltaTime;
  std::ofstream OutputFile(SimulationSaveFile, std::ofstream::binary | std::ofstream::app);

  if (false == OutputFile.is_open())
  {
    UE_LOG(LogCarla, Error, TEXT("Can not open file \"%s\" for saving the replay information"), UTF8_TO_TCHAR(SimulationSaveFile));
    return;
  }

  for (int32_t i = 0; i < Agents.Num(); ++i)
  {
    Agents[i]->AcceptVisitor(*this);
  }

  ObjectState::FFrameObject FrameObject = { 0 };
  FrameObject.NumberOfObject = ObjetsState.Num();

  FrameObject.GameTime = GameTimeStamp;
  FrameObject.FrameCounter = GFrameCounter;
  FrameObject.PlatformTime = FPlatformTime::Seconds();

  OutputFile.write(reinterpret_cast<const char *>(&FrameObject), sizeof(ObjectState::FFrameObject));

  for (int32_t i = 0; i < ObjetsState.Num(); ++i)
  {
    size_t DataSize = 0;

    switch (ObjetsState[i].Header.type)
    {
      case ObjectState::ObjectType::Vehicle:
      {
        DataSize = sizeof(ObjectState::FVehicleState);
      } break;

      case ObjectState::ObjectType::Walker:
      {
        DataSize = sizeof(ObjectState::FWalkerState);
      } break;
    }

    OutputFile.write (reinterpret_cast<const char *>(&ObjetsState[i]), DataSize);
  }

  OutputFile.close();
  ObjetsState.Reset();
}

void AReplaySystemDataRouter::Visit(const UTrafficSignAgentComponent &Agent)
{

}

void AReplaySystemDataRouter::Visit(const UVehicleAgentComponent &Agent)
{
  ObjectState::FObjectState ObjState;

  ObjState.Header.type = ObjectState::ObjectType::Vehicle;
  ObjState.Header.Id = Agent.GetId();

  FTransform Transform = Agent.GetTransform();
  const ACarlaWheeledVehicle *Vehicle = Agent.GetVehicle();

  ObjState.Vehicle.Transform.Position.x = Transform.GetLocation().X;
  ObjState.Vehicle.Transform.Position.y = Transform.GetLocation().Y;
  ObjState.Vehicle.Transform.Position.z = Transform.GetLocation().Z;

  ObjState.Vehicle.Transform.Scale.x = Transform.GetScale3D().X;
  ObjState.Vehicle.Transform.Scale.x = Transform.GetScale3D().X;
  ObjState.Vehicle.Transform.Scale.x = Transform.GetScale3D().X;

  ObjState.Vehicle.Transform.Rotation.w = Transform.GetRotation().W;
  ObjState.Vehicle.Transform.Rotation.x = Transform.GetRotation().X;
  ObjState.Vehicle.Transform.Rotation.y = Transform.GetRotation().Y;
  ObjState.Vehicle.Transform.Rotation.z = Transform.GetRotation().Z;

  ObjState.Vehicle.CurrentGear = Vehicle->GetVehicleCurrentGear();

  //TODO(Andrei): Add break, throttle, acceleration, hand break, speed limit

  ObjState.Vehicle.Brake = 0.0f;
  ObjState.Vehicle.Throttle = 0.0f;
  ObjState.Vehicle.HandBreak = false;

  ObjState.Vehicle.SpeedLimit = 0;
  ObjState.Vehicle.Acceleration = { 0, 0, 0 };
}

void AReplaySystemDataRouter::Visit(const UWalkerAgentComponent &Agent)
{

}
