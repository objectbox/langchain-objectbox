#!/usr/bin/env bash
set -e

script_dir=$( cd "$(dirname "$0")" ; pwd -P )
project_dir=$script_dir/..
repo_dir=$project_dir/../objectbox-langchain

cp $repo_dir/libs/community/langchain_community/vectorstores/objectbox.py $project_dir/libs/objectbox/langchain_objectbox/vectorstores.py
cp $repo_dir/libs/community/tests/integration_tests/vectorstores/test_objectbox.py $project_dir/libs/objectbox/tests/integration_tests/

sed -i s/langchain_community.vectorstores.objectbox/langchain_objectbox/g $project_dir/libs/objectbox/tests/integration_tests/test_objectbox.py
sed -i s@../../docs/docs/modules@testdata@g $project_dir/libs/objectbox/tests/integration_tests/test_objectbox.py
sed -i 's@from langchain_community.embeddings import HuggingFaceEmbeddings@@g' $project_dir/libs/objectbox/tests/integration_tests/test_objectbox.py
sed -i 's@HuggingFaceEmbeddings()@ConsistentFakeEmbeddings(dimensionality=768)@g' $project_dir/libs/objectbox/tests/integration_tests/test_objectbox.py