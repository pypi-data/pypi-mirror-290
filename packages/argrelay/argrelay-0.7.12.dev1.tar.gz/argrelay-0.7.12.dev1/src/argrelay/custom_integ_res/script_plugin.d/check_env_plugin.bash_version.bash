
########################################################################################################################
# Report `bash_version`:
# shellcheck disable=SC2154
if [[ -n "${BASH_VERSION+x}" ]]
then
    echo -e "${success_color}INFO:${reset_style} ${field_color}bash_version:${reset_style} ${BASH_VERSION}"
else
    echo -e "${failure_color}ERROR:${reset_style} ${field_color}bash_version:${reset_style} ${failure_message}# The env var is not defined: \`BASH_VERSION\`${reset_style}"
    exit 1
fi
