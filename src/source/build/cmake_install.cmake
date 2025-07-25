# Install script for directory: /nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux" TYPE EXECUTABLE FILES "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/bin/linux/DualSPHysics5.4CPU_linux64")
  if(EXISTS "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64"
         OLD_RPATH "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../lib/linux_gcc:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/../../bin/linux/DualSPHysics5.4CPU_linux64")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/src/source/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
