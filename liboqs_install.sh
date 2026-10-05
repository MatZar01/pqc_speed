cd /tmp

git clone --depth=1 https://github.com/open-quantum-safe/liboqs.git

cmake -S liboqs -B liboqs/build \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_BUILD_ONLY_LIB=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$CONDA_PREFIX"

cmake --build liboqs/build --parallel 8

cmake --build liboqs/build --target install