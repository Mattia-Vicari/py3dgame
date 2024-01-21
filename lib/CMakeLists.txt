# Minimum CMake version required
cmake_minimum_required(VERSION 3.10)

# Project name and language
project(Py3dGame CXX)

# Set a variable for the DLL name
set(DLL_NAME rendering)

# Add your source files for the library
add_library(${DLL_NAME} SHARED
    rendering.cpp
)

# Include directories
target_include_directories(${DLL_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Any additional configurations, dependencies, etc.
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
