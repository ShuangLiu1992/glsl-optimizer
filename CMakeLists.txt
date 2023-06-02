cmake_minimum_required(VERSION 3.22)

project(glsl_opt C CXX)

include_directories(./include)
include_directories(./src/mesa)
include_directories(./src/mapi)
include_directories(./src/glsl)
include_directories(./src)

file(GLOB glcpp-library_sources ./src/glsl/glcpp/*.c ./src/util/*.c)
add_library(glcpp-library ${glcpp-library_sources})

file(GLOB mesa_sources ./src/mesa/program/*.c ./src/mesa/main/*.c)
add_library(mesa ${mesa_sources})

file(GLOB glsl_sources ./src/glsl/*.cpp ./src/glsl/*.c)
file(GLOB glsl_sources_remove ./src/glsl/main.cpp ./src/glsl/builtin_stubs.cpp)
list(REMOVE_ITEM glsl_sources ${glsl_sources_remove})
add_library(glsl_optimizer ${glsl_sources})
target_link_libraries(glsl_optimizer glcpp-library mesa)

install(TARGETS glcpp-library mesa glsl_optimizer
        RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        )