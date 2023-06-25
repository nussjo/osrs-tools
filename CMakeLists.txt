cmake_minimum_required(VERSION 3.25)
project(osrs)

option(${PROJECT_NAME}_ENABLE_DEFAULT_WARNING_LEVELS "Default Warning Levels" ON)
option(${PROJECT_NAME}_ENABLE_DEFAULT_OPTIMIZATION_LEVELS "Default Optimization Levels" ON)

add_library(${PROJECT_NAME}_default_options INTERFACE)
add_library(${PROJECT_NAME}::default_options ALIAS ${PROJECT_NAME}_default_options)

if (${PROJECT_NAME}_ENABLE_DEFAULT_WARNING_LEVELS)
    target_compile_options(${PROJECT_NAME}_default_options
        INTERFACE
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Wall>
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Wextra>
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Wshadow>
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Wconversion>
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Wpedantic>
            $<$<CXX_COMPILER_ID:Clang,GNU>:-Werror>
    )
endif()

if (${PROJECT_NAME}_ENABLE_DEFAULT_OPTIMIZATION_LEVELS)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
    target_compile_options(${CMAKE_PROJECT_NAME}_default_options
        INTERFACE
            $<$<CONFIG:Debug>:-O0>
            $<$<CONFIG:Debug>:-U_FORTIFY_SOURCE>
            $<$<CONFIG:Release>:-O2>
    )
endif()

enable_testing()

add_subdirectory(components)
add_subdirectory(projects)
