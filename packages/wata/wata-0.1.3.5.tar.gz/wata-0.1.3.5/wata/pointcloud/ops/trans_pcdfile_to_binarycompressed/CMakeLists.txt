cmake_minimum_required(VERSION 3.10)  # 设置 CMake 的最低版本要求
project(savePSDFileBinaryCompressed)                   # 设置项目名称


# 查找 Boost 库
find_package(Boost  REQUIRED COMPONENTS filesystem)
find_package(PCL REQUIRED)


include_directories(${Boost_INCLUDE_DIRS} ${PCL_INCLUDE_DIRS})


link_directories(${PCL_LIBRARY_DIRS})

add_definitions(${PCL_DEFINITIONS})
add_definitions(-DPCL_NO_PRECOMPILE)

add_executable(savePSDFileBinaryCompressed savePSDFileBinaryCompressed.cpp)
target_link_libraries (savePSDFileBinaryCompressed ${PCL_LIBRARIES})
target_link_libraries(savePSDFileBinaryCompressed ${Boost_LIBRARIES})