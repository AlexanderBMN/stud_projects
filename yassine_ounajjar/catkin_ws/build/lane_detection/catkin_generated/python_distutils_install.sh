#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ameise/Yassine_GIT/catkin_ws/src/diy_driverless_car_ROS/rover_cv/lane_detection"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ameise/Yassine_GIT/catkin_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ameise/Yassine_GIT/catkin_ws/install/lib/python2.7/dist-packages:/home/ameise/Yassine_GIT/catkin_ws/build/lane_detection/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ameise/Yassine_GIT/catkin_ws/build/lane_detection" \
    "/usr/bin/python2" \
    "/home/ameise/Yassine_GIT/catkin_ws/src/diy_driverless_car_ROS/rover_cv/lane_detection/setup.py" \
     \
    build --build-base "/home/ameise/Yassine_GIT/catkin_ws/build/lane_detection" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ameise/Yassine_GIT/catkin_ws/install" --install-scripts="/home/ameise/Yassine_GIT/catkin_ws/install/bin"
