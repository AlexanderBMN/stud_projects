execute_process(COMMAND "/home/ameise/Yassine_GIT/catkin_ws/build/camera_cal/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/ameise/Yassine_GIT/catkin_ws/build/camera_cal/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
