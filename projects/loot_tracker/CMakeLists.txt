cmake_minimum_required(VERSION 3.25)
project(loot_tracker)

add_executable(${PROJECT_NAME})
add_executable(osrs::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE main.cpp)
