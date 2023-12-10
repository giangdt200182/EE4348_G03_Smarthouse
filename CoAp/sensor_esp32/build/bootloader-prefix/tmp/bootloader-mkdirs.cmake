# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "D:/esp/Espressif/frameworks/esp-idf-v4.4.5/components/bootloader/subproject"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix/tmp"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix/src/bootloader-stamp"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix/src"
  "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/EE4843_G3/EE4348_G03_Smarthouse/CoAp/sensor_esp32/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
