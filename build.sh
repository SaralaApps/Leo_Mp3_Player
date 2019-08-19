#!/usr/bin/env bash
VERSION=`cat version.txt`

echo "Packaging demo program..."
rm -rf dist build
python setup.py bdist_wheel

COPY_DIR="cvap-age-demo-${VERSION}/"
LOGGING_FILE='logging_config.yaml'
CONFIG_FILE='configure_package.py'

rm -rf $COPY_DIR
mkdir $COPY_DIR -p

for file in dist/*; do
  WHL_FILE=$(basename $file)
  cp $file $COPY_DIR
done
cp $LOGGING_FILE "${COPY_DIR}"
cp $CONFIG_FILE "${COPY_DIR}"

CONFIGS_DIR="~/Apps/volume/cvap/configs"
echo "Creating install script"
echo "echo Installing Age Verification Demo" >> "${COPY_DIR}install.sh"
echo "pip install ${WHL_FILE} -U" >> "${COPY_DIR}/install.sh"
echo "cp -n ${LOGGING_FILE} ${CONFIGS_DIR}" >> "${COPY_DIR}install.sh"
echo "python ${CONFIG_FILE}" >> "${COPY_DIR}install.sh"

tar -czvf "age_demo-${VERSION}.tar.gz" "${COPY_DIR}"
rm -rf $COPY_DIR









