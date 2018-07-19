#pragma once

#include <cstdint>
#include <vector>

namespace ObjectState
{
  // @}
  // =============================================================================
  // -- Enum  --------------------------------------------------------------------
  // =============================================================================
  // @{

  enum class ObjectType : int32_t
  {
    Vehicle,
    Walker,

    // NOTE(Andrei): Put above this line all the data
    Counter
  };

  // @}
  // =============================================================================
  // -- Data structures ----------------------------------------------------------
  // =============================================================================
  // @{

  union F3DVector
  {
    struct { float x, y, z; };
    float u[3];
  };

  union FQuaternion
  {
    struct { float w, x, y, z; };
    float u[4];
  };

  struct FObjectTransform
  {
    F3DVector Translation, Scale;
    FQuaternion Rotation;
  }; // NOTE(Andrei): 40 bytes;

  struct FVehicleState
  {
    FObjectTransform Transform;
    F3DVector Acceleration;
    F3DVector Position;

    float Brake;
    float Throttle;
    float SpeedLimit;

    int32_t HandBreak;
    int32_t CurrentGear;
  }; // NOTE(Andrei): 84 bytes;

  struct FWalkerState
  {
    FObjectTransform Transform;
    F3DVector Position;

    int32_t WalkerStatus;
    float TimeInState;
  }; // NOTE(Andrei): 60 bytes

  struct FObjectHeader
  {
    int32_t Id;
    ObjectType type;
  }; // NOTE(Andrei): 8 bytes

  struct FObjectState
  {
    FObjectHeader Header;

    union
    {
      FVehicleState Vehicle;
      FWalkerState Walker;
    };
  }; // NOTE(Andrei): 92 bytes;

  struct FFrameObject
  {
    uint64_t NumberOfObject;  // NOTE(Andrei): Keep track of how many objects there are per frame
    uint64_t FrameCounter;    // NOTE(Andrei): Frame counter is not reset per episodes
    uint32_t PlatformTime;    // NOTE(Andrei): This is the current hour in seconds
    uint32_t GameTime;        // NOTE(Andrei): Game time is reset per episode
  }; // NOTE(Andrei): 24 bytes

  // @}
  // =============================================================================
  // -- Possible format ----------------------------------------------------------
  // =============================================================================
  // @{

  /*
      FFrameObject | FObjectState | FObjectState | ... | FFrameObject | FObjectState | FObjectState | ...
  */
}
