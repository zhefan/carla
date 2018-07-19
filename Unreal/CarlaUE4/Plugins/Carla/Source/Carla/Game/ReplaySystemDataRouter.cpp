// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "Carla.h"
#include "ReplaySystemDataRouter.h"

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
}
