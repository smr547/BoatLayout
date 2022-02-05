BoatGraph records the layout of a boat as a graph of Spaces and Access ports.

## Data model

The following UML class diagram shows the data structure for BoatGraph.

![Data Model](./data/dataModel_class_UML.jpg)

A Boat consist of many Spaces. Spaces are used for various purposes including human occupation, equipment installation and storage.

An Access is a connection between two spaces. Examples are doorways, hatches and opening of other kinds. Some accesses allow human passage while  others are only allow a humand to reach in (e.g. small storage compartments).
