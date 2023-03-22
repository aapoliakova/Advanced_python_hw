cd hw_2
docker build -t docker_hw2 $(pwd)
docker run --mount src=$(pwd)/artifacts,target=/results_art,type=bind -it docker_hw2
