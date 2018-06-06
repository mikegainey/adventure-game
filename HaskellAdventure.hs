-- a text adventure game in Haskell

import Data.List (intercalate)

data World = World {_location :: Location,
                    _items    :: [(Item, Location, [Property])],
                    _paths    :: [(Location, [(Location, String, [Property])])]}
  deriving (Show)

type Location    = String
type Item        = String
type Description = String
type Property    = String

start = World {_location = "kitchen",
               -- items :: [(Item, Location, [Property])]
               _items = [("cheese", "kitchen", []), ("apple", "kitchen", []),
                        ("book", "dining hall", []), ("knife", "ballroom", []),
                        ("matches", "inventory", ["wet"]), ("torch", "inventory", ["not lit"]),
                        ("spoon", "inventory", [])],
               -- paths :: [(Location, [(connected Location, how to get there, [Property])])]
               _paths = [("kitchen", [("dining hall", "south", [])]),
                        ("dining hall", [("kitchen", "north", []), ("ballroom", "west", [])]),
                        ("ballroom", [("dining hall", "east", []), ("balcony", "up the stairs", ["blocked"])]),
                        ("balcony", [("ballroom", "down the stairs", [])])] }

items :: [(Item, Description, [Property])]
items = [("cheese", "a smelly piece of cheese", []), ("apple", "an apple", []),
                    ("book", "a book", []), ("knife", "a knife", []),
                    ("matches", "a book of matches", []), ("torch", "a torch", []),
                    ("spoon", "an old metal spoon", [])]

main = game start

locations :: [(Location, Description)]
locations = [("kitchen", "The kitchen. A dank and dirty room buzzing with flies."),
             ("dining hall", "The dining hall. A large room with ornate golden decorations on each wall."),
             ("ballroom", "The ballroom. A vast room with a shiny wooden floor.\nHuge candlesticks guard the entrance. Stairs lead to a balcony overlooking the ballroom."),
             ("balcony", "A balcony surrounding and overlooking the ballroom.\nStairs lead back down to the ballroom floor.")]

-- the game loop
game world = do putStrLn $ describe world
                putStr "Now what? "
                command <- getLine
                let newWorld = update world command
                game newWorld

describe :: World -> String
describe world = "\n\nLocation: " ++ (describeLocation world) ++
                 "\nYou see " ++ (describeItems world) ++
                 "\n\nInventory: " ++ (describeInventory world) ++
                 "\n\nPlaces you can go from here:\n" ++ (describePaths world)

describeLocation world = head $ find name locations
  where name = _location world

describeItems world = listItems itemDescriptions
  where currentLocation = _location world
        itemNames = itemsIn world currentLocation
        itemDescriptions = items2descriptions itemNames

describeInventory world = "You have " ++ (listItems itemDescriptions)
  where itemNames = itemsIn world "inventory"
        itemDescriptions = items2descriptions itemNames

itemsIn world place = [itemName | (itemName, itemPlace, _) <- (_items world),
                        itemPlace == place]

items2descriptions itemNames = [description | itemName <- itemNames,
                                (name, description, _) <- items,
                                name == itemName]

listItems items = case (length items) of
  0 -> ""
  1 -> (head items) ++ "."
  2 -> (head items) ++ " and " ++ (last items) ++ "."
  _ -> (intercalate ", " (init items)) ++ ", and " ++ (last items)  ++ "."

describePaths world = unlines $ map format (getPaths world)
  where format (i, newloc, path) = concat [i, ". ", newloc, ": ", path]

getPaths world = [(show i, newLocation, path) | (i, (newLocation, path, _)) <- zip [1..] pathlist]
  where currentLocation = _location world
        pathlist = head $ find currentLocation (_paths world)

update :: World -> String -> World
update world command
  | command `elem` (map show [1..9]) = move world command
  | verb == "take"  = takeItem world command
  | verb == "leave" = leaveItem world command
  | otherwise       = world
  where verb   = head $ words command
        object = last $ words command

move :: World -> String -> World
move world command = if newLocation == []
                      then world
                      else world {_location = (head newLocation)}
  where pathlist = getPaths world
        newLocation = [location | (i, location, path)<- pathlist, i == command]

takeItem :: World -> String -> World
takeItem world command
  | isPresent = world {_items = new_items}
  | otherwise = world
  where object = last $ words command
        location = _location world
        isPresent = object `elem` (itemsIn world location)
        new_items = map update (_items world)
        update (it,loc,prop) = if it == object
                               then (it,"inventory",prop)
                               else (it,loc,prop)

leaveItem :: World -> String -> World
leaveItem world command
  | inInventory = world {_items = update_items}
  | otherwise = world
  where object = last $ words command
        location = _location world
        inInventory = object `elem` (itemsIn world "inventory")
        update_items = map update (_items world)
        update (it,loc,prop) = if it == object
                               then (it, location, prop)
                               else (it, loc, prop)

-- find key in table, return value or [] if key not found
find key table = [v | (k,v) <- table, k == key]

{-| to take items:

- verify the item is in the current location
- if so, change item location to inventory

-}

