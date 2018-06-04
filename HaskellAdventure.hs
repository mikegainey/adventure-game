-- text adventure game

import Data.List (intercalate)

data Status = Status {location :: String,
                      inventory :: [String]}
            deriving (Show)

main = game start

start = Status {location="the old gas station", inventory=["a book of matches", "an old metal spoon"]}

game status = do putStrLn $ describe status
                 putStr "Now what? "
                 command <- getLine
                 let newStatus = update status
                 game newStatus

describe :: Status -> String
describe status = "\nLocation: " ++ (describeLocation status) ++
                  "\nInventory: " ++ (describeInventory status)

describeLocation status = concat ["You are at ", name, ". ", description]
  where name = location status
        description = head $ find name locations

describeInventory status = "You have " ++ intercalate ", " (inventory status)

update s = s

-- returns [] if key not found
find key table = [v | (k,v) <- table, k == key]

-- [(name, description)]
locations = [("the old gas station", "The attendant looks like he doesn't want your business."),
            ("the post office", "No one remembers what a post office does anymore.")]

-- [(location, [connected locations])]
paths = []
