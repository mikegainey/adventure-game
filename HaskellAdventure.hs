-- a text adventure game

import Data.List (intercalate)

data Status = Status {location :: Location,
                      items :: [(Item, Location, [Property])]}
            deriving (Show)

type Location = String
type Item = String
type Description = String
type Property = String

start = Status {location="kitchen",
                items=[("cheese", "kitchen", []), ("apple", "kitchen", []),
                      ("book", "dining hall", []), ("knife", "ballroom", []),
                      ("matches", "inventory", ["dry"]), ("torch", "inventory", ["not lit"]),
                      ("spoon", "inventory", [])]}

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

paths :: [(Location, [(Location, String)])] -- [(Location, [(connected Location, how to get there)])]
paths = [("kitchen", [("dining hall", "south")]),
        ("dining hall", [("kitchen", "north"), ("ballroom", "west")]),
        ("ballroom", [("dining hall", "east"), ("balcony", "up the stairs")]),
        ("balcony", [("ballroom", "down the stairs")])]


-- the game loop
game status = do putStrLn $ describe status
                 putStr "Now what? "
                 command <- getLine
                 let newStatus = update status command
                 game newStatus

describe :: Status -> String
describe status = "\n\nLocation: " ++ (describeLocation status) ++
                  "\nYou see: " ++ (describeItems status) ++
                  "\n\nInventory: " ++ (describeInventory status) ++
                  "\n\nPlaces you can go from here:\n" ++ (describePaths status)

describeLocation status = head $ find name locations
  where name = location status

describeItems status = listItems itemList
  where placeName = location status
        itemList = [description | (name, description, place)<- items, place == placeName]

describeInventory status = "You have " ++ itemList
  where items = [name | (name, place, properties) <- (items status)]
        itemList = listItems items

listItems items = case (length items) of
  0 -> ""
  1 -> (head items) ++ "."
  2 -> (head items) ++ " and " ++ (last items) ++ "."
  _ -> (intercalate ", " (init items)) ++ ", and " ++ (last items)  ++ "."

describePaths status = unlines $ map format (getPaths status)
  where format (i, newloc, path) = concat [i, ". ", newloc, ": ", path]

getPaths status = [(show i, newLocation, path) | (i, (newLocation, path)) <- zip [1..] pathlist]
  where currentLocation = location status
        pathlist = head $ find currentLocation paths

update :: Status -> String -> Status
update status command
  | command `elem` (map show [1..9]) = move status command
  | verb == "take"                   = takeItem status command
  | otherwise = status
  where verb = head $ words command
        object = last $ words command

move :: Status -> String -> Status
move status command = if newLocation == []
                      then status
                      else status {location = (head newLocation)}
  where pathlist = getPaths status
        newLocation = [location | (i, location, path)<- pathlist, i == command]

takeItem :: Status -> String -> Status
takeItem status command = status
  where object = last $ words command
        isPresent = (not . null) [name | (name, description, place)<- items, name == object]

-- find key in table, return value or [] if key not found
find key table = [v | (k,v) <- table, k == key]

{-| to take items:

redo items:
- status should keep track of all items [("name", "location")]. location = "backpack" for carried items
- items = [("name", "description")]

-}

