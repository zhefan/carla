// Copyright (c) 2018 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.
#pragma once

#include "CoreMinimal.h"
#include "FunctionalTest.h"
#include "CarlaFunctionalTestBase.generated.h"

//class ACarlaFunctionalAITest;

/**
 * Class to perform unit and functional tests with CARLA
 */
UCLASS(Blueprintable, BlueprintType)
class CARLA_API ACarlaFunctionalTestBase : public AFunctionalTest
{
	GENERATED_BODY()
	
public:
    /** Setup the test before running it */
    void Setup(const FString& mapname, TArray<AActor*> ais);

    virtual bool RunTest(const TArray<FString>& Params = TArray<FString>()) override;;
	
private:
    /** Map name (level) to load to perform the tests */
    UPROPERTY(VisibleAnywhere)
    FString MapName;

    /** List of AIs to test. They will try to spawn and check conditions for tests */
    UPROPERTY(VisibleAnywhere)
    TArray<AActor*> AITestList;

    /** Flag to know if the test is configured already */
    UPROPERTY(VisibleAnywhere)
    bool SetupDone = false;
};
