# Distributed Virtual Machine Management System

A web-based application for monitoring and controlling virtual machines across multiple physical servers.

## Team Members

* Noah Foli
* Johnathan Beals

## Project Overview

This project is being developed for our Object-Oriented Programming final project.

The goal is to create a web dashboard that allows users to view and control virtual machines running on multiple physical servers from one location.

Users will be able to:

* View available virtual machines
* See whether a virtual machine is running or stopped
* Start virtual machines
* Stop virtual machines
* Restart virtual machines
* Manage virtual machines across multiple servers

## Project Goals

The project is designed to demonstrate object-oriented programming concepts while also working with real-world technologies such as:

* Object-Oriented Programming
* Virtual Machines
* Networking
* Web Development
* APIs
* Docker
* Automated Testing

## Planned Architecture

```text
                Web Dashboard
                      |
                      v
              Backend Application
                      |
             -------------------
             |                 |
             v                 v
         Server 1           Server 2
             |                 |
             v                 v
      Virtual Machines   Virtual Machines
```

The web dashboard will communicate with the backend application. The backend will then communicate with each physical server to retrieve virtual machine information and send management commands.

## Object-Oriented Design

The backend will use classes to represent the different parts of the system.

Some planned classes may include:

```text
Server
VirtualMachine
VMManager
Hypervisor
```

These classes will handle responsibilities such as storing server information, tracking virtual machine states, and performing virtual machine operations.

## Docker

Docker will be used to provide a consistent environment for running and testing the project.

This will help ensure that the application can be run on another computer without requiring the exact same server setup used during development.

## Testing

Automated test cases will be created for the main features of the application.

Tests may include:

* Starting a stopped virtual machine
* Stopping a running virtual machine
* Restarting a virtual machine
* Checking virtual machine status
* Handling invalid operations
* Handling unavailable servers

Mock virtual machines may be used during testing so that the automated tests do not depend on our physical servers being available.

## Current Status

🚧 Project currently in development.

## Authors

**Noah Foli**
**Johnathan Beals**

Object-Oriented Programming Final Project
