# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "D:/esp/Espressif/frameworks/esp-idf-v4.4.5/components/bootloader/subproject"
  "D:/Cambienngoainha/coap_server/build/bootloader"
  "D:/Cambienngoainha/coap_server/build/bootloader-prefix"
  "D:/Cambienngoainha/coap_server/build/bootloader-prefix/tmp"
  "D:/Cambienngoainha/coap_server/build/bootloader-prefix/src/bootloader-stamp"
  "D:/Cambienngoainha/coap_server/build/bootloader-prefix/src"
  "D:/Cambienngoainha/coap_server/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/Cambienngoainha/coap_server/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
