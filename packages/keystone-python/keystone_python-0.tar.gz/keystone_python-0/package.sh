#!/bin/bash

export tmp_version=${version//-/__}
export shortened_version=${tmp_version%__*}
export package_version=${shortened_version/__/a}

cd "$PROJECT_PATH"
hatch version "$package_version"
hatch build
hatch publish -r ${PUBLISH_URL}
