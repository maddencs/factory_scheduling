terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_network" "factory_net" {
  name = "factory_net"
}

resource "docker_image" "postgres" {
  name = "postgres:16"
  keep_locally = false
}

resource "docker_container" "db" {
  name  = "factory_db"
  image = docker_image.postgres.name
  networks_advanced {
    name = docker_network.factory_net.name
  }

  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=password",
    "POSTGRES_DB=factory_db"
  ]

  ports {
    internal = 5432
    external = 5432
  }
}

resource "docker_image" "app" {
  name = "factory_scheduling_app"
  build {
    context = "${path.module}/"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "app" {
  name  = "your_app"
  image = docker_image.app.name
  ports {
    internal = 8000
    external = 8000
  }
}
