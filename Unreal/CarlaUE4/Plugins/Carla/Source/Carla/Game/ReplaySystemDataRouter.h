// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include "GameFramework/Actor.h"

#include "Agent/AgentComponentVisitor.h"

#include "Util/ObjectState.h"

#include "ReplaySystemDataRouter.generated.h"



class UReplayLoggerAgentComponent;

UCLASS()
class CARLA_API AReplaySystemDataRouter : public AActor, public IAgentComponentVisitor
{
  GENERATED_BODY()

public:

  AReplaySystemDataRouter(const FObjectInitializer& ObjectInitializer);
  AReplaySystemDataRouter();

	void RegisterAgent(const UReplayLoggerAgentComponent *Agent)
	{
		check(Agent != nullptr);
		Agents.Emplace(Agent);
	}

	void DeregisterAgent(const UReplayLoggerAgentComponent *Agent)
	{
		check(Agent != nullptr);
		Agents.RemoveSwap(Agent);
	}

	const TArray<const UReplayLoggerAgentComponent *> &GetAgents() const
	{
		return Agents;
	}

  void Tick(float DeltaTime) override;

  virtual void Visit(const UTrafficSignAgentComponent &) override;
  virtual void Visit(const UVehicleAgentComponent &) override;
  virtual void Visit(const UWalkerAgentComponent &) override;

private:

	TArray<const UReplayLoggerAgentComponent *> Agents;
  TArray<ObjectState::FObjectState> ObjetsState;
};
