// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "Carla.h"
#include "ReplaySystemDataRouter.h"

#include "Agent/ReplayLoggerAgentComponent.h"
#include "Agent/VehicleAgentComponent.h"

#include "Vehicle/CarlaWheeledVehicle.h"

AReplaySystemDataRouter::AReplaySystemDataRouter(const FObjectInitializer& ObjectInitializer)
  : Super(ObjectInitializer)
{
  PrimaryActorTick.bCanEverTick = true;
  PrimaryActorTick.bTickEvenWhenPaused = true;
  PrimaryActorTick.TickGroup = TG_PostPhysics;
}

AReplaySystemDataRouter::AReplaySystemDataRouter()
{
  PrimaryActorTick.bCanEverTick = true;
  PrimaryActorTick.bTickEvenWhenPaused = true;
  PrimaryActorTick.TickGroup = TG_PostPhysics;
}

void AReplaySystemDataRouter::Tick(float DeltaTime)
{
  Super::Tick(DeltaTime);

  for (int32_t i = 0; i < Agents.Num(); ++i)
  {
    Agents[i]->AcceptVisitor(*this);
  }

  // TODO(Andrei): Store the state to the file
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
