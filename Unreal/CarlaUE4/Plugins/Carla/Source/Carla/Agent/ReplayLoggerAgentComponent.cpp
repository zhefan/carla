// Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

#include "Carla.h"
#include "ReplayLoggerAgentComponent.h"
#include "Engine/World.h"
#include "Game/CarlaGameModeBase.h"
#include "Game/DataRouter.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"

static AReplaySystemDataRouter *GetReplaySystemDataRouter(UWorld *World)
{
	check(World != nullptr);
	ACarlaGameModeBase *GameMode = Cast<ACarlaGameModeBase>(World->GetAuthGameMode());

	check(GameMode != nullptr);
	return GameMode->GetReplaySystemDataRoute();
}

UReplayLoggerAgentComponent::UReplayLoggerAgentComponent(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	bVisible = false;
	bHiddenInGame = true;
	bShouldUpdatePhysicsVolume = false;
	PrimaryComponentTick.bCanEverTick = false;

}

void UReplayLoggerAgentComponent::AcceptVisitor(IAgentComponentVisitor &Visitor) const
{
	unimplemented();
}

void UReplayLoggerAgentComponent::BeginPlay()
{
	Super::BeginPlay();

	if (bRegisterReplayLoggerAgentComponent)
	{
		GetReplaySystemDataRouter(GetWorld())->RegisterAgent(this);
		bAgentReplayLoggerComponentIsRegistered = true;
	}
}

void UReplayLoggerAgentComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (bAgentReplayLoggerComponentIsRegistered)
	{
		GetReplaySystemDataRouter(GetWorld())->DeregisterAgent(this);
		bAgentReplayLoggerComponentIsRegistered = false;
	}

	Super::EndPlay(EndPlayReason);
}

