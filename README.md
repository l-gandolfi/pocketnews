# PocketNews
> Project for the Laboratorio di Progettazione course at University of Milano-Bicocca 

## Brief

The project aims to implement a webapp allowing users to view suggested news by a recommender system based on their topics of interest and their interactions system. The system allows also for social functionalities, letting users interact with each other.

## Structure

The repository is structured as a folder for each container, each corresponding to a component in the system architecture.

- [`api`](api) contains the code for the backend in Flask
- [`recommender`](recommender) contains the code for the recommender system
- [`web`](web) contains the code for the frontend in Vue.js

## Prerequisites
* Docker
* Docker Compose

## Installation
```sh
$ git clone https://github.com/l-gandolfi/pocketnews
$ cd pocketnews
```

## Authors

* [**Luca Gandolfi**](https://github.com/l-gandolfi/) (807485)
* [**Nassim Habbash**](https://github.com/nhabbash) (808292)
* [**Bruno Palazzi**](https://gitlab.com/Spolli) (806908)
* [**Stefano Sacco**](https://gitlab.com/stefano250396) (807532)
* [**Giacomo Villa**](https://gitlab.com/Villons96) (807462)

## Note
Due to github's 100MB limit, the populated DB will not be provided.