-- A text adventure game in Haskell (just to see if I can do it).

import Data.List (intercalate)

main = game start

--------------------------------------------------------------------------------
-- data definitions and aliases
--------------------------------------------------------------------------------

data World = World {_location :: Location,
                    _items    :: [(Item, Location, [Property])],
                    _paths    :: [(Location, [(Location, String, [Property])])]
                   }
  deriving (Show)

-- just to make type signatures more descriptive
type Location    = String
type Item        = String
type Description = String
type Property    = String

--------------------------------------------------------------------------------
-- things in the world that can change
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------
-- things in the world that don't change
--------------------------------------------------------------------------------

items :: [(Item, Description, [Property])]
items = [("cheese", "a smelly piece of cheese", []),
          ("apple", "an apple", []),
          ("book", "a book", []),
          ("knife", "a knife", []),
          ("matches", "a book of matches", []),
          ("torch", "a torch", ["not lit"]),
          ("spoon", "an old metal spoon", [])]

locations :: [(Location, Description)]
locations = [("kitchen", "The kitchen. A dank and dirty room buzzing with flies."),
             ("dining hall", "The dining hall. A large room with ornate golden decorations on each wall."),
             ("ballroom", "The ballroom. A vast room with a shiny wooden floor.\nHuge candlesticks guard the entrance. Stairs lead to a balcony overlooking the ballroom."),
             ("balcony", "A balcony surrounding and overlooking the ballroom.\nStairs lead back down to the ballroom floor.")]

--------------------------------------------------------------------------------
-- the game loop: display status; get player's command; update world; repeat
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------
-- describing the player's current location
--------------------------------------------------------------------------------

describeLocation :: World -> Description
describeLocation world = case (lookup currentLocation locations) of
                           (Just description) -> description
                           nothing            -> currentLocation
  where currentLocation = _location world

--------------------------------------------------------------------------------
-- describing items in the current location and the player's inventory
--------------------------------------------------------------------------------

describeItems :: World -> String
describeItems world = listItems itemDescriptions
  where currentLocation = _location world
        itemNames = itemsIn world currentLocation
        itemDescriptions = map item2description itemNames

describeInventory :: World -> String
describeInventory world = "You have " ++ (listItems itemDescriptions)
  where itemNames = itemsIn world "inventory"
        itemDescriptions = map item2description itemNames

itemsIn :: World -> Location -> [Item]
itemsIn world place = [iName | (iName, iPlace, _) <- (_items world), iPlace == place]

item2description itemName = i2d itemName items
  where i2d target [] = itemName
        i2d target ((n,d,p):xs) | n == target = d
                                | otherwise   = i2d target xs

listItems :: [Item] -> String
listItems items = case (length items) of
  0 -> ""
  1 -> (head items) ++ "."
  2 -> (head items) ++ " and " ++ (last items) ++ "."
  _ -> (intercalate ", " (init items)) ++ ", and " ++ (last items)  ++ "."

--------------------------------------------------------------------------------
-- describing paths the player can take from the current location
--------------------------------------------------------------------------------

describePaths :: World -> String
describePaths world = unlines $ map format (getPaths world)
  where format (i, newloc, path) = concat [i, ". ", newloc, ": ", path]

getPaths :: World -> [(String, Location, String)]
getPaths world = [(show i, newLocation, path) | (i, (newLocation, path, _)) <- zip [1..] pathlist]
  where currentLocation = _location world
        pathlist = case (lookup currentLocation (_paths world)) of
          (Just pathlist) -> pathlist
          nothing         -> [("kitchen", "RESET LOCATION", [])]

--------------------------------------------------------------------------------
-- call functions to perform player commands
--------------------------------------------------------------------------------

update :: World -> String -> World
update world command
  | command `elem` (map show [1..9]) = move world command
  | verb `elem` ["take", "get"]   = takeItem world command
  | verb `elem` ["leave", "drop"] = leaveItem world command
  | otherwise = world
  where verb   = head $ words command
        object = last $ words command

--------------------------------------------------------------------------------
-- functions to implement player commands
--------------------------------------------------------------------------------

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
