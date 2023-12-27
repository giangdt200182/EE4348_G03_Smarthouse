# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "D:/camBienHongNgoai/Espressif/frameworks/esp-idf-v5.0.1/components/bootloader/subproject"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/tmp"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/src/bootloader-stamp"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/src"
  "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "D:/camBienHongNgoai/Espressif/frameworks/tcp_mqtt_transmit_test_2/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
