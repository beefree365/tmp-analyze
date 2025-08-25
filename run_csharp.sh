#!/bin/bash
# 编译并运行 RecursiveFilter.cs
set -e
mcs -langversion:5 RecursiveFilter.cs
mono RecursiveFilter.exe
