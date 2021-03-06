cmake_minimum_required (VERSION 2.8)
project(a2vme)

# check for in-source build, forbid it!
if(CMAKE_BINARY_DIR STREQUAL CMAKE_SOURCE_DIR AND NOT MSVC_IDE)
  message(FATAL_ERROR "\nIn-source build attempt detected!\n"
    "Please create a new directory (e.g. build) and run `cmake ..`.\n"
    "Also don't forget to delete the created CMakeCache.txt and CMakeFiles dir"
    )
endif()

include(cmake/settings.cmake)
message(STATUS "*** Build Type:      " ${CMAKE_BUILD_TYPE})
message(STATUS "*** Compiler Flags:  " ${DEFAULT_COMPILE_FLAGS})
message(STATUS "*** Install libs to: " ${LIBRARY_OUTPUT_PATH})
message(STATUS "*** Install bin to:  " ${EXECUTABLE_OUTPUT_PATH})

# this does not use the standard vmelib
add_subdirectory(cb_disc)

# compile the VMEbus library (and some simple binaries) first...
add_subdirectory(vmebus)
# then all projects which depend on them...
add_subdirectory(taps_experiment_control)
add_subdirectory(PairSpectrometer)
add_subdirectory(moellerandmore_experiment_control)
add_subdirectory(moellerandmore)
add_subdirectory(Moeller)
add_subdirectory(flash)
add_subdirectory(vitec)
add_subdirectory(gesica_sadc)
