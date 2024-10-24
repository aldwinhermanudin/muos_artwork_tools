#!/bin/bash

#set -e

readonly BOX_DIRECTORY_NAME="box"
readonly PREVIEW_DIRECTORY_NAME="preview"
readonly TEXT_DIRECTORY_NAME="text"
readonly TEXT_GENERATOR_SCRIPT="gamelist_to_muostext.py"
readonly GAMELIST_FILENAME="gamelist.xml"

source=${1}      # locations of all the roms including the ${artwork_dir} folder
dest=${2}        # path to the final artwork location
artwork_dir=${3} # all box preview and gamelist.xml should be in this name under ${source}

# usage ./process_skraper_artwork.sh ROMS ArtWork muos_media

# copy artwork to new folder and generate the text directory
find $source -type d -name "${artwork_dir}" | while IFS= read -r dir; do
    
    # copy any artwork per to a new folder separated per system
    echo "Looking for Artwork under ${dir}"
    system="${dir/ROMS\//}"
    system="${system/\/muos_media/}"

    new_dir="${dest}/${system}"
    mkdir -p "${new_dir}"
    cp -rf "${dir}"/* "${new_dir}"

    # generate text game description folder and file
    echo "Generating text game description"
    text_dir=${new_dir}/${TEXT_DIRECTORY_NAME}
    mkdir -p "${text_dir}"
    python3 ${TEXT_GENERATOR_SCRIPT} --input-file "${new_dir}/${GAMELIST_FILENAME}" --output-directory "${text_dir}"
    
    # clean-up any gamelist.xml or gamelist.serialmissing.txt
    rm -rf "${new_dir}"/*.{xml,txt}

    echo ""
done

# flatten the box directory
find ${dest} -type d -name "${BOX_DIRECTORY_NAME}" | while IFS= read -r dir; do
    echo "Flattening ${BOX_DIRECTORY_NAME} directory: $dir"
    find "${dir}" -mindepth 2 -type f -exec mv "{}" "${dir}" \;
    find "${dir}" -mindepth 1 -type d -exec rmdir "{}" \;

    # find "${dir}" -mindepth 2 -type f -exec echo "Move {}" to "${dir}" \; -exec mv "{}" "${dir}" \;
    # find "${dir}" -mindepth 1 -type d -exec echo "Removing {}" \; -exec rmdir "{}" \;
    echo ""
done

# flatten the preview directory
find ${dest} -type d -name "${PREVIEW_DIRECTORY_NAME}" | while IFS= read -r dir; do
    echo "Flattening ${PREVIEW_DIRECTORY_NAME} directory: $dir"
    find "${dir}" -mindepth 2 -type f -exec mv "{}" "${dir}" \;
    find "${dir}" -mindepth 1 -type d -exec rmdir "{}" \;

    # find "${dir}" -mindepth 2 -type f -exec echo "Move {}" to "${dir}" \; -exec mv "{}" "${dir}" \;
    # find "${dir}" -mindepth 1 -type d -exec echo "Removing {}" \; -exec rmdir "{}" \;
done
