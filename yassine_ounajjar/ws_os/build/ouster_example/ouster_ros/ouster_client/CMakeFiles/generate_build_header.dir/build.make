# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ameise/Yassine_GIT/ws_os/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ameise/Yassine_GIT/ws_os/build

# Utility rule file for generate_build_header.

# Include the progress variables for this target.
include ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/progress.make

generate_build_header: ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/build.make
	cd /home/ameise/Yassine_GIT/ws_os/build/ouster_example/ouster_ros/ouster_client && /usr/bin/cmake -DVERSION_GEN_OUT_DIR="/home/ameise/Yassine_GIT/ws_os/build/ouster_example/ouster_ros/ouster_client/include/ouster" -DVERSION_GEN_SOURCE_DIR="/home/ameise/Yassine_GIT/ws_os/src/ouster_example/ouster_client/.." -DBUILD_TYPE="Release" -DBUILD_SYSTEM="Linux" -Douster_client_VERSION="0.3.0" -Douster_client_VERSION_SUFFIX="" -P /home/ameise/Yassine_GIT/ws_os/src/ouster_example/ouster_client/../cmake/VersionGen.cmake
.PHONY : generate_build_header

# Rule to build all files generated by this target.
ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/build: generate_build_header

.PHONY : ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/build

ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/clean:
	cd /home/ameise/Yassine_GIT/ws_os/build/ouster_example/ouster_ros/ouster_client && $(CMAKE_COMMAND) -P CMakeFiles/generate_build_header.dir/cmake_clean.cmake
.PHONY : ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/clean

ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/depend:
	cd /home/ameise/Yassine_GIT/ws_os/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ameise/Yassine_GIT/ws_os/src /home/ameise/Yassine_GIT/ws_os/src/ouster_example/ouster_client /home/ameise/Yassine_GIT/ws_os/build /home/ameise/Yassine_GIT/ws_os/build/ouster_example/ouster_ros/ouster_client /home/ameise/Yassine_GIT/ws_os/build/ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : ouster_example/ouster_ros/ouster_client/CMakeFiles/generate_build_header.dir/depend

