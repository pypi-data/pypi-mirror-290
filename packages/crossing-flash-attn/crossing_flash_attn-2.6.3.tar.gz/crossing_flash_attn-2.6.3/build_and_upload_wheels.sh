#!/bin/bash
set -e

PYTHON_VERSIONS="3.8.19 3.9.19 3.10.14 3.11.7"
TORCH_VERSIONS="2.1.2 2.4.0"
CUDA_TOOLKIT_VERSIONS="12-4"
BUILD_FORCE_CXX11_ABI=FALSE
GIT_SHA=$(git rev-parse HEAD)
DIST_DIR=$(pwd)/dist/${GIT_SHA}
rm -rf $DIST_DIR && mkdir -p $DIST_DIR

echo "Building wheels for torch versions: ${TORCH_VERSIONS}"
echo "Building wheels for cuda versions: ${CUDA_TOOLKIT_VERSIONS}"
echo "Building wheels for python versions: ${PYTHON_VERSIONS}"
echo "Building wheels in directory: ${DIST_DIR}"

echo "Building flash-attention wheels"
for CUDA_TOOLKIT_VERSION in ${CUDA_TOOLKIT_VERSIONS}; do
    for TORCH_VERSION in ${TORCH_VERSIONS}; do
        for PYTHON_VERSION in ${PYTHON_VERSIONS}; do
            BUILDER_IMAGE_NAME="flash-attn-builder:cudatoolkit-${CUDA_TOOLKIT_VERSION}-torch-${TORCH_VERSION}-python-${PYTHON_VERSION}"
            BUILDER_CONTAINER_NAME="flash-attn-builder-cudatoolkit-${CUDA_TOOLKIT_VERSION}-torch-${TORCH_VERSION}-python-${PYTHON_VERSION}"
            docker stop $BUILDER_CONTAINER_NAME || true
            
            echo "Building image with BUILDER_IMAGE_NAME: ${BUILDER_IMAGE_NAME}"
            docker build . -f Dockerfile.builder -t ${BUILDER_IMAGE_NAME} \
            --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
            --build-arg TORCH_VERSION=${TORCH_VERSION} \
            --build-arg CUDA_TOOLKIT_VERSION=${CUDA_TOOLKIT_VERSION}
            
            docker run --rm -d --name $BUILDER_CONTAINER_NAME -w /workspace ${BUILDER_IMAGE_NAME} sleep infinity
            docker cp . $BUILDER_CONTAINER_NAME:/workspace
            docker exec -e FLASH_ATTENTION_FORCE_BUILD=TRUE $BUILDER_CONTAINER_NAME python setup.py bdist_wheel --dist-dir=dist
            CUDA_VERSION=$(docker exec $BUILDER_CONTAINER_NAME python -W ignore::UserWarning -c "import torch; print(torch.version.cuda.replace('.', ''))")
            TMPNAME=cu${CUDA_VERSION}torch$(echo $TORCH_VERSION | sed 's/\.[0-9]*$//')cxx11abi$BUILD_FORCE_CXX11_ABI
            WHEEL_NAME=$(docker exec -e TMPNAME=$TMPNAME $BUILDER_CONTAINER_NAME bash -c 'ls dist/*whl | xargs -n 1 basename | sed "s/-/_$TMPNAME-/2"')
            docker exec -e WHEEL_NAME=$WHEEL_NAME $BUILDER_CONTAINER_NAME bash -c 'ls dist/*whl |xargs -I {} mv {} dist/$WHEEL_NAME'
            docker cp $BUILDER_CONTAINER_NAME:/workspace/dist/${WHEEL_NAME} ${DIST_DIR}/${WHEEL_NAME}
            docker stop $BUILDER_CONTAINER_NAME
        done
    done
done

echo "Building flash-attention sdist"
FLASH_ATTENTION_SKIP_CUDA_BUILD=TRUE python setup.py sdist --dist-dir $DIST_DIR

echo "Uploading wheels to OSS"
CROSSING_EXTENSION_OSS_DIR=oss://silicon-public/siliconllm/crossing-extension/crossing-flash-attention
OSS_CONFIG_PATH=$HOME/.ossutilconfig

SRC_PATH=${DIST_DIR}/
DST_PATH=$CROSSING_EXTENSION_OSS_DIR/$GIT_SHA
ossutil64 cp --disable-ignore-error --update --config-file $OSS_CONFIG_PATH -r $SRC_PATH $DST_PATH

echo "Update the latest version"
SRC_PATH=$CROSSING_EXTENSION_OSS_DIR/$GIT_SHA/
DST_PATH=$CROSSING_EXTENSION_OSS_DIR/latest
ossutil64 cp --disable-ignore-error --update --config-file $OSS_CONFIG_PATH -r $SRC_PATH $DST_PATH

