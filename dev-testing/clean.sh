if [ -d "../temp" ]; then
  # count files to delete
  file_count=$(ls -1q ../temp/* | wc -l)
  echo "deleting $file_count files in temp"
  # delete all files in temp
  rm -rf ../temp/*
  # if cleaned echo good
  if [ -z "$(ls -A ../temp)" ]; then
    echo "deleted $file_count files in temp"
  fi
fi