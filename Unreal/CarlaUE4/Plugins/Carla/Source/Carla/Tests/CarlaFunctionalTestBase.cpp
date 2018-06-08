// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#include "Carla.h"
#include "CarlaFunctionalTestBase.h"


void ACarlaFunctionalTestBase::Setup(const FString& mapname, TArray<AActor*> ais)
{
    /** @TODO: check that the map exists and the ais are valid */
    MapName = mapname;
    AITestList = ais;
    SetupDone = true; //<-- only if the checks are ok
    //If a Map should be loaded, Mark this actor and the actors it will use as
    // Persisting Actors across Seamless Travel
}

bool ACarlaFunctionalTestBase::RunTest(const TArray<FString>& Params)
{
    if (!SetupDone) return false;
    return Super::RunTest(Params);
}
